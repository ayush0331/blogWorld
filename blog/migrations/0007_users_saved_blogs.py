# Generated by Django 3.2.6 on 2021-08-16 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_reply'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='saved_blogs',
            field=models.ManyToManyField(to='blog.Blog'),
        ),
    ]
