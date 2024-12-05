"""Django test settings."""

MIGRATION_MODULES = {
    'catalog_plugin': None,
}

DEBUG = True
INSTALLED_APPS = [
    'catalog_plugin',
]
MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    },
}

SILENCED_SYSTEM_CHECKS = ['fields.E300', 'fields.E307']

# Backends for tests
CP_COURSE_OLIVE_BACKEND = 'catalog_plugin.tests.backends_for_tests'
