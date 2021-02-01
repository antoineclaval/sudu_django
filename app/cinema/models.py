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
from django.core.exceptions import ValidationError



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

PRESENCE_CHOICES = [('ONLINE', 'On-line'), ('PHYSICAL', 'Physique'), ('BOTH','Online+Physique')]
class Festival(models.Model):
    class Meta:
        ordering = ['name']
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
    isCompetitive = models.BooleanField(default=False)
    isRescheduled = models.BooleanField('is rescheduled', default=False)
    rescheduledDate = models.DateField('Rescheduled Date', blank=True, null=True)
    comments = models.CharField(max_length=500, blank=True, null=True)
    support = models.CharField(max_length=600, blank=True, null=True)
    link = models.CharField(max_length=200, blank=True, null=True)
    presenceType = models.CharField('In person/remote', default='PHYSICAL' , max_length=20, choices=PRESENCE_CHOICES)  
    # https://www.revsys.com/tidbits/tips-using-djangos-manytomanyfield/
    inscriptions = models.ManyToManyField('Film', through="Submission", related_name='festivals') 

    def __str__(self):
        return self.name

class Film(models.Model):
    class Meta:
        ordering = ['name']

    FILM_TYPE_CHOICES = [('DOCU', 'Documentaire'), ('FICTION', 'Fiction'), ('SHORT','Court-Métrage'), ('XP','Experimental')]
    YEAR_CHOICES = []
    for r in range(2010, (datetime.datetime.now().year+1)):
        YEAR_CHOICES.append((r,r))

    name = models.CharField('Film title',max_length=200)
    poster = models.ImageField(null=True, blank=True, upload_to="poster")
    country = CountryField(blank=False, null=False, default="FR")
    director = models.CharField(max_length=80, null=False, blank=False, default="Unknow")
    productionYear = models.IntegerField('Production Year',choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    description = models.TextField(null=True, blank=True)
        
    def __str__(self):
        return self.name
    filmType = models.CharField(default='FICTION' , max_length=20, choices=FILM_TYPE_CHOICES)  
    # langue
    # Palmares


MY_CHOICES = [('SELECTIONED', 'Selectionned'), ('REFUSED', 'Refused'), ('NO_RESPONSE','No response yet')]
class Submission(models.Model):
    dateSubmission = models.DateField('Inscription Date', blank=False, null=datetime.datetime.now)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    festival = models.ForeignKey(Festival, on_delete=models.CASCADE) 
    isCompetitive = models.BooleanField('is Part of festival competitive selection?',default=False, blank=False)
    response = models.CharField( default='NO_RESPONSE' , max_length=30, choices=MY_CHOICES)  
    responseDate = models.DateField('Response Date', blank=True, null=True)
    def __str__(self):
        return '{} / {}'.format(self.film.name, self.festival.name) 
    def clean(self):
        if self.responseDate is not None and self.response == 'NO_RESPONSE':
            raise ValidationError("Specify what is the response. Selectioned or Refused? ")    


class Event(models.Model): 
    structure = models.CharField('Structure', max_length=100)
    name = models.CharField('Event name', max_length=100)
    deadlineMediaReception = models.DateField('Media reception date', blank=True, null=True)
    def __str__(self):
        return self.structure + ' - ' + self.name

class Projection(models.Model): 
    SUPPORT_CHOICES = [('HDFTP', 'HD FTP'), ('DD', 'DD'), ('NAS','Nas'), ('DCP DD','DCP DD'), ( 'SMASH', 'Smash'), ('DVD', 'DVD'), ('.MOV', '.MOV'), ('BLURAY', 'Blu-ray')]
    location = models.CharField('City', max_length=200)
    country = CountryField(blank=False, null=False, default="FR")

    films = models.ManyToManyField('Film') 

    festival = models.ForeignKey(Festival, on_delete=models.CASCADE, blank=True, null=True) 
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, null=True) 
    
    date = models.DateField('Projection Date', blank=True, null=True)
    dateStartPeriod = models.DateField('Start period', blank=True, null=True)
    dateEndPeriod = models.DateField('End period', blank=True, null=True)

    presenceType = models.CharField('In person/remote', default='PHYSICAL' , max_length=20, choices=PRESENCE_CHOICES)  
    supportChoices = models.CharField('Projection support', default='HDFTP' , max_length=20, choices=SUPPORT_CHOICES) 
    
    quotedPrice = models.CharField('Quoted price', max_length=10, blank=True, null=True)
    quoteSent = models.BooleanField('Quote sent', default=False)
    billSent = models.BooleanField('Bill sent', default=False)
    mediaSent = models.BooleanField('Media sent', default=False)
    paymentReceived = models.BooleanField('Payment received', default=False)
    socialMediaNotified = models.BooleanField('Social media notified', default=False)
    isCancel = models.BooleanField('Cancel', default=False)
    isRescheduled = models.BooleanField('is rescheduled', default=False)
    rescheduledDate = models.DateField('Rescheduled Date', blank=True, null=True)
    
    def clean(self):
        if self.festival is None and self.event is None:
            raise ValidationError("Specify a event or a festival.")
        if self.dateStartPeriod is None and self.dateEndPeriod is None and self.date is None:
            raise ValidationError("Specify a projection date, or start period and end period.") 
        if self.date is not None:
            if ( self.dateStartPeriod is not None or self.dateEndPeriod is not None):
                raise ValidationError("if you specify a projection date, you cannot specify a start period or end period.") 
        else:
            if ( self.dateStartPeriod is None or self.dateEndPeriod is None):
                raise ValidationError("Specify both start period and end period.") 
        if self.dateStartPeriod is not None and self.dateEndPeriod is not None and self.dateStartPeriod > self.dateEndPeriod:
            raise ValidationError("Start date after end date in the date-range.")    
        if self.quoteSent and self.quotedPrice is None:
            raise ValidationError("If the quote is sent, specify a quoted price.")    

    def get_films(self):
        return " -- ".join([p.name for p in self.films.all()])    
    def get_month(self):
        if self.date is not None:
            return self.date.strftime('%B')
        else:
            return self.dateStartPeriod.strftime('%B')



    def __str__(self):
        return self.location