# Generated by Django 4.0.6 on 2022-08-04 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0007_alter_profile_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='', upload_to='profile/'),
        ),
    ]