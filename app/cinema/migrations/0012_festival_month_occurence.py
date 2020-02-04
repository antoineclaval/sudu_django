# Generated by Django 2.2.9 on 2020-02-04 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0011_remove_festival_month_occurence'),
    ]

    operations = [
        migrations.AddField(
            model_name='festival',
            name='month_occurence',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], null=True),
        ),
    ]