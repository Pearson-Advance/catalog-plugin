"""Serializers module for API v0."""
# your_app_name/serializers.py
from opaque_keys import InvalidKeyError
from opaque_keys.edx.keys import CourseKey
from rest_framework import serializers

from catalog_plugin.models import AvailableCourse, CatalogCourses, FixedCatalog, FlexibleCatalogModel


class CourseKeySerializer(serializers.BaseSerializer):  # pylint: disable=abstract-method
    """Class that contains the course key serializer."""

    def to_representation(self, instance):
        """Set the representation value of the instance."""
        return str(instance)

    def to_internal_value(self, data):
        """Validate the input value."""
        try:
            return CourseKey.from_string(data)
        except InvalidKeyError as exc:
            raise serializers.ValidationError(f'Invalid course key: {data}.') from exc


class AvailableCourseSerializer(serializers.ModelSerializer):
    """Serializer for the AvailableCourse model."""

    course = CourseKeySerializer()

    class Meta:
        """Meta class."""

        model = AvailableCourse
        fields = ['id', 'course', 'active']


class FlexibleCatalogSerializer(serializers.ModelSerializer):
    """Serializer for the FlexibleCatalog model."""

    class Meta:
        """Meta class."""

        model = FlexibleCatalogModel
        fields = ['id', 'slug', 'name']


class FixedCatalogSerializer(serializers.ModelSerializer):
    """Serializer for the FixedCatalog model."""

    course_runs = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=AvailableCourse.objects.none(),
        required=False,
    )

    class Meta:
        """Meta class."""

        model = FixedCatalog
        fields = ['id', 'slug', 'name', 'course_runs']


class CatalogCoursesSerializer(serializers.ModelSerializer):
    """Serializer for the CatalogCourses model."""

    courses = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=AvailableCourse.objects.all(),
    )

    class Meta:
        """Meta class."""

        model = CatalogCourses
        fields = ['id', 'slug', 'name', 'courses']
