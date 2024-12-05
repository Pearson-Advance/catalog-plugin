"""Course module definitions."""
from importlib import import_module

from django.conf import settings


def course_overview():
    """Get get_course_overview method."""
    backend_function = settings.CP_COURSE_OLIVE_BACKEND
    backend = import_module(backend_function)

    return backend.course_overview_backend()
