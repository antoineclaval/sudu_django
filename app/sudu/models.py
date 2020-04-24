from django.db import models
from django_countries import Countries


from django.utils.translation import gettext_lazy as _
from solo.models import SingletonModel


class G8Countries(Countries):
    override = [
        ('EU', _('European Union'))
    ]


class Language(models.Model):
    '''
    List of languages by iso code (2 letter only because country code
    is not needed.
    This should be popluated by getting data from django.conf.locale.LANG_INFO
    '''
    name = models.CharField(max_length=256,
                            null=False,
                            blank=False,
                            verbose_name='Language name'
                            )
    name_local = models.CharField(max_length=256,
                                null=False,
                                blank=True,
                                default='',
                                verbose_name='Language name (in that language)')
    isocode = models.CharField(max_length=2,
                            null=False,
                            blank=False,
                            unique=True,
                            verbose_name='ISO 639-1 Language code',
                            help_text='2 character language code without country'
                            )
    sorting = models.PositiveIntegerField(blank=False,
                                        null=False,
                                        default=0,
                                        verbose_name='sorting order',
                                        help_text='increase to show at top of the list')


def __str__(self):
    return '%s (%s)' % (self.name, self.name_local)


class Meta:
    verbose_name = 'language'
    verbose_name_plural = 'languages'
    ordering = '-sorting', 'name', 'isocode', 
