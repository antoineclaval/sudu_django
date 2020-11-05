import os 
from django.db import models
from django_countries.fields import CountryField
from django_countries import Countries

from enum import Enum 
from django.utils.dates import MONTHS
import datetime

from django.utils.translation import gettext_lazy as _
from solo.models import SingletonModel

from django.conf import settings
from django.core.files.storage import FileSystemStorage


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


class SiteConfiguration(SingletonModel):
    maintenance_mode = models.BooleanField(default=False)

    def lang_path_fr(self, filename):
        return 'reportTemplate/template-fr.docx'

    def lang_path_en(self, filename):
        return 'reportTemplate/template-en.docx'

    def __unicode__(self):
        return u"Reports Configuration"

    class Meta:
        verbose_name = "Reports Configuration"
    
    frenchTemplate = models.FileField(null=True, blank=True, upload_to=lang_path_fr, storage=OverwriteStorage())
    englishTemplate = models.FileField(null=True, blank=True, upload_to=lang_path_en, storage=OverwriteStorage())


class G8Countries(Countries):
    override = [
        ('AN', _('Antilles')),
        ('KO', _('Kosovo')),
        ('RA', _('Republique d\'Abhkazia')),
        ('WL', _('Wales')),
    ]


OCCURENCE_CHOICES = { 111: _('Year Round')}
OCCURENCE_CHOICES.update(MONTHS)


class Festival(models.Model):
    name = models.CharField(max_length=200)
    # https://dustindavis.me/django-month_choices/
    month_occurence = models.PositiveSmallIntegerField(choices=OCCURENCE_CHOICES.items(), null=True, blank=True)
    is_african = models.BooleanField(default=False)
    country = CountryField(blank=False, null=False, countries=G8Countries)
    current_year_date = models.CharField(max_length=50, blank=True, null=True) # too fuzzy for date as of now
    deadline_date = models.CharField(max_length=50, blank=True, null=True) # too fuzzy for date as of now
    price = models.CharField(max_length=100, blank=True, null=True)
    # fee = models.DecimalField()
    has_rental_fee = models.BooleanField(default=False)
    is_competitive = models.BooleanField(default=False)
    comments = models.CharField(max_length=500, blank=True, null=True)
    support = models.CharField(max_length=600, blank=True, null=True)
    link = models.CharField(max_length=200, blank=True, null=True)
    # models.ManyToManyField('Topping', through='ToppingAmount', related_name='pizzas'
    inscriptions = models.ManyToManyField('Film', through="Submission", related_name='festivals') 
    # Location YES?NO

    def __str__(self):
        return self.name


class FilmTypeChoice(Enum):  
    DOC = "Documentaire"
    FICTION = "Fiction"
    COURT = "Court-Métrage"


YEAR_CHOICES = []
for r in range(2000, (datetime.datetime.now().year+1)):
    YEAR_CHOICES.append((r,r))


class Film(models.Model):
    name = models.CharField(max_length=200)
    poster = models.ImageField(null=True, blank=True, upload_to="poster")
    country = CountryField(blank=False, null=False, default="FR")
    director = models.CharField(max_length=80, null=False, blank=False, default="Unknow")
    productionYear = models.IntegerField(choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    description = models.TextField(null=True, blank=True)
        
    def __str__(self):
        return self.name
    #filmType = models.CharField( default=FilmTypeChoice.FICTION , max_length=20, choices=[(tag, tag.value) for tag in FilmTypeChoice])  # Choices is a list of Tuple
    # langue
    # Palmares
    # 	..
    # Projection
    # 	 date
    # 	 Lieux


class ResponseChoice(Enum):  
    SELECTIONED = "Selectionned"
    REFUSED = "Refused"
    NO_RESPONSE = "No response yet"


MY_CHOICES = [('SELECTIONED', 'Selectionned'), ('REFUSED', 'Refused'), ('NO_RESPONSE','No response yet')]


class Submission(models.Model):
    dateSubmission = models.DateField('Submission Date', blank=False, null=datetime.datetime.now)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    # https://www.revsys.com/tidbits/tips-using-djangos-manytomanyfield/
    # pizza = models.ForeignKey('Pizza', related_name='topping_amounts', on_delete=models.SET_NULL, null=True)
    # topping = models.ForeignKey('Topping', related_name='topping_amounts', on_delete=models.SET_NULL, null=True, blank=True)

    festival = models.ForeignKey(Festival, on_delete=models.CASCADE) 
    response = models.CharField( default='NO_RESPONSE' , max_length=30, choices=MY_CHOICES)  
    responseDate = models.DateField('Response Date', blank=True, null=True)

    def __str__(self):
        return '{} / {}'.format(self.film.name, self.festival.name) 


class Projection(models.Model): 
    date = models.DateField('Periode', blank=True, null=True)
    location = models.CharField(max_length=200)
    film = models.ForeignKey(Film, on_delete=models.CASCADE) 
    
    def __str__(self):
        return self.location
# Award
