"""Django admin pages for Catalog models."""
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from catalog_plugin.models import AvailableCourse, CatalogCourses, DynamicCatalog, FlexibleCatalogModel


class CourseKeysMixin:
    """
    Mixin class providing functionality to render a list of course IDs.

    This mixin can be used by other classes to easily display the IDs of
    associated courses. It relies on the presence of a method named
    `get_courses` on the mixed-in class, which should return a queryset of
    course objects.

    Usage:
        - Inherit from `CourseKeysMixin` in your class definition.
        - Ensure your class implements the `get_courses` method to retrieve
            relevant courses.

    Attributes:
        course_keys (method): A method that retrieves and formats a list of
            course IDs.
    """

    def course_keys(self, obj):
        """
        Retrieve and formats a list of course IDs for the provided object.

        This method leverages the `get_courses` method (assumed to be
        implemented in the mixed-in class) to retrieve associated courses
        for the given object (`obj`). It then extracts the IDs from the
        courses and formats them into a human-readable HTML string with line
        breaks.

        Args:
            obj (Any): The object for which to retrieve course IDs.

        Returns:
            str: A formatted HTML string containing a list of course IDs, or
                the message "No courses available" if no courses are found.
        """
        courses = obj.get_courses()
        if courses.exists():
            course_ids = [str(course.id) for course in courses]
            return format_html('<br>'.join(course_ids))
        return 'No courses available'


@admin.register(FlexibleCatalogModel)
class FlexibleCatalogModelAdmin(admin.ModelAdmin, CourseKeysMixin):
    """Admin for the FlexibleCatalog model."""

    list_display = ('name', 'slug', 'id', 'model_class_name', 'course_keys')
    search_fields = ('name', 'slug', 'id')
    prepopulated_fields = {'slug': ('name',)}

    def model_class_name(self, obj):
        """Provide a link to the admin edit page for the specific subclass instance."""
        subclass_admin_url = reverse(
            f'admin:{obj._meta.app_label}_{obj.__class__.__name__.lower()}_change',
            args=[obj.id],
        )
        return format_html('<a href="{}">{}</a>', subclass_admin_url, obj.__class__.__name__)

    def get_queryset(self, request):
        """Override the queryset to use select_subclasses for subclass resolution."""
        return FlexibleCatalogModel.objects.select_subclasses()


@admin.register(CatalogCourses)
class CatalogCoursesAdmin(admin.ModelAdmin, CourseKeysMixin):
    """Admin for the CatalogCourse model."""

    list_display = ('__str__', 'display_courses')
    search_fields = ('flexible_catalog__name', 'flexible_catalog__slug', 'flexible_catalog__id')
    filter_horizontal = ('courses',)

    def display_courses(self, obj):
        """
        Return a comma-separated string representation of courses associated with the object.

        Args:
            obj (Any): The object for which to retrieve and display associated courses.

        Returns:
            str: A comma-separated string containing the string representations of
                all associated courses, or an empty string if no courses are found.
        """
        return ', '.join([str(course) for course in obj.courses.all()])


@admin.register(DynamicCatalog)
class DynamicCatalogAdmin(admin.ModelAdmin, CourseKeysMixin):
    """Admin for the DynamicCatalog model."""

    list_display = ('__str__', 'query_string', 'course_keys')
    search_fields = (
        'flexible_catalog__name',
        'flexible_catalog__slug',
        'flexible_catalog__id',
        'query_string',
    )

    def course_keys(self, obj):
        """Return the ids for easy debug in the admin views."""
        course_runs = obj.get_course_runs()
        if course_runs.exists():
            course_ids = [str(course.id) for course in course_runs]
            return format_html('<br>'.join(course_ids))
        return 'No courses available'


@admin.register(AvailableCourse)
class AvailableCourseAdmin(admin.ModelAdmin):
    """Admin for the AvailableCourse model."""

    list_display = ('id', 'course', 'active')
    search_fields = ('course',)
