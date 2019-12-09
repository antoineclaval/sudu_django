from django.contrib import admin
from .models import Festival
from .models import Film


class FestivalAdmin(admin.ModelAdmin):
	search_fields = ['name']


class FilmAdmin(admin.ModelAdmin):
	search_fields = ['name']
    

admin.site.register(Festival, FestivalAdmin)
admin.site.register(Film, FilmAdmin)
