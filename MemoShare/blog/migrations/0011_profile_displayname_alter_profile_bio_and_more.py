# Generated by Django 4.1.7 on 2023-05-25 13:43

from django.db import migrations, models
import django_google_maps.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_post_geolocation_alter_post_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='displayname',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=django_google_maps.fields.AddressField(blank=True, max_length=200, null=True),
        ),
    ]