# Generated by Django 3.2.6 on 2021-08-16 01:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_users_saved_blogs'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Reactions',
        ),
    ]
