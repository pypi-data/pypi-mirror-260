from datetime import datetime
from django.contrib import auth
from django.contrib.auth.middleware import PersistentRemoteUserMiddleware, RemoteUserMiddleware
from django.contrib.auth.backends import RemoteUserBackend
from django.contrib.auth.views import redirect_to_login
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http.response import HttpResponseForbidden
from hijack.middleware import HijackRemoteUserMiddleware
from re import compile

from django.conf import settings


class SetLocalDevShibUID(MiddlewareMixin):
    def process_request(self, request):
        if settings.DEBUG and hasattr(settings, "LOCALDEV_SHIB_UID"):
            request.META["SHIB_UID"] = settings.LOCALDEV_SHIB_UID
            request.META["SHIB_AFFILIATION"] = request.META.get("SHIB_AFFILIATION", "") if "SHIB_AFFILIATION" in request.META else "member@ncsu.edu"
            request.META["Shib-Authentication-Instant"] = datetime.utcnow().isoformat() + "Z"
        else:
            raise ImproperlyConfigured(
                """
            Set Local Shib UID Middleware is enabled with no corresponding
            value in settings.py. Please disable this middleware or specify
            LOCALDEV_SHIB_UID = 'unity_id' in settings.py and ensure that
            DEBUG = True
            """
            )


class CustomRemoteUserBackend(RemoteUserBackend):
    create_unknown_user = False


class CustomHijackMiddleware(HijackRemoteUserMiddleware, MiddlewareMixin):
    """
    Sets the expected auth header to "SHIB_UID" for Hijack
    """

    header = "SHIB_UID"


class LoginRequiredMiddleware(MiddlewareMixin):
    """
    Requires a user to be authenticated to view any page other
    than LOGIN_URL. Exemptions to this requirement can optionally be specified
    in settings via a list of regular expressions in LOGIN_EXEMPT_URLS (which
    you can copy from your urls.py).

    Requires authentication middleware and template context processors to be
    loaded. You'll get an error if they aren't.
    """

    def process_request(self, request):
        assert hasattr(
            request, "user"
        ), "The Login Required middleware\
         requires authentication middleware to be installed. Edit your\
         MIDDLEWARE_CLASSES setting to insert\
         'django.contrib.auth.middlware.AuthenticationMiddleware'. If that doesn't\
         work, ensure your TEMPLATE_CONTEXT_PROCESSORS setting includes\
         'django.core.context_processors.auth'."
        if not request.user.is_authenticated:
            redirect_field_name = "target"
            EXEMPT_URLS = [compile(settings.LOGIN_URL.lstrip("/"))]
            if hasattr(settings, "LOGIN_EXEMPT_URLS"):
                EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]
            path = request.path_info.lstrip("/")
            if not any(m.match(path) for m in EXEMPT_URLS):
                path = request.get_full_path()
                return redirect_to_login(path, settings.LOGIN_URL, redirect_field_name)


class ShibAffiliationRequiredMiddleware(PersistentRemoteUserMiddleware):
    """
    Allow Shibboleth to handle login details then shifts to using the
    build in Django session behavior. There is also is modification
    to return a 403 for unknown/anonymous users.
    """

    header = "SHIB_UID"

    @staticmethod
    def handle_non_existant_user(reason):
        eit_helpdesk_email = "eithelpdesk@ncsu.edu"
        if hasattr(settings, "EIT_HELPDESK_EMAIL"):
            eit_helpdesk_email = settings.EIT_HELPDESK_EMAIL

        return HttpResponseForbidden(
            """
            Access to this site is restricted ({reason}).
            If you believe you should have access,
            please contact the EIT Help Desk at <a href="mailto:{email}">{email}</a>
            """.format(reason=reason, email=eit_helpdesk_email)
        )

    def check_affiliation(self, request):
        is_hijacked = request.session.get("is_hijacked_user", False)
        allowed_affiliations = ["member@ncsu.edu"]
        if hasattr(settings, "ALLOWED_SHIB_AFFILIATIONS"):
            allowed_affiliations = settings.ALLOWED_SHIB_AFFILIATIONS
        user_affiliations = [sa for sa in request.META.get("SHIB_AFFILIATION", "").split(";") if sa]
        if not any(affiliation in allowed_affiliations for affiliation in user_affiliations) and not is_hijacked:
            EXEMPT_URLS = [compile(settings.LOGIN_URL.lstrip("/"))]
            if hasattr(settings, "LOGIN_EXEMPT_URLS"):
                EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]
            path = request.path_info.lstrip("/")
            if not any(m.match(path) for m in EXEMPT_URLS):
                return self.handle_non_existant_user("insufficient shibboleth affiliation -- {ua}".format(ua=user_affiliations))

    def process_request(self, request):
        # AuthenticationMiddleware is required so that request.user exists.
        if not hasattr(request, "user"):
            raise ImproperlyConfigured(
                "The Django remote user auth middleware requires the"
                " authentication middleware to be installed.  Edit your"
                " MIDDLEWARE setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the RemoteUserMiddleware class."
            )
        try:
            username = request.META[self.header]
        except KeyError:
            # If specified header doesn't exist then remove any existing
            # authenticated remote-user, or return (leaving request.user set to
            # AnonymousUser by the AuthenticationMiddleware).
            if self.force_logout_if_no_header and request.user.is_authenticated:
                self._remove_invalid_user(request)
            return

        # Check shib affiliations before continuing to django-auth
        affiliation_issues = self.check_affiliation(request)
        if affiliation_issues:
            return affiliation_issues

        # If the user is already authenticated and that user is the user we are
        # getting passed in the headers, then the correct user is already
        # persisted in the session and we don't need to continue.
        if request.user.is_authenticated:
            if request.user.get_username() == self.clean_username(username, request):
                return
            else:
                # An authenticated user is associated with the request, but
                # it does not match the authorized user in the header.
                self._remove_invalid_user(request)

        # We are seeing this user for the first time in this session, attempt
        # to authenticate the user.
        user = auth.authenticate(request, remote_user=username)
        if not user:
            # 403 for user that isn't in the db
            return self.handle_non_existant_user("user does not exist")

        # User is valid.  Set request.user and persist user in the session
        # by logging the user in.
        request.user = user
        auth.login(request, user)


class SpecialGroupRequiredMiddleware(MiddlewareMixin):
    """
    Requires a user to be in the eit_admin or testers group to view any page other
    than LOGIN_URL. Can be configured to use other groups by definining
    ALLOWED_GROUPS = ['group_name_1', 'group_name_2'] in settings.py
    """

    def process_request(self, request):
        is_hijacked = request.session.get("is_hijacked_user", False)
        allowed_groups = settings.ALLOWED_GROUPS if hasattr(settings, "ALLOWED_GROUPS") else ["testers", "eit_admin"]
        user_groups = request.user.groups.all().values_list("name", flat=True)
        if not any(group in allowed_groups for group in user_groups) and not is_hijacked:
            EXEMPT_URLS = [compile(settings.LOGIN_URL.lstrip("/"))]
            if hasattr(settings, "LOGIN_EXEMPT_URLS"):
                EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]
            path = request.path_info.lstrip("/")
            if not any(m.match(path) for m in EXEMPT_URLS):
                return HttpResponseForbidden(
                    "Access to this site is restricted. If you believe you should have access, please contact EIT"
                )
