# Generated by Django 4.1.3 on 2022-11-01 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_weather_min_temp'),
    ]

    operations = [
        migrations.CreateModel(
            name='Corn_grain_yield',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(max_length=7)),
                ('harvested', models.BigIntegerField()),
            ],
        ),
    ]