"""Serializers module for API v0."""
from rest_framework import serializers
from opaque_keys import InvalidKeyError
from catalog_plugin.edxapp_wrapper.course_module import course_overview
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
            return course_overview().objects.get(id=data)
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
    courses = serializers.SerializerMethodField()

    class Meta:
        model = FlexibleCatalogModel
        fields = '__all__'

    def get_courses(self, obj):
        """Return courses serialized with the correct serializer."""
        obj = FlexibleCatalogModel.objects.get_subclass(id=obj.id)

        courses = obj.get_courses()
        if not courses:
            return []

        serializer_mapping = {
            FixedCatalog: CourseKeySerializer,
            CatalogCourses: AvailableCourseSerializer,
        }

        serializer_class = serializer_mapping.get(type(obj))

        if not serializer_class:
            return []

        return serializer_class(courses, many=True).data


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
