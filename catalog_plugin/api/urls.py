"""URLs API file."""
from django.urls import include, re_path

app_name = 'catalog_plugin.api'

urlpatterns = [
    re_path(r'^v0/',include(('catalog_plugin.api.v0.urls', 'v0'), namespace='v0')),
]
