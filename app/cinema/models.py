from django.db import models
#from django_countries.fields import CountryField


class Festival(models.Model):
    name = models.CharField(max_length=200)
 #   month_occurence = models.DateTimeField('Periode')
  #  is_african = model.BooleanField(default=false)
   # country = CountryField()
    #current_year_date = models.DateTimeField('Current year date')
    # deadline_date
    # price
    # fee
    # has_rental_fee
    # is_competitive
    # comments
    # support
    # link



class Film(models.Model):
    name = models.CharField(max_length=200)

