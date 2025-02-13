# Generated by Django 4.2.6 on 2023-10-20 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WeatherCache',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('condition', models.CharField(blank=True, choices=[('clear sky', 'Clear sky'), ('few clouds', 'Few clouds'), ('scattered clouds', 'Scattered clouds'), ('broken clouds', 'Broken clouds'), ('shower rain', 'Shower rain'), ('rain', 'Rain'), ('thunderstorm', 'Thunderstorm'), ('snow', 'Snow'), ('mist', 'Mist')], max_length=20, null=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('temperature', models.FloatField(blank=True, null=True)),
                ('feels_like', models.FloatField(blank=True, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('icon', models.URLField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'unique_together': {('latitude', 'longitude')},
            },
        ),
    ]
