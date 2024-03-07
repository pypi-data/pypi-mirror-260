from datetime import datetime, timedelta
from django.test import override_settings, TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils import timezone
from pathlib import Path
from re import compile

import json

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

from .test_shared import EitDjangoUtilsBaseTest

BASE_DIR = Path(__file__).resolve().parent.parent


@override_settings(
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [
                BASE_DIR / "templates",
            ],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                    "eit_django_utils.context_processors.favicon",
                ],
            },
        },
    ],
)
class TestFavicon(EitDjangoUtilsBaseTest, TestCase):
    """make sure the various favicons that are supplied via context processors are providing something that's retrievable"""

    @override_settings(
        ALLOWED_HOSTS=["127.0.0.1", "localhost", "testserver"],
        DEBUG=True,
        LOGIN_EXEMPT_URLS=[
            r"^eit_utils/$",
        ],
    )
    def test_local_icon(self):
        """if debug is True and we're making a request against localhost or 127.0.0.1, the local icon should be used"""

        response = self.client.get(reverse("eit_django_utils:base"))
        self.assertEqual(response.status_code, 200)

        favicon = response.context.get("favicon")

        self.assertTrue("wolficon-local.svg" in favicon)

    @override_settings(
        ALLOWED_HOSTS=["testserver"],
        DEBUG=True,
        LOGIN_EXEMPT_URLS=[
            r"^eit_utils/$",
        ],
    )
    def test_dev_icon(self):
        """if debug is True and we're not making a request against localhost or 127.0.0.1, the dev icon should be used"""
        response = self.client.get(reverse("eit_django_utils:base"))
        self.assertEqual(response.status_code, 200)

        favicon = response.context.get("favicon")

        self.assertTrue("wolficon-dev.svg" in favicon)

    @override_settings(
        ALLOWED_HOSTS=["localhost", "127.0.0.1", "testserver"],
        DEBUG=False,
        MIDDLEWARE=[
            "django.middleware.security.SecurityMiddleware",
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.middleware.common.CommonMiddleware",
            "django.middleware.csrf.CsrfViewMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            # "django_browser_reload.middleware.BrowserReloadMiddleware",
            # "eit_django_utils.backends.custom_auth.SetLocalDevShibUID",
            "eit_django_utils.backends.custom_auth.CustomHijackMiddleware",
            "eit_django_utils.backends.custom_auth.ShibAffiliationRequiredMiddleware",
            "eit_django_utils.backends.custom_auth.LoginRequiredMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
            "django.middleware.clickjacking.XFrameOptionsMiddleware",
        ],
        LOGIN_EXEMPT_URLS=[
            r"^eit_utils/$",
        ],
    )
    def test_prod_icon(self):
        """if debug is False, the production favicon should be used"""
        response = self.client.get(reverse("eit_django_utils:base"))
        self.assertEqual(response.status_code, 200)

        favicon = response.context.get("favicon")

        self.assertTrue("wolficon.svg" in favicon)
