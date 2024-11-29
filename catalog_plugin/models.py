"""Database ORM models managed by this plugin."""

import uuid

from django.db import models


class AvailableCourse(models.Model):
    """
    Represents an available course.

    Attributes:
        course (str): The name of the course.
        active (bool): Indicates whether the course is currently active.
    """

    course = models.CharField(
        max_length=255,
        verbose_name='Course',
    )
    active = models.BooleanField(default=True)

    def __str__(self):
        """Available Courses object is represented according to the course and status.

        Returns:
            str: Name of the catalogue.
        """
        return f'{self.course} - {self.active}'

class Catalogue(models.Model):
    """
    Represents a catalogue.

    Attributes:
        name (str): The name of the catalogue.
        uuid (UUIDField): A unique identifier for the catalogue.
    """

    name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Catalogue',
    )
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    courses = models.ManyToManyField(
        AvailableCourse,
        verbose_name='Available Courses',
    )

    def __str__(self):
        """Catalogue object is represented according to its name.

        Returns:
            str: Name of the catalogue.
        """
        return self.name or 'Unnamed Catalogue'
