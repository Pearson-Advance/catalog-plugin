"""Catalogs API client module."""
import uuid
import logging

from django.core.validators import validate_slug
from django.core.exceptions import ValidationError
from django.db.models import Q

from opaque_keys.edx.keys import CourseKey
from opaque_keys import InvalidKeyError

from catalog_plugin.edxapp_wrapper.course_module import course_overview
from catalog_plugin.models import (
    AvailableCourse,
    CatalogCourses,
    FixedCatalog,
    FlexibleCatalogModel,
)

logger = logging.getLogger(__name__)


class FlexibleCatalogAPIClient:
    """
    A Python API client for FlexibleCatalogModel to interact with flexible catalog models backend-to-backend.
    """

    def __init__(self, catalog_uuid=None, catalog_slug=None, lookup_dict=None):
        """
        Initialize the API client with a catalog UUID, catalog slug, and/or a dict that contains the lookup
        fields to be used.

        At least one of these must be provided.
        """
        if not (catalog_uuid or catalog_slug or lookup_dict):
            raise ValueError('Either catalog_uuid, catalog_slug, or lookup_dict must be provided.')

        if catalog_uuid and not isinstance(catalog_uuid, (str, uuid.UUID)):
            raise TypeError('catalog_uuid must be a string or a UUID.')
        if catalog_slug and not isinstance(catalog_slug, str):
            raise TypeError('catalog_slug must be a string.')
        if lookup_dict:
            if not isinstance(lookup_dict, dict):
                raise TypeError('lookup_dict must be a valid dictionary.')

        self.catalog_uuid = catalog_uuid
        self.catalog_slug = catalog_slug
        self.lookup_dict = lookup_dict

    def _validate_fields(self, data):
        """
        Validate and clean the input fields.

        Args:
            data (dict): A dictionary of fields to validate.

        Raises:
            ValidationError: If any field fails validation.
        """
        slug, name = data.get('slug'), data.get('name')

        if slug:
            validate_slug(slug)

        if name is not None and not isinstance(name, str):
            raise ValidationError('"name" must be a string.')

    def fetch_flexible_catalog(self):
        """
        Fetch a flexible catalog by UUID or slug.

        Returns:
            FlexibleCatalogModel or QuerySet.none(): The retrieved flexible catalog object or empty QuerySet if not found.
        """
        try:
            if self.lookup_dict:
                lookup_query = Q()
                for key, value in self.lookup_dict.items():
                    lookup_query &= Q(**{key: value})
                return FlexibleCatalogModel.objects.filter(lookup_query)
            elif self.catalog_uuid:
                return FlexibleCatalogModel.objects.get(id=self.catalog_uuid)
            elif self.catalog_slug:
                return FlexibleCatalogModel.objects.get(slug=self.catalog_slug)
        except FlexibleCatalogModel.DoesNotExist:
            logger.warning(
                'FlexibleCatalogModel not found. UUID: %s, Slug: %s, Lookup Dict: %s',
                self.catalog_uuid,
                self.catalog_slug,
                self.lookup_dict,
            )
        return FlexibleCatalogModel.objects.none()

    def get_flexible_catalog(self):
        """
        Retrieve a flexible catalog.

        Returns:
            FlexibleCatalogModel or QuerySet: The retrieved catalog or empty QuerySet if not found.
        """
        catalog = self.fetch_flexible_catalog()

        return catalog if catalog else FlexibleCatalogModel.objects.none()

    def update_flexible_catalog(self, **kwargs):
        """
        Update the fields of a flexible catalog dynamically using kwargs.

        Args:
            **kwargs: Arbitrary keyword arguments for catalog fields to update.

        Returns:
            FlexibleCatalogModel or QuerySet: The updated FlexibleCatalogModel instance or empty QuerySet if not found.
        """
        update_fields = {key: value for key, value in kwargs.items() if value is not None}

        if not update_fields:
            logger.info('No fields provided for update.')
            return FlexibleCatalogModel.objects.none()

        self._validate_fields(update_fields)

        catalog = self.fetch_flexible_catalog()

        if not catalog:
            return FlexibleCatalogModel.objects.none()

        for field, value in update_fields.items():
            setattr(catalog, field, value)

        catalog.save()

        logger.info(
            'FlexibleCatalogModel updated successfully. UUID: %s, Slug: %s',
            self.catalog_uuid,
            self.catalog_slug,
        )
        return catalog

    def delete_flexible_catalog(self):
        """
        Delete a flexible catalog by its UUID or slug.

        Returns:
            bool: True if a catalog was deleted, False otherwise.
        """
        catalog = self.fetch_flexible_catalog()
        if not catalog:
            return False

        catalog.delete()
        logger.info(
            'FlexibleCatalogModel deleted successfully. UUID: %s, Slug: %s',
            self.catalog_uuid,
            self.catalog_slug,
        )
        return True


