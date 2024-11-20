"""App configuration for catalog_plugin."""

from __future__ import unicode_literals

from django.apps import AppConfig


class CatalogPluginConfig(AppConfig):
    """catalog_plugin configuration."""

    name = 'catalog_plugin'
    namespace = 'catalog_plugin'
    verbose_name = 'catalog_plugin'
    plugin_app = {
        'url_config': {
            'lms.djangoapp': {
                'namespace': namespace,
                'regex': rf'^{namespace}/',
                'relative_path': 'urls',
            },
        },
        'settings_config': {
            'lms.djangoapp': {
                'common': {'relative_path': 'settings.common'},
                'test': {'relative_path': 'settings.test'},
            },
        },
    }
