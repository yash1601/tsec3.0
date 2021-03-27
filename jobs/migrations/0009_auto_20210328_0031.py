# Generated by Django 3.1.7 on 2021-03-27 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0008_auto_20210327_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='url',
            field=models.URLField(unique=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='url',
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name='question',
            name='url',
            field=models.URLField(unique=True),
        ),
    ]