class AvailableCourseAPIClient:
    """
    A Python API client for the AvailableCourse model to interact with flexible catalog models backend-to-backend.
    """

    def __init__(self, course_id):
        """
        Initialize the client with a course_id.

        Args:
            course_id: The ID of the course to be used by the client. Must be a CourseKey instance.

        Raises:
            TypeError: If course_id is not a CourseKey instance.
        """
        if not isinstance(course_id, CourseKey):
            raise TypeError(f'course_id must be a CourseKey instance, but got {type(course_id).__name__}.')

        self.course_id = course_id

    def get_available_course(self):
        """
        Retrieve a single available course by its course ID.

        Returns:
            AvailableCourse: The retrieved AvailableCourse instance, or QuerySet.none() if not found.
        """
        try:
            return AvailableCourse.objects.get(course__id=self.course_id)
        except AvailableCourse.DoesNotExist:
            logger.warning('AvailableCourse with course ID "%s" does not exist.', self.course_id)
        return AvailableCourse.objects.none()

    def get_all_available_courses(self):
        """
        Retrieve all available courses.

        Returns:
            QuerySet: A QuerySet containing all instances of AvailableCourse.
        """
        return AvailableCourse.objects.all()

    def create_available_course(self, active=False):
        """
        Create a new available course if it does not already exist.

        Args:
            active (bool): The active status of the new course. Defaults to False.

        Returns:
            AvailableCourse or QuerySet: The AvailableCourse instance if created or found,
            or an empty QuerySet if the course does not exist.
        """
        try:
            course = course_overview().objects.get(id=self.course_id)
            available_course, created = AvailableCourse.objects.get_or_create(
                course=course,
                defaults={'active': active},
            )
            if created:
                logger.info('Created new AvailableCourse. Course ID: %s, Active: %s', self.course_id, active)
            return available_course
        except course_overview().DoesNotExist:
            logger.warning(
                'Cannot create AvailableCourse. Course with ID "%s" does not exist.',
                self.course_id,
            )
        return AvailableCourse.objects.none()

    def update_available_course(self, active):
        """
        Update the active status of an existing available course.

        Args:
            active (bool): The new active status.

        Returns:
            AvailableCourse or QuerySet.none(): The updated AvailableCourse instance, or an empty QuerySet if not found.
        """
        available_course = self.get_available_course()

        if not available_course.exists():
            return AvailableCourse.objects.none()

        if available_course.active != active:
            available_course.active = active
            available_course.save()
            logger.info('Updated AvailableCourse active status. Course ID: %s, Active: %s', self.course_id, active)

        return available_course

    def delete_available_course(self):
        """
        Delete an available course by its course ID.

        Returns:
            bool: True if the available course was deleted, False otherwise.
        """
        available_course = self.get_available_course()

        if not available_course:
            return False

        available_course.delete()
        logger.info(
            'AvailableCourse deleted successfully. Course ID: %s',
            self.course_id,
        )
        return True


def validate_catalog_id(catalog_id):
        """
        Validate the catalog ID to ensure it is a valid UUID.

        Args:
            catalog_id (int or str): The catalog ID to validate.

        Returns:
            uuid.UUID: A valid UUID instance.

        Raises:
            ValueError: If the catalog_id is not a valid UUID.
        """
        if not isinstance(catalog_id, uuid.UUID):
            try:
                return uuid.UUID(catalog_id)
            except (ValueError, TypeError):
                raise ValueError(f'catalog_id must be a valid UUID, but got: {catalog_id}')
        return catalog_id


def validate_course_ids(course_ids):
    """
    Validate that all course IDs are of the expected type.

    Args:
        course_ids (list): A list of course IDs to validate.

    Returns:
        list: The same list of validated course IDs.

    Raises:
        TypeError: If any course ID is not of the expected type (CourseKey).
    """
    invalid_ids = tuple(course_id for course_id in course_ids if not isinstance(course_id, CourseKey))

    if invalid_ids:
        raise TypeError(
            f'All course IDs must be instances of {CourseKey.__name__}. Invalid IDs: {invalid_ids}',
        )

    return course_ids


class FixedCatalogAPIClient:
    """
    A Python API client for FixedCatalog model to interact with flexible catalog models backend-to-backend.
    """

    def __init__(self, catalog_id, course_run_ids=[]):
        """
        Initialize the client with a catalog_id and optionally validate course IDs.

        Args:
            catalog_id (int or str): The ID of the fixed catalog to operate on.
            course_run_ids (list[str], optional): A list of course run IDs to validate and use.
        """
        self.catalog_id = validate_catalog_id(catalog_id)
        self.course_run_ids = validate_course_ids(course_run_ids) if course_run_ids else []

    def get_fixed_catalog(self):
        """
        Retrieve the fixed catalog by its ID.

        Returns:
            FixedCatalog or QuerySet: The FixedCatalog instance if found,
            or an empty QuerySet if it does not exist.
        """
        try:
            return FixedCatalog.objects.get(id=self.catalog_id)
        except FixedCatalog.DoesNotExist:
            logger.warning('FixedCatalog with ID "%s" does not exist.', self.catalog_id)
        return FixedCatalog.objects.none()

    def get_all_fixed_catalogs(self):
        """
        Retrieve all fixed catalogs.

        Returns:
            QuerySet: A QuerySet containing all instances of FixedCatalog.
        """
        return FixedCatalog.objects.all()

    def add_courses_to_fixed_catalog(self, course_run_ids=[]):
        """
        Add the course runs from the provided list or the initialized list to the fixed catalog.

        This method associates the course runs, identified by their IDs, with the fixed catalog.

        Args:
            course_run_ids (list[str], optional): A list of course run IDs to add.
                If not provided, the instance's initialized list will be used.

        Returns:
            FixedCatalog or QuerySet: The updated FixedCatalog instance with the added course runs,
            or an empty QuerySet if no catalog or courses are found.
        """
        course_run_ids = validate_course_ids(course_run_ids)

        if not course_run_ids:
            logger.warning('No course run IDs were provided.')
            return FixedCatalog.objects.none()

        catalog = self.get_fixed_catalog()

        if not catalog:
            return FixedCatalog.objects.none()

        courses = course_overview().objects.filter(id__in=course_run_ids)

        if not courses.exists():
            logger.warning('No valid courses found for IDs: %s', course_run_ids)
            return FixedCatalog.objects.none()

        catalog.course_runs.add(courses)
        catalog.save()

        return catalog

    def remove_courses_from_fixed_catalog(self, course_run_ids=[]):
        """
        Remove multiple course runs from the fixed catalog.

        This method removes the course runs, identified by their IDs, from the fixed catalog.

        Args:
            course_run_ids (list[str], optional): A list of course run IDs to remove.
                If not provided, the instance's initialized list will be used.

        Returns:
            FixedCatalog or QuerySet: The updated FixedCatalog instance with the removed course runs,
            or an empty QuerySet if no catalog or courses are found.
        """
        course_run_ids = validate_course_ids(course_run_ids)

        if not course_run_ids:
            logger.warning('No course run IDs were provided.')
            return FixedCatalog.objects.none()

        catalog = self.get_fixed_catalog()

        if not catalog:
            return FixedCatalog.objects.none()

        courses = course_overview().objects.filter(id__in=course_run_ids)

        if not courses.exists():
            logger.warning('No valid courses found for IDs: %s', course_run_ids)
            return FixedCatalog.objects.none()

        catalog.course_runs.remove(courses)
        catalog.save()

        return catalog


