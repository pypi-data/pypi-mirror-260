import time
from datetime import datetime
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib import auth
from django.shortcuts import redirect

def logout(request):
    auth.logout(request)
    return redirect("/Shibboleth.sso/Logout?return=https://shib.ncsu.edu/idp/profile/Logout")


class Handler403(TemplateView):
    template_name = "eit_django_utils/403.html"


class Handler404(TemplateView):
    template_name = "eit_django_utils/404.html"


class Handler500(TemplateView):
    template_name = "eit_django_utils/500.html"
