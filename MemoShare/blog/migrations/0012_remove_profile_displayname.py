# Generated by Django 4.1.7 on 2023-05-25 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_profile_displayname_alter_profile_bio_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='displayname',
        ),
    ]