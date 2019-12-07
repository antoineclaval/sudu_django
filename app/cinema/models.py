from django.db import models
from django_countries.fields import CountryField


class Festival(models.Model):
    name = models.CharField(max_length=200)
    month_occurence = models.DateTimeField('Periode',blank=True, null=True)
    is_african = models.BooleanField(default=False)
    country = CountryField(blank=False, null=False, default="FR")
    current_year_date = models.DateTimeField('Current year date', blank=True, null=True)
    deadline_date = models.DateTimeField('Deadline', blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    #fee = models.DecimalField()
    has_rental_fee = models.BooleanField(default=False)
    is_competitive = models.BooleanField(default=False)
    comments = models.CharField(max_length=500, blank=True, null=True)
    support = models.CharField(max_length=200, blank=True, null=True)
    link = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
    	return self.name



class Film(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
    	return self.name

