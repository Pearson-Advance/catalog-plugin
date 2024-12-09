"""Urls API file."""
from django.conf.urls import include, url

app_name = 'catalog_plugin.api'
urlpatterns = [
    url(r'^v0/', include('catalog_plugin.api.v0.urls', namespace='v0')),
]
