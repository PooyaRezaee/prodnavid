# Generated by Django 4.1.4 on 2022-12-12 17:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('PanelNavid', '0004_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
