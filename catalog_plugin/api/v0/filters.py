"""Filters for the api.v0 module."""
import django_filters
from catalog_plugin.models import AvailableCourse, FixedCatalog, CatalogCourses


class AvailableCourseFilter(django_filters.FilterSet):
    """
    FilterSet for AvailableCourse model.
    Allows filtering by course ID and active status.
    """
    course_id = django_filters.CharFilter(field_name='course__id')
    active = django_filters.BooleanFilter(field_name='active')

    class Meta:
        """Meta class."""
        model = AvailableCourse
        fields = ['course_id', 'active']


class FixedCatalogFilter(django_filters.FilterSet):
    """
    FilterSet for FixedCatalog model.
    Allows filtering by name, active status, and creation date ranges.
    """
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    active = django_filters.BooleanFilter(field_name='active')
    created_after = django_filters.DateFilter(field_name='created', lookup_expr='gte')
    created_before = django_filters.DateFilter(field_name='created', lookup_expr='lte')

    class Meta:
        """Meta class."""
        model = FixedCatalog
        fields = ['name', 'active', 'created_after', 'created_before']


class CatalogCoursesFilter(django_filters.FilterSet):
    """
    FilterSet for CatalogCourses model.
    Allows filtering by name, active status, and related courses.
    """
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    active = django_filters.BooleanFilter(field_name='active')
    course_id = django_filters.CharFilter(field_name='courses__id')

    class Meta:
        """Meta class."""
        model = CatalogCourses
        fields = ['name', 'active', 'course_id']
