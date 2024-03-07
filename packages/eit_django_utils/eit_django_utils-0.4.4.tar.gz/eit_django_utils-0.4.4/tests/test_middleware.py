from http import HTTPStatus

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase, override_settings
from django.urls import reverse

from .test_shared import EitDjangoUtilsBaseTest


class TestUserThatDoesntExist(EitDjangoUtilsBaseTest, TestCase):
    def test_home_view_403(self):
        response = self.client.get(
            reverse("eit_django_utils:base"),
            SHIB_UID="unknown_user",
            SHIB_AFFILIATION="member@ncsu.edu",
        )
        self.assertEqual(response.status_code, 403)

    def test_create_unknown_user(self):
        response = self.client.get(reverse("eit_django_utils:base"))
        user_model = get_user_model()
        self.assertEqual(user_model.objects.count(), 1)

        username_field = user_model.USERNAME_FIELD
        employee = user_model.objects.get(id=1)
        self.assertEqual(getattr(employee, username_field), "jdoe1")
        self.assertNotEqual(getattr(employee, username_field), "unknown_user")

    def test_helpdesk_email_default(self):
        response = self.client.get(
            reverse("eit_django_utils:base"),
            SHIB_UID="unknown_user",
            SHIB_AFFILIATION="member@ncsu.edu",
        )

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertContains(response, text="eithelpdesk@ncsu.edu", status_code=HTTPStatus.FORBIDDEN)
        self.assertContains(response, text="user does not exist", status_code=HTTPStatus.FORBIDDEN)

    @override_settings(EIT_HELPDESK_EMAIL="testemail@ncsu.edu")
    def test_helpdesk_email_custom(self):
        response = self.client.get(
            reverse("eit_django_utils:base"),
            SHIB_UID="unknown",
            SHIB_AFFILIATION="member@ncsu.edu",
        )

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertContains(response, text=settings.EIT_HELPDESK_EMAIL, status_code=HTTPStatus.FORBIDDEN)


class TestSetLocalDevShibUID(EitDjangoUtilsBaseTest):
    def test_unity_id_content(self):
        user_model = get_user_model()
        username_field = user_model.USERNAME_FIELD
        employee = user_model.objects.get(id=1)
        self.assertEqual(getattr(employee, username_field), "jdoe1")

    def test_unity_id_content2(self):
        user_model = get_user_model()
        username_field = user_model.USERNAME_FIELD
        employee = user_model.objects.get(id=1)
        self.assertNotEqual(getattr(employee, username_field), "jdoe")


