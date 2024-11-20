"""
Tests for the `catalog_plugin` apps module.
For more information on this file, see:
https://docs.python.org/3/library/unittest.html
"""
from django.test import TestCase
from jsonschema import validate

from catalog_plugin.apps import CatalogPluginConfig


class TestCatalogPluginConfig(TestCase):
    """Test catalog_plugin app config."""

    config = CatalogPluginConfig

    def test_plugin_app_schema(self):
        """
        Test class plugin_app configuration schema.
        For more information on this test, see:
        https://python-jsonschema.readthedocs.io/en/stable/
        """
        settings_config_properties = {
            'type': 'object',
            'required': ['common', 'test'],
            'patternProperties': {
                '^.*$': {
                    'type': 'object',
                    'required': ['relative_path'],
                    'properties': {'relative_path': {'type': 'string'}},
                },
            },
        }
        schema = {
            'type': 'object',
            'required': ['settings_config'],
            'properties': {
                'settings_config': {
                    'type': 'object',
                    'required': ['lms.djangoapp'],
                    'patternProperties': {'^.*$': settings_config_properties},
                },
            },
        }

        validate(instance=self.config.plugin_app, schema=schema)
