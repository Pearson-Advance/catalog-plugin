"""Django admin pages for Catalog models."""
from django.contrib import admin

from catalog_plugin.models import AvailableCourse, Catalogue


@admin.register(AvailableCourse)
class AvailableCourseAdmin(admin.ModelAdmin):
    """Admin for the AvailableCourse model."""

    list_display = ('id', 'course', 'active')
    search_fields = ('course',)


@admin.register(Catalogue)
class CatalogueAdmin(admin.ModelAdmin):
    """Admin for the Catalogue model."""

    list_display = ('id', 'name', 'uuid')
    search_fields = ('name',)
