# Generated by Django 4.1.4 on 2022-12-27 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_joined'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='ip_register',
            field=models.CharField(default='0.0.0.0', max_length=20),
        ),
    ]
