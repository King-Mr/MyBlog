# Generated by Django 3.1.4 on 2021-01-15 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0004_post_content_html'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='color',
            field=models.CharField(default='#000000', max_length=10, verbose_name='颜色'),
        ),
    ]