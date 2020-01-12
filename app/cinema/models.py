from django.db import models
from django_countries.fields import CountryField
from enum import Enum 
import datetime

class Festival(models.Model):
    name = models.CharField(max_length=200)
    month_occurence = models.DateTimeField('Periode', blank=True, null=True)
    is_african = models.BooleanField(default=False)
    country = CountryField(blank=False, null=False, default="FR")
    current_year_date = models.DateTimeField('Current year date', blank=True, null=True)
    deadline_date = models.DateTimeField('Deadline', blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    # fee = models.DecimalField()
    has_rental_fee = models.BooleanField(default=False)
    is_competitive = models.BooleanField(default=False)
    comments = models.CharField(max_length=500, blank=True, null=True)
    support = models.CharField(max_length=200, blank=True, null=True)
    link = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

class FilmTypeChoice(Enum):  
    DOC = "Documentaire"
    FICTION = "Fiction"
    COURT = "Court-Métrage"

YEAR_CHOICES = []
for r in range(1980, (datetime.datetime.now().year+1)):
    YEAR_CHOICES.append((r,r))

class Film(models.Model):
    name = models.CharField(max_length=200)
    poster = models.ImageField(null=True, blank=True, upload_to="poster")
    country = CountryField(blank=False, null=False, default="FR")
    director = models.CharField(max_length=80, null=False, blank=False, default="Unknow")
    #filmType = models.CharField( default=FilmTypeChoice.FICTION , max_length=20, choices=[(tag, tag.value) for tag in FilmTypeChoice])  # Choices is a list of Tuple
    productionYear = models.IntegerField(choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    description = models.TextField(null=True, blank=True)
    # langue
    # Palmares
    # 	..
    # Projection
    # 	 date
    # 	 Lieux
    def __str__(self):
        return self.name

class Submission(models.Model):
    date = models.DateTimeField('Periode', blank=True, null=True)
    film = models.ForeignKey(Film, on_delete=models.CASCADE) 
    festival = models.ForeignKey(Festival, on_delete=models.CASCADE) 
    #Many to One Response
    def __str__(self):
        return '{} / {}'.format(self.film.name,self.festival.name) 

# Response 
#     Date
#     Yes/No

class Projection(models.Model): 
    date = models.DateTimeField('Periode', blank=True, null=True)
    location = models.CharField(max_length=200)
    film = models.ForeignKey(Film, on_delete=models.CASCADE) 
    def __str__(self):
        return self.location
        
# Award

