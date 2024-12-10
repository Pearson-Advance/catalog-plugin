"""Serializers module for API v0."""
# your_app_name/serializers.py
from rest_framework import serializers
from opaque_keys import InvalidKeyError
from opaque_keys.edx.keys import CourseKey

from catalog_plugin.models import (
    FlexibleCatalogModel,
    AvailableCourse,
    FixedCatalog,
    CatalogCourses,
)


class CourseKeySerializer(serializers.BaseSerializer):  # pylint: disable=abstract-method
    """Class that contains the course key serializer."""

    def to_representation(self, data):
        """Set the representation value of the instance."""
        return str(data)

    def to_internal_value(self, data):
        """Validate the input value."""
        try:
            return CourseKey.from_string(data)
        except InvalidKeyError:
            raise serializers.ValidationError(  # pylint: disable=raise-missing-from
                'Invalid course key: {}.'.format(data),
            )


class AvailableCourseSerializer(serializers.ModelSerializer):
    """
    Serializer for the AvailableCourse model.
    """
    course = CourseKeySerializer()

    class Meta:
        model = AvailableCourse
        fields = ['id', 'course', 'active']


class FlexibleCatalogSerializer(serializers.ModelSerializer):
    """
    Serializer for the FlexibleCatalog model.
    """
    class Meta:
        model = FlexibleCatalogModel
        fields = ['id', 'slug', 'name']


class FixedCatalogSerializer(serializers.ModelSerializer):
    """
    Serializer for the FixedCatalog model.
    """
    course_runs = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=AvailableCourse.objects.none(),
        required=False,
    )

    class Meta:
        model = FixedCatalog
        fields = ['id', 'slug', 'name', 'course_runs']


class CatalogCoursesSerializer(serializers.ModelSerializer):
    """
    Serializer for the CatalogCourses model.
    """
    courses = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=AvailableCourse.objects.all(),
    )

    class Meta:
        model = CatalogCourses
        fields = ['id', 'slug', 'name', 'courses']
