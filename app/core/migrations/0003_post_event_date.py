# Generated by Django 4.1.6 on 2023-02-14 13:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_story_options_advice_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='event_date',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]
