# Generated by Django 4.1.4 on 2022-12-14 11:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('beat', '0005_alter_beat_audio_beat_alter_beat_image_beat_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('P', 'paid'), ('W', 'Waiting'), ('C', 'Cancelled')], default='W', max_length=1)),
                ('link', models.CharField(max_length=1024)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('paid', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_code', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('sended', models.BooleanField(default=False)),
                ('recived', models.BooleanField(null=True)),
                ('report', models.CharField(blank=True, max_length=256, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('beat', models.ForeignKey(default='Not Avalible', on_delete=django.db.models.deletion.SET_DEFAULT, to='beat.beat')),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.payment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
