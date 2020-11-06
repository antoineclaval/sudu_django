from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from imagekit.admin import AdminThumbnail
from admin_auto_filters.filters import AutocompleteFilter
from django_countries.filters import CountryFilter

from .models import Festival
from .models import Film
from .models import Submission
from .models import Projection
from .models import SiteConfiguration

from solo.admin import SingletonModelAdmin

admin.site.register(SiteConfiguration, SingletonModelAdmin)

class FestivalAdmin(ImportExportModelAdmin):
    search_fields = ['name', 'country', 'month_occurence']
    list_display = ['name', 'month_occurence','current_year_date','deadline_date', 'is_african', 'country', 'has_rental_fee', 'price']
    list_filter = ('month_occurence',
    ('is_african', admin.BooleanFieldListFilter),
    'country')

class FilmAdmin(ImportExportModelAdmin):
    search_fields = ['name', 'director']
    list_display = ['name', 'country', 'director', 'productionYear','image_display']
    image_display = AdminThumbnail(image_field='poster')
    image_display.short_description = 'Image'
    list_filter = ('productionYear',
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
    search_fields = ['film__name', 'festival__name', 'response', 'responseDate', 'dateSubmission']
    list_display = ['festival', 'film', 'dateSubmission', 'response', 'responseDate', 'isCompetitive']
    #list_filter = [FestivalFilter, FilmFilter]
    list_filter = ('dateSubmission','response', 'responseDate', 'isCompetitive')
    autocomplete_fields = ['festival', 'film']
    class Media:
        pass

class ProjectionAdmin(admin.ModelAdmin):
    search_fields = ['location', 'film__name',]


admin.site.register(Festival, FestivalAdmin)
admin.site.register(Film, FilmAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Projection, ProjectionAdmin)
