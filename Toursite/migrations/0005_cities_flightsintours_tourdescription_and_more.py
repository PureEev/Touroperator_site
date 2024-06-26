# Generated by Django 5.0.3 on 2024-04-24 15:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Toursite', '0004_tourinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_city', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='FlightsInTours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tour_number', models.CharField(max_length=100)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Toursite.cities')),
            ],
        ),
        migrations.CreateModel(
            name='TourDescription',
            fields=[
                ('tour_number', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image_number', models.CharField(max_length=100)),
                ('tour_description', models.TextField()),
            ],
        ),
        migrations.RenameModel(
            old_name='tours',
            new_name='Tour',
        ),
        migrations.DeleteModel(
            name='city',
        ),
    ]
