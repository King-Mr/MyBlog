# Generated by Django 3.1.4 on 2021-01-20 05:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0008_auto_20210119_1735'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='tag',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
