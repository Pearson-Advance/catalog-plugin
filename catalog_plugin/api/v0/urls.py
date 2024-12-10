"""URL for the API v0."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from catalog_plugin.api.v0 import views

app_name = 'catalog_plugin.api.v0'
router = DefaultRouter()

router.register(r'flexible-catalogs', views.FlexibleCatalogViewSet, basename='flexible-catalog')
router.register(r'available-courses', views.AvailableCourseViewSet, basename='availablecourse')
router.register(r'fixed-catalogs', views.FixedCatalogViewSet, basename='fixedcatalog')
router.register(r'catalog-courses', views.CatalogCoursesViewSet, basename='catalogcourses')

urlpatterns = [
    path('', include(router.urls)),
]
