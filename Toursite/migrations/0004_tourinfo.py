# Generated by Django 5.0.3 on 2024-04-09 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Toursite', '0003_ticket_weeklyschedule'),
    ]

    operations = [
        migrations.CreateModel(
            name='TourInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input1', models.CharField(max_length=100)),
                ('input2', models.CharField(max_length=100)),
                ('input3', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'tour_description',
                'managed': False,
            },
        ),
    ]
