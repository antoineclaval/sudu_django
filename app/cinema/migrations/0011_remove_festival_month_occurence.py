# Generated by Django 2.2.9 on 2020-02-04 03:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0010_auto_20200204_0321'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='festival',
            name='month_occurence',
        ),
    ]
