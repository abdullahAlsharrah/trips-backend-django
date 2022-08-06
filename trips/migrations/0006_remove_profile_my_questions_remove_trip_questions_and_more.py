# Generated by Django 4.0.6 on 2022-08-05 23:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0005_question_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='my_questions',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='questions',
        ),
        migrations.AddField(
            model_name='question',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='trips.profile'),
        ),
        migrations.AddField(
            model_name='question',
            name='trip',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='trips.trip'),
        ),
    ]
