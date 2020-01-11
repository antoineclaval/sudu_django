# Generated by Django 2.2.8 on 2020-01-11 04:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0006_auto_20200111_0403'),
    ]

    operations = [
        migrations.RenameField(
            model_name='submission',
            old_name='dateSent',
            new_name='date',
        ),
        migrations.CreateModel(
            name='Projection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(blank=True, null=True, verbose_name='Periode')),
                ('location', models.CharField(max_length=200)),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.Film')),
            ],
        ),
    ]
