# Generated by Django 4.0.6 on 2022-08-04 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='favorite',
            field=models.ManyToManyField(blank=True, default=None, related_name='favorites', to='trips.profile'),
        ),
    ]
