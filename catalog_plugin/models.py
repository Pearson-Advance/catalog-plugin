"""Database ORM models managed by this plugin."""
import json
import uuid

from django.core.exceptions import ValidationError
from django.db import models
from model_utils.managers import InheritanceManager
from model_utils.models import TimeStampedModel

from catalog_plugin.edxapp_wrapper.course_module import course_overview


class AvailableCourse(models.Model):
    """
    Represent an available course.

    Attributes:
        course (str): The name of the course.
        active (bool): Indicates whether the course is currently active.
    """

    course = models.ForeignKey(course_overview(), on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        """Available Courses object is represented according to the course and status.

        Returns:
            str: Name of the catalogue.
        """
        return f'{self.course} - {self.active}'


class FlexibleCatalogModel(TimeStampedModel):
    """
    Abstract base class for catalog models.

    This class provides common attributes and functionalities for different
    catalog models. It should not be used directly but rather extended
    by specific catalog model classes.

    Attributes:
        id (UUIDField): Unique identifier for the catalog entry (primary key).
        slug (SlugField): Unique slug generated from the name for URL purposes.
            (optional, blank=True)
        name (CharField): Human-readable name for the catalog entry.
            (max_length=255)
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # type: ignore
    slug = models.SlugField(unique=True, blank=True, max_length=255)  # type: ignore
    name = models.CharField(max_length=255, help_text='Human friendly')  # type: ignore

    objects = InheritanceManager()

    def get_courses(self):
        """Catalog class returns every AvailableCourse."""
        return AvailableCourse.objects.all()

    def __str__(self):
        """Get a string representation of this model instance."""
        return f'<FlexibleCatalogModel, ID: {self.id}>'


class FixedCatalog(FlexibleCatalogModel):
    """Represent the custom fixed catalog model."""

    course_runs = models.ManyToManyField(course_overview(), blank=True)

    def get_course_runs(self):
        """
        Returns the associated course_runs.
        """
        return self.course_runs.all()

    def __str__(self):
        return f'FixedCatalog: {self.id}'


class CatalogCourses(FlexibleCatalogModel):
    """
    Represent a course offering within a catalog.

    This class inherits from `FlexibleCatalogModel` and extends it with
    a many-to-many relationship to `AvailableCourse` objects through the
    `course_runs` field.

    Attributes:
        course_runs (ManyToManyField): A many-to-many relationship with
            `AvailableCourse` objects representing specific course runs
            associated with this catalog course offering. (blank=True)
    """

    class Meta:
        verbose_name_plural = 'Catalog Courses'

    courses = models.ManyToManyField(  # type: ignore
        AvailableCourse,
        verbose_name='Available Courses',
    )

    def get_courses(self):
        """Return the associated courses."""
        return self.courses.all()

    def __str__(self):
        """Get a string representation of this model instance."""
        return f'CatalogCourses: {self.id} - {self.name}'


class DynamicCatalog(FlexibleCatalogModel):
    """
    Represent a dynamic catalog for filtering courses based on a JSON query string.

    This class extends `FlexibleCatalogModel` and allows for dynamic filtering
    of courses using a JSON-formatted query string stored in the `query_string` field.

    Attributes:
        query_string (TextField): A JSON-formatted string containing filters
            for retrieving courses. (optional, blank=True, null=True)
    """

    query_string = models.TextField(  # type: ignore
        help_text='Dynamic query string to filter courses.',
        blank=True,
        null=True,
    )

    def get_courses(self):
        """Filter courses dynamically based on the query_string."""
        if self.query_string:
            try:
                # Dynamically filter CourseOverview using the query string as json
                filter_params = json.loads(self.query_string)
                if not isinstance(filter_params, dict):
                    raise ValidationError('Query string must be a JSON object.')
                return course_overview().objects.filter(**filter_params)
            except Exception as e:
                raise ValueError(f'Invalid query_string: {e}') from e
        return course_overview().objects.none()

    def __str__(self):
        """Get a string representation of this model instance."""
        return f'DynamicCatalog: {self.id}'
