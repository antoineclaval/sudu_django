from django.urls import path

from . import views

urlpatterns = [
    path('reports/', views.index, name='index'),
    path('reports/<int:year>/<int:month_id>/', views.byMonth, name='byMonth'),
    path('reports/<int:year>/<int:month_id>/<int:film_id>/', views.inscriptionByMonthAndFilm, name='inscriptionView'),
    path('reports/<int:year>/<int:month_id>/<int:film_id>/docx/<lang>', views.docxReport, name='docxDownload'),
    path('reports/<int:year>/<int:month_id>/zip', views.generateZipReport, name='multiReport')

]