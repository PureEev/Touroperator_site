# Generated by Django 5.0.3 on 2024-04-02 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Toursite', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='tours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='Название тура')),
                ('cities', models.CharField(max_length=100, verbose_name='Города')),
                ('duration', models.DecimalField(decimal_places=0, max_digits=2, verbose_name='Длительность тура')),
                ('image', models.ImageField(upload_to='images', verbose_name='Изображение')),
                ('price', models.DecimalField(decimal_places=0, max_digits=6, verbose_name='Цена')),
            ],
        ),
    ]
