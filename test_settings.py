"""Django test settings."""

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
