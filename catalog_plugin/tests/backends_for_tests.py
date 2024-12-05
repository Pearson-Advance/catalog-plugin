"""This file contains all the necessary backends in a test scenario."""
from django.db import models


class CourseOverviewTestModel(models.Model):
    """Test model to enable unit testing."""

    class Meta:
        """Meta class."""

        app_label = 'catalog_plugin'


def course_overview_backend():
    """Fake get_course_enrollment_model class."""
    return CourseOverviewTestModel