@override_settings(
    MIDDLEWARE=[
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        # SetLocalDevShibUID is only for local development!
        # "eit_django_utils.backends.custom_auth.SetLocalDevShibUID",
        "eit_django_utils.backends.custom_auth.CustomHijackMiddleware",
        "eit_django_utils.backends.custom_auth.ShibAffiliationRequiredMiddleware",
        "eit_django_utils.backends.custom_auth.LoginRequiredMiddleware",
        "eit_django_utils.backends.custom_auth.SpecialGroupRequiredMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]
)
class TestSpecialGroupRequired(EitDjangoUtilsBaseTest):
    def test_non_member(self):
        response = self.client.get(
            reverse("eit_django_utils:base"),
            SHIB_UID="jdoe1",
            SHIB_AFFILIATION="member@ncsu.edu",
        )
        self.assertEqual(response.status_code, 403)

    def test_testers_member(self):
        testers = Group.objects.create(name="testers")
        user_model = get_user_model()
        username_field = user_model.USERNAME_FIELD
        employee = user_model.objects.get(**{username_field: "jdoe1"})
        employee.groups.add(testers)
        response = self.client.get(
            reverse("eit_django_utils:base"),
            SHIB_UID="jdoe1",
            SHIB_AFFILIATION="member@ncsu.edu",
        )
        self.assertEqual(response.status_code, 200)

    def test_eit_admin_member(self):
        eit_admin = Group.objects.create(name="eit_admin")
        user_model = get_user_model()
        username_field = user_model.USERNAME_FIELD
        employee = user_model.objects.get(**{username_field: "jdoe1"})
        employee.groups.add(eit_admin)
        response = self.client.get(
            reverse("eit_django_utils:base"),
            SHIB_UID="jdoe1",
            SHIB_AFFILIATION="member@ncsu.edu",
        )
        self.assertEqual(response.status_code, 200)

    @override_settings(ALLOWED_GROUPS=[])
    def test_empty_allowed_groups(self):
        some_custom_group = Group.objects.create(name="some_custom_group")
        user_model = get_user_model()
        username_field = user_model.USERNAME_FIELD
        employee = user_model.objects.get(**{username_field: "jdoe1"})
        employee.groups.add(some_custom_group)
        response = self.client.get(
            reverse("eit_django_utils:base"),
            SHIB_UID="jdoe1",
            SHIB_AFFILIATION="member@ncsu.edu",
        )
        self.assertEqual(response.status_code, 403)

    @override_settings(ALLOWED_GROUPS=["some_custom_group"])
    def test_custom_allowed_group(self):
        some_custom_group = Group.objects.create(name="some_custom_group")
        user_model = get_user_model()
        username_field = user_model.USERNAME_FIELD
        employee = user_model.objects.get(**{username_field: "jdoe1"})
        employee.groups.add(some_custom_group)
        response = self.client.get(
            reverse("eit_django_utils:base"),
            SHIB_UID="jdoe1",
            SHIB_AFFILIATION="member@ncsu.edu;",
        )
        self.assertEqual(response.status_code, 200)


@override_settings(
    MIDDLEWARE=[
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        # SetLocalDevShibUID is only for local development!
        # "eit_django_utils.backends.custom_auth.SetLocalDevShibUID",
        "eit_django_utils.backends.custom_auth.CustomHijackMiddleware",
        "eit_django_utils.backends.custom_auth.ShibAffiliationRequiredMiddleware",
        "eit_django_utils.backends.custom_auth.LoginRequiredMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]
)
class TestExemptUrls(EitDjangoUtilsBaseTest):
    def test_login_redirect(self):
        response = self.client.get(reverse("eit_django_utils:base"))
        self.assertEqual(response.status_code, 302)

    @override_settings(
        LOGIN_EXEMPT_URLS=[
            r"^eit_utils/$",
        ]
    )
    def test_exempt_url(self):
        response = self.client.get(reverse("eit_django_utils:base"))
        self.assertEqual(response.status_code, 200)


@override_settings(
    MIDDLEWARE=[
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        # SetLocalDevShibUID is only for local development!
        # "eit_django_utils.backends.custom_auth.SetLocalDevShibUID",
        "eit_django_utils.backends.custom_auth.CustomHijackMiddleware",
        "eit_django_utils.backends.custom_auth.ShibAffiliationRequiredMiddleware",
        "eit_django_utils.backends.custom_auth.LoginRequiredMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]
)
class TestShibAffiliationRequired(EitDjangoUtilsBaseTest):
    def test_shib_affiliation_member(self):
        """happy path - member@ncsu.edu should result in a 200"""
        user_model = get_user_model()
        username_field = user_model.USERNAME_FIELD
        employee = user_model.objects.get(**{username_field: "jdoe1"})

        self.client.force_login(employee)

        response = self.client.get(
            reverse("eit_django_utils:base"),
            SHIB_UID="jdoe1",
            SHIB_AFFILIATION="member@ncsu.edu;staff@ncsu.edu",
        )

        self.assertEqual(response.status_code, 200)

    @override_settings(ALLOWED_SHIB_AFFILIATIONS=["test1@ncsu.edu"])
    def test_shib_affiliation_custom_setting(self):
        """test with a custom affiliation via settings -test1@ncsu.edu should result in a 200"""
        user_model = get_user_model()
        username_field = user_model.USERNAME_FIELD
        employee = user_model.objects.get(**{username_field: "jdoe1"})

        self.client.force_login(employee)

        response = self.client.get(
            reverse("eit_django_utils:base"),
            SHIB_UID="jdoe1",
            SHIB_AFFILIATION="test1@ncsu.edu",
        )

        self.assertEqual(response.status_code, 200)

    @override_settings(ALLOWED_SHIB_AFFILIATIONS=["something@ncsu.edu"])
    def test_shib_affiliation_custom_setting_deny(self):
        """test an unspecified affiliation w/ custom ALLOWED_SHIB_AFFILIATIONS defined. 403 expected"""
        user_model = get_user_model()
        username_field = user_model.USERNAME_FIELD
        employee = user_model.objects.get(**{username_field: "jdoe1"})

        response = self.client.get(
            reverse("eit_django_utils:base"),
            SHIB_UID="jdoe1",
            SHIB_AFFILIATION="somethingelse@ncsu.edu;affiliate@ncsu.edu",
        )

        self.assertEqual(response.status_code, 403)
        self.assertContains(
            response,
            text="insufficient shibboleth affiliation",
            status_code=HTTPStatus.FORBIDDEN,
        )
        # make sure the output includes the affiliations that the user does have
        self.assertContains(
            response,
            text="somethingelse@ncsu.edu",
            status_code=HTTPStatus.FORBIDDEN,
        )
        self.assertContains(
            response,
            text="affiliate@ncsu.edu",
            status_code=HTTPStatus.FORBIDDEN,
        )

    def test_shib_affiliation_affiliate(self):
        """affiliate@ncsu.edu should result in a 403 by default"""

        user_model = get_user_model()
        username_field = user_model.USERNAME_FIELD
        employee = user_model.objects.get(**{username_field: "jdoe1"})

        response = self.client.get(
            reverse("eit_django_utils:base"),
            SHIB_UID="jdoe1",
            SHIB_AFFILIATION="affiliate@ncsu.edu;",
        )

        self.assertEqual(response.status_code, 403)

    def test_shib_headers_not_required_after_auth(self):
        """
        After a user authenticates via Shibboleth, we want Django's session authentication to take over.
        This prevents authentication oddities that we have run into when using the NCSU wifi -> AWS or
        County networks where requests can potentially come from multiple public IP addresses (NAT)
        """

        user_model = get_user_model()
        username_field = user_model.USERNAME_FIELD
        employee = user_model.objects.get(**{username_field: "jdoe1"})

        self.client.force_login(employee)

        response = self.client.get(reverse("eit_django_utils:base"))

        self.assertEqual(response.status_code, 200)
