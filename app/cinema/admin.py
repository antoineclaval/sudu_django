from django.contrib import admin
from imagekit.admin import AdminThumbnail

from .models import Festival
from .models import Film
from .models import Submission


class FestivalAdmin(admin.ModelAdmin):
    search_fields = ['name']


class FilmAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'image_display']
    image_display = AdminThumbnail(image_field='poster')
    image_display.short_description = 'Image'

    readonly_fields = ['image_display']  # this is for the change form

class SubmissionAdmin(admin.ModelAdmin):
    search_fields = ['dateSent']



admin.site.register(Festival, FestivalAdmin)
admin.site.register(Film, FilmAdmin)
admin.site.register(Submission, SubmissionAdmin)
