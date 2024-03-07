from django.conf import settings


def favicon(request):
    context_extras = {}
    favicon = "https://brand.ces.ncsu.edu/images/icons/{}"
    if settings.DEBUG:
        allowed_hosts = settings.ALLOWED_HOSTS
        if not allowed_hosts or "localhost" in allowed_hosts or "127.0.0.1" in allowed_hosts:
            context_extras["favicon"] = favicon.format("wolficon-local.svg")
        else:
            context_extras["favicon"] = favicon.format("wolficon-dev.svg")
    else:
        context_extras["favicon"] = favicon.format("wolficon.svg")
    return context_extras
