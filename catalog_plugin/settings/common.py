"""Django common settings."""

from typing import Any


INSTALLED_APPS = [
    'rest_framework',
    'django_filters',
    'catalog_plugin',
]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}


def plugin_settings(settings: Any):  # pylint: disable=unused-argument
    """Open edX plugin settings.

    Args:
        settings: Django settings object.
    ...Open edX plugins app - README.rst:
        https://github.com/openedx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    # Backends Settings
    settings.CP_COURSE_OLIVE_BACKEND = 'catalog_plugin.edxapp_wrapper.backends.course_module_o_v1'
