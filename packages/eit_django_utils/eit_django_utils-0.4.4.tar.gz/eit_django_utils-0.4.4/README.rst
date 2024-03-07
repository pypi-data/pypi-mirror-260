=============================
EIT Django Utils
=============================

Convenient utils for EIT Django dev

Documentation
-------------

Quickstart
----------

Install EIT Django Utils::

    pip install eit_django_utils

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django-hijack',
        'eit_django_utils',
        ...
    )

Add EIT Django Utils's URL patterns:

.. code-block:: python

    from eit_django_utils import urls as eit_django_utils_urls


    urlpatterns = [
        ...
        path("eit_utils/", include(eit_django_utils_urls, namespace="eit_django_utils")),
        ...
    ]

Using with Django 2.2+ settings.py:

  .. code-block:: python

    MIDDLEWARE = [
      ...
      'django.contrib.auth.middleware.AuthenticationMiddleware',
      # SetLocalDevShibUID is only for local development!
      'eit_django_utils.backends.custom_auth.SetLocalDevShibUID',
      'eit_django_utils.backends.custom_auth.CustomHijackMiddleware',
      'eit_django_utils.backends.custom_auth.ShibAffiliationRequiredMiddleware',
      'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
      ...
    ]

    AUTHENTICATION_BACKENDS = (
    'eit_django_utils.backends.custom_auth.CustomRemoteUserBackend',
    )

    LOCALDEV_SHIB_UID = 'desired_unity_id'


