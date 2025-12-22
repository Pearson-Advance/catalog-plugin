"""Django URL configuration.

Attributes:
    app_name (str): URL pattern namespace.
    urlpatterns (list): URL patterns list.
"""
from django.urls import include, re_path

app_name = 'catalog_plugin'

urlpatterns = [
    re_path(r'^api/', include(('catalog_plugin.api.urls', 'api'), namespace='api')),
]
