from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from imagekit.admin import AdminThumbnail
from admin_auto_filters.filters import AutocompleteFilter
from django_countries.filters import CountryFilter

from .models import Festival
from .models import Film
from .models import Submission
from .models import Projection
from .models import Event
from .models import SiteConfiguration

from solo.admin import SingletonModelAdmin

admin.site.register(SiteConfiguration, SingletonModelAdmin)

class FestivalAdmin(ImportExportModelAdmin):
    search_fields = ['name', 'country', 'month_occurence', 'inscriptions__name']
    list_display = ['name', 'month_occurence','current_year_date','deadline_date', 'is_african', 'country', 'isCompetitive', 'has_rental_fee', 'price', 'presenceType', 'isRescheduled', 'rescheduledDate']
    list_filter = ('month_occurence',
    ('is_african', admin.BooleanFieldListFilter),
    'country',
    'presenceType',
    'month_occurence',
    'inscriptions__name')

class FilmAdmin(ImportExportModelAdmin):
    search_fields = ['name', 'director']
    list_display = ['name', 'country', 'director', 'productionYear','image_display', 'filmType']
    image_display = AdminThumbnail(image_field='poster')
    image_display.short_description = 'Image'
    list_filter = ('productionYear', 'filmType',
                  ('country')
                  )


    readonly_fields = ['image_display']  # this is for the change form

class FestivalFilter(AutocompleteFilter):
    title = 'Festival' # display title
    field_name = 'festival' # name of the foreign key field

class FilmFilter(AutocompleteFilter):
    title = 'Film' # display title
    field_name = 'film' # name of the foreign key field

class SubmissionAdmin(ImportExportModelAdmin):
    model = Submission
    search_fields = ['film__name', 'festival__name', 'response', 'responseDate', 'dateSubmission']
    list_display = ['festival', 'film', 'dateSubmission', 'response', 'responseDate', 'get_isCompetitive', 'get_country', 'get_month_occurence']
    #list_filter = [FestivalFilter, FilmFilter]
    list_filter = ('dateSubmission','response', 'responseDate')
    autocomplete_fields = ['festival', 'film']
    class Media:
        pass

    def get_isCompetitive(self, obj):
        return obj.festival.isCompetitive
    get_isCompetitive.admin_order_field  = 'festival__isCompetitive'  
    get_isCompetitive.short_description = 'Competitive' 

    def get_country(self, obj):
        return obj.festival.country
    get_country.admin_order_field  = 'festival__country'  
    get_country.short_description = 'Country' 

    def get_month_occurence(self, obj):
        return obj.festival.month_occurence
    get_month_occurence.admin_order_field  = 'festival__month_occurence'  
    get_month_occurence.short_description = 'Month Festival' 

class ProjectionAdmin(admin.ModelAdmin):
    search_fields = ['location', 'film__name']
    list_display = [ 'get_films', 'get_month','location', 'country', 'festival', 'event', 'date', 'dateStartPeriod', 'dateEndPeriod', 'supportChoices', 'quotedPrice', 'quoteSent', 'billSent', 'mediaSent', 'paymentReceived', 'socialMediaNotified', 'isCancel', 'isRescheduled', 'rescheduledDate']

class EventAdmin(admin.ModelAdmin):
    search_fields = ['structure', 'name']
    list_display = [ 'structure', 'name', 'deadlineMediaReception']

admin.site.register(Festival, FestivalAdmin)
admin.site.register(Film, FilmAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Projection, ProjectionAdmin)
admin.site.register(Event, EventAdmin)
