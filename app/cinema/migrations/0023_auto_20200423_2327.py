# Generated by Django 2.2.10 on 2020-04-23 23:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0022_auto_20200421_2330'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maintenance_mode', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Site Configuration',
            },
        ),
        migrations.AlterField(
            model_name='submission',
            name='dateSubmission',
            field=models.DateField(null=datetime.datetime(2020, 4, 23, 23, 27, 55, 803771), verbose_name='Submission Date'),
        ),
    ]
