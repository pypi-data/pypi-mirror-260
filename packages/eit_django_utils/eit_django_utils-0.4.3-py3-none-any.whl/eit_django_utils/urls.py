# -*- coding: utf-8 -*-
from django.urls import re_path
from django.views.generic import TemplateView

from . import views

app_name = "eit_django_utils"
urlpatterns = [
    re_path(r"^$", TemplateView.as_view(template_name="eit_django_utils/base.html"), name="base"),
    re_path(r"^logout$", views.logout, name="logout"),
    re_path(r"^403/$", TemplateView.as_view(template_name="eit_django_untils/403.html"), name="403"),
    re_path(r"^404/$", TemplateView.as_view(template_name="eit_django_utils/404.html"), name="404"),
    re_path(r"^500/$", TemplateView.as_view(template_name="eit_django_utils/500.html"), name="500"),
]