class CatalogCoursesAPIClient:
    """
    A Python API client for CatalogCourses model to interact with flexible catalog models backend-to-backend.
    """

    def __init__(self, catalog_id, course_ids=[]):
        """
        Initialize the client with a catalog_id and optionally validate course IDs.

        Args:
            catalog_id (int or str): The ID of the CatalogCourses instance to operate on.
            course_ids (list[int], optional): A list of IDs for AvailableCourse objects to validate and use.
        """
        self.catalog_id = validate_catalog_id(catalog_id)
        self.course_ids = validate_course_ids(course_ids) if course_ids else []

    def _get_active_courses(self, course_run_ids):
        """
        Retrieve active AvailableCourse objects for the given course run IDs.

        Args:
            course_run_ids (list[CourseKey]): A list of validated course run IDs.

        Returns:
            QuerySet: A QuerySet of active AvailableCourse objects.
        """
        return AvailableCourse.objects.filter(
            course__id__in=[str(course_id) for course_id in course_run_ids],
            active=True,
        )

    def get_catalog(self):
        """
        Retrieve the CatalogCourses instance for the current catalog_id.

        Returns:
            CatalogCourses or QuerySet: The corresponding CatalogCourses instance if found,
            or an empty QuerySet if no instance is found.
        """
        try:
            return CatalogCourses.objects.get(id=self.catalog_id)
        except CatalogCourses.DoesNotExist:
            logger.warning('No CatalogCourses found with ID "%s".', self.catalog_id)
        return CatalogCourses.objects.none()

    def add_courses_to_catalog(self, course_ids=[]):
        """
        Add multiple AvailableCourse objects to the catalog.

        Args:
            course_ids (list[CourseKey], optional): A list of course IDs to add.
                If not provided, the instance's initialized list will be used.

        Returns:
            CatalogCourses or QuerySet: The updated CatalogCourses instance with the added courses,
            or an empty QuerySet if no catalog is found.
        """
        course_run_ids = course_ids or self.course_ids
        validate_course_ids(course_run_ids)

        active_courses = self._get_active_courses(course_run_ids)

        if not active_courses.exists():
            logger.warning('No active courses found for IDs: %s', course_run_ids)
            return CatalogCourses.objects.none()

        catalog = self.get_catalog()

        if not catalog:
            return CatalogCourses.objects.none()

        catalog.courses.add(active_courses)
        catalog.save()

        return catalog

    def remove_courses_from_catalog(self, course_ids=[]):
        """
        Remove multiple AvailableCourse objects from the catalog.

        Args:
            course_ids (list[CourseKey], optional): A list of course IDs to remove.
                If not provided, the instance's initialized list will be used.

        Returns:
            CatalogCourses or QuerySet: The updated CatalogCourses instance with the removed courses,
            or an empty QuerySet if no catalog is found.
        """
        course_run_ids = course_ids or self.course_ids
        validate_course_ids(course_run_ids)

        courses_to_remove = AvailableCourse.objects.filter(
            course__id__in=[str(course_id) for course_id in course_run_ids],
        )

        if not courses_to_remove.exists():
            logger.warning('No valid courses found for IDs: %s', course_run_ids)
            return CatalogCourses.objects.none()

        catalog = self.get_catalog()

        if not catalog:
            return CatalogCourses.objects.none()

        catalog.courses.remove(courses_to_remove)
        catalog.save()

        return catalog
