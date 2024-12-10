"""Views module for API v0."""
from edx_rest_framework_extensions.auth.jwt.authentication import JwtAuthentication
from edx_rest_framework_extensions.permissions import IsAuthenticated, IsStaff
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from catalog_plugin.models import (
    FlexibleCatalogModel,
    AvailableCourse,
    FixedCatalog,
    CatalogCourses,
)
from catalog_plugin.api.v0.serializers import (
    FlexibleCatalogSerializer,
    AvailableCourseSerializer,
    FixedCatalogSerializer,
    CatalogCoursesSerializer,
)
from catalog_plugin.api.v0.filters import (
    FlexibleCatalogFilter,
    AvailableCourseFilter,
    FixedCatalogFilter,
    CatalogCoursesFilter,
)


class AvailableCourseViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing AvailableCourse instances.
    """

    authentication_classes = (JwtAuthentication,)
    permission_classes = (IsAuthenticated, IsStaff)
    queryset = AvailableCourse.objects.all()
    serializer_class = AvailableCourseSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AvailableCourseFilter
    search_fields = ['course__name']
    ordering_fields = ['course', 'active', 'id']
    ordering = ['id']


class FlexibleCatalogViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing FlexibleCatalogModel instances.
    """

    authentication_classes = (JwtAuthentication,)
    permission_classes = (IsAuthenticated, IsStaff)
    queryset = FlexibleCatalogModel.objects.all()
    serializer_class = FlexibleCatalogSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = FlexibleCatalogFilter
    search_fields = ['name', 'slug']
    ordering_fields = ['name', 'slug', 'id']
    ordering = ['name']


class FixedCatalogViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing FixedCatalog instances.
    """

    authentication_classes = (JwtAuthentication,)
    permission_classes = (IsAuthenticated, IsStaff)
    queryset = FixedCatalog.objects.all()
    serializer_class = FixedCatalogSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = FixedCatalogFilter
    search_fields = ['name']
    ordering_fields = ['name', 'created', 'modified', 'id']
    ordering = ['created']


class CatalogCoursesViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing CatalogCourses instances.
    """

    authentication_classes = (JwtAuthentication,)
    permission_classes = (IsAuthenticated, IsStaff)
    queryset = CatalogCourses.objects.all()
    serializer_class = CatalogCoursesSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CatalogCoursesFilter
    search_fields = ['name', 'courses__course__name']
    ordering_fields = ['name', 'created', 'modified', 'id']
    ordering = ['name']
