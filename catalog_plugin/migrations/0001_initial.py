# Generated by Django 3.2.17 on 2024-12-05 22:24

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):
    """
    Initial migration for the catalog plugin.
    Creates five models:
    - `FlexibleCatalogModel`: Represents Base Catalog.
    - `DynamicCatalog`: Represents Dynamic Catalog.
    - `AvailableCourse`: Represents available courses.
    - `FixedCatalog`: Represents custom catalog with course overview courses.
    - `CatalogCourses`: Represents a collection of available courses.
    """

    initial = True

    dependencies = [
        ('course_overviews', '0026_courseoverview_entrance_exam'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlexibleCatalogModel',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('name', models.CharField(help_text='Human friendly', max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DynamicCatalog',
            fields=[
                ('flexiblecatalogmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='catalog_plugin.flexiblecatalogmodel')),
                ('query_string', models.TextField(blank=True, help_text='Dynamic query string to filter courses.', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('catalog_plugin.flexiblecatalogmodel',),
        ),
        migrations.CreateModel(
            name='AvailableCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course_overviews.courseoverview')),
            ],
        ),
        migrations.CreateModel(
            name='FixedCatalog',
            fields=[
                ('flexiblecatalogmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='catalog_plugin.flexiblecatalogmodel')),
                ('course_runs', models.ManyToManyField(blank=True, to='course_overviews.CourseOverview')),
            ],
            options={
                'abstract': False,
            },
            bases=('catalog_plugin.flexiblecatalogmodel',),
        ),
        migrations.CreateModel(
            name='CatalogCourses',
            fields=[
                ('flexiblecatalogmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='catalog_plugin.flexiblecatalogmodel')),
                ('courses', models.ManyToManyField(to='catalog_plugin.AvailableCourse', verbose_name='Available Courses')),
            ],
            options={
                'abstract': False,
            },
            bases=('catalog_plugin.flexiblecatalogmodel',),
        ),
    ]
