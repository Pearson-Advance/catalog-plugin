"""Django URL configuration.

Attributes:
    app_name (str): URL pattern namespace.
    urlpatterns (list): URL patterns list.
"""
from django.conf.urls import include, url

app_name = 'catalog_plugin'

urlpatterns = [
    url(r'^api/', include('catalog_plugin.api.urls', namespace='api')),
]
