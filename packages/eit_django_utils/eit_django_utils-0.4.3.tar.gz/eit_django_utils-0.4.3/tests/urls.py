# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.conf.urls import include
from django.urls import path

from eit_django_utils.urls import app_name as eit_django_utils_app_name
from eit_django_utils.urls import urlpatterns as eit_django_utils_urls

urlpatterns = [
    path("eit_utils/", include((eit_django_utils_urls, eit_django_utils_app_name))),
]
