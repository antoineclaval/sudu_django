from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from imagekit.admin import AdminThumbnail
from admin_auto_filters.filters import AutocompleteFilter
from django_countries.filters import CountryFilter

from .models import Festival
from .models import Film
from .models import Submission
from .models import Projection

class FestivalAdmin(ImportExportModelAdmin):
    search_fields = ['name', 'country']
    list_display = ['name', 'country', 'is_african', 'country', 'has_rental_fee', 'price']


class FilmAdmin(ImportExportModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'image_display']
    image_display = AdminThumbnail(image_field='poster')
    image_display.short_description = 'Image'

    readonly_fields = ['image_display']  # this is for the change form

class FestivalFilter(AutocompleteFilter):
    title = 'Festival' # display title
    field_name = 'festival' # name of the foreign key field

class FilmFilter(AutocompleteFilter):
    title = 'Film' # display title
    field_name = 'film' # name of the foreign key field



class SubmissionAdmin(admin.ModelAdmin):
    search_fields = ['film__name', 'festival__name']
    list_display = ['festival', 'film', 'dateSubmission']
    #list_filter = [FestivalFilter, FilmFilter]
    autocomplete_fields = ['festival', 'film']
    class Media:
        pass

class ProjectionAdmin(admin.ModelAdmin):
    search_fields = ['location']





admin.site.register(Festival, FestivalAdmin)
admin.site.register(Film, FilmAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Projection, ProjectionAdmin)
