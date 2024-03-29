# Generated by Django 4.0.6 on 2022-07-22 19:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_auto_20220720_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='Оценка'),
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.PositiveSmallIntegerField(help_text='Use the following format: <YYYY>', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2022)], verbose_name='Год издания'),
        ),
    ]
