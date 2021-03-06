# Generated by Django 2.2.10 on 2020-11-06 04:14

import cinema.models
import datetime
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Festival',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('month_occurence', models.PositiveSmallIntegerField(blank=True, choices=[(111, 'Year Round'), (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], null=True)),
                ('is_african', models.BooleanField(default=False)),
                ('country', django_countries.fields.CountryField(countries=cinema.models.G8Countries, max_length=2)),
                ('current_year_date', models.CharField(blank=True, max_length=50, null=True)),
                ('deadline_date', models.CharField(blank=True, max_length=50, null=True)),
                ('price', models.CharField(blank=True, max_length=100, null=True)),
                ('has_rental_fee', models.BooleanField(default=False)),
                ('isCompetitive', models.BooleanField(default=False)),
                ('comments', models.CharField(blank=True, max_length=500, null=True)),
                ('support', models.CharField(blank=True, max_length=600, null=True)),
                ('link', models.CharField(blank=True, max_length=200, null=True)),
                ('presenceType', models.CharField(choices=[('ONLINE', 'On-line'), ('PHYSICAL', 'Physique'), ('BOTH', 'Online+Physique')], default='PHYSICAL', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('poster', models.ImageField(blank=True, null=True, upload_to='poster')),
                ('country', django_countries.fields.CountryField(default='FR', max_length=2)),
                ('director', models.CharField(default='Unknow', max_length=80)),
                ('productionYear', models.IntegerField(choices=[(2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020)], default=2020)),
                ('description', models.TextField(blank=True, null=True)),
                ('filmType', models.CharField(choices=[('DOCU', 'Documentaire'), ('FICTION', 'Fiction'), ('SHORT', 'Court-Métrage')], default='FICTION', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='SiteConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maintenance_mode', models.BooleanField(default=False)),
                ('frenchTemplate', models.FileField(blank=True, null=True, storage=cinema.models.OverwriteStorage(), upload_to=cinema.models.SiteConfiguration.lang_path_fr)),
                ('englishTemplate', models.FileField(blank=True, null=True, storage=cinema.models.OverwriteStorage(), upload_to=cinema.models.SiteConfiguration.lang_path_en)),
            ],
            options={
                'verbose_name': 'Reports Configuration',
            },
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateSubmission', models.DateField(null=datetime.datetime.now, verbose_name='Submission Date')),
                ('response', models.CharField(choices=[('SELECTIONED', 'Selectionned'), ('REFUSED', 'Refused'), ('NO_RESPONSE', 'No response yet')], default='NO_RESPONSE', max_length=30)),
                ('responseDate', models.DateField(blank=True, null=True, verbose_name='Response Date')),
                ('festival', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.Festival')),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.Film')),
            ],
        ),
        migrations.CreateModel(
            name='Projection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Periode')),
                ('location', models.CharField(max_length=200)),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.Film')),
            ],
        ),
        migrations.AddField(
            model_name='festival',
            name='inscriptions',
            field=models.ManyToManyField(related_name='festivals', through='cinema.Submission', to='cinema.Film'),
        ),
    ]
