from django.test import override_settings, TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from re import compile


from eit_django_utils.urls import *
from eit_django_utils.views import *

from eit_django_utils.backends.custom_auth import (
    SetLocalDevShibUID,
    CustomRemoteUserBackend,
    CustomHijackMiddleware,
    ShibAffiliationRequiredMiddleware,
    LoginRequiredMiddleware,
    SpecialGroupRequiredMiddleware,
)


@override_settings(
    LOCALDEV_SHIB_UID="jdoe1",
    DEBUG=True,
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
    ],
)
class EitDjangoUtilsBaseTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user_model = get_user_model()
        username_field = user_model.USERNAME_FIELD
        jdoe1 = user_model.objects.create(
            **{
                "id": 1,
                username_field: "jdoe1",
                "first_name": "John",
                "last_name": "Doe",
                "email": "jdoe1@ncsu.edu",
                "is_active": True,
            }
        )
