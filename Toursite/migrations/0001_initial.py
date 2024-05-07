# Generated by Django 5.0.3 on 2024-04-02 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='city',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='Город')),
                ('description', models.TextField(verbose_name='Описание')),
                ('image', models.ImageField(upload_to='images', verbose_name='Изображение')),
                ('price', models.DecimalField(decimal_places=0, max_digits=6, verbose_name='Цена')),
                ('type', models.CharField(choices=[('MO', 'Понедельник'), ('TU', 'Вторник'), ('WE', 'Среда'), ('TH', 'Четверг'), ('FR', 'Пятница'), ('SA', 'Суббота'), ('SU', 'Воскресенье')], default='Понедельник', max_length=2, verbose_name='День недели')),
            ],
        ),
    ]
