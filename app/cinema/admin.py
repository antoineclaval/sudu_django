from django.contrib import admin
from imagekit.admin import AdminThumbnail
from admin_auto_filters.filters import AutocompleteFilter


from .models import Festival
from .models import Film
from .models import Submission
from .models import Projection


class FestivalAdmin(admin.ModelAdmin):
    search_fields = ['name']


class FilmAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'image_display']
    image_display = AdminThumbnail(image_field='poster')
    image_display.short_description = 'Image'

    readonly_fields = ['image_display']  # this is for the change form

class FestivalFilter(AutocompleteFilter):
    title = 'Festival' # display title
    field_name = 'festival' # name of the foreign key field

class SubmissionAdmin(admin.ModelAdmin):
    search_fields = ['dateSent']
    list_filter = [FestivalFilter]
    autocomplete_fields = ['festival']
    class Media:
        pass

class ProjectionAdmin(admin.ModelAdmin):
    search_fields = ['location']





admin.site.register(Festival, FestivalAdmin)
admin.site.register(Film, FilmAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Projection, ProjectionAdmin)
