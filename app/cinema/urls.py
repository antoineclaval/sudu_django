from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('festival/inscription/<int:year>/<int:month_id>/<int:film_id>/', views.inscriptionByMonthAndFilm, name='index'),
    path('festival/inscription/<int:year>/<int:month_id>/<int:film_id>/pdf', views.pdfReport, name='index'),
]