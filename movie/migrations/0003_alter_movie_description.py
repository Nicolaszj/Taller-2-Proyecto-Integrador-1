# Generated by Django 5.1.5 on 2025-03-02 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0002_movie_genre_movie_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='description',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
