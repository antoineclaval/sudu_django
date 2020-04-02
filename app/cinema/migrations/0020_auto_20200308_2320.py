# Generated by Django 2.2.9 on 2020-03-08 23:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0019_auto_20200308_2319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='festival',
            name='price',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='submission',
            name='dateSubmission',
            field=models.DateField(null=datetime.datetime(2020, 3, 8, 23, 20, 57, 713049), verbose_name='Submission Date'),
        ),
    ]