# Generated by Django 5.0.3 on 2024-04-24 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Toursite', '0006_сities_remove_flightsintours_city_delete_cities_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='сities',
            new_name='City',
        ),
    ]
