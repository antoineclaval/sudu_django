from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from .models import Film
from .models import Submission
from .models import Festival
from .models import Projection
from .models import Projection
from django.db.models import Count, Q, Sum, Min

from docxtpl import DocxTemplate

import os
import locale
from datetime import date
import time
import datetime
from sudu.settings import MEDIA_ROOT
from babel.dates import format_date, format_datetime, format_time

from io import BytesIO
from zipfile import ZipFile

import calendar
import json
from django.forms import model_to_dict

from django.contrib.auth.decorators import login_required


def generateZipReport(request, year, month_id):
    response = HttpResponse(content_type='application/zip')
    movie_id_list = request.GET.getlist('movie') 
    # lang = request.GET['lang']
    # print (movie_id_list)
  
    in_memory_zip = BytesIO()
    zip = ZipFile(in_memory_zip, "a")

    for movieID in movie_id_list :
        inMemoryDoc = BytesIO()
        docxDoc = generateDocXReport(month_id,year, "fr", movieID)
        docxDoc.save(inMemoryDoc)
        zip.writestr(docxDoc.core_properties.title+".docx", inMemoryDoc.getvalue())

        inMemoryDoc = BytesIO()
        docxDoc = generateDocXReport(month_id,year, "en", movieID)
        docxDoc.save(inMemoryDoc)
        zip.writestr(docxDoc.core_properties.title+".docx", inMemoryDoc.getvalue())
    
    # fix for Linux zip files read in Windows
    for file in zip.filelist:
        file.create_system = 0       

    zip.close()
    response["Content-Disposition"] = F'attachment; filename=Sudu-Report-{month_id}-{year}.zip'
    
    in_memory_zip.seek(0)    
    response.write(in_memory_zip.read())
    return response


FILM_TYPE_LABELS = {'DOCU': 'Documentaire', 'FICTION': 'Fiction', 'SHORT': 'Court-Métrage', 'XP': 'Experimental'}


@login_required(login_url='/admin/login')
def globalReport(request):
    current_year = int(time.strftime("%Y"))

    agg = Submission.objects.aggregate(
        total=Count('id'),
        total_selected=Count('id', filter=Q(response='SELECTIONED')),
        total_fees=Sum('fee'),
    )
    total = agg['total'] or 0
    total_selected = agg['total_selected'] or 0
    total_fees = agg['total_fees'] or 0
    selection_rate = round(total_selected / total * 100, 1) if total else 0
    unique_festivals = Submission.objects.values('festival').distinct().count()

    min_year = Submission.objects.aggregate(m=Min('dateSubmission__year'))['m'] or current_year
    year_range = list(range(min_year, current_year + 1))

    sent_by_year_map = {
        r['dateSubmission__year']: r['count']
        for r in Submission.objects.values('dateSubmission__year').annotate(count=Count('id'))
    }
    selected_by_year_map = {
        r['responseDate__year']: r['count']
        for r in Submission.objects.filter(response='SELECTIONED').values('responseDate__year').annotate(count=Count('id'))
    }
    sent_by_year = [sent_by_year_map.get(y, 0) for y in year_range]
    selected_by_year = [selected_by_year_map.get(y, 0) for y in year_range]

    top_films = Film.objects.annotate(sub_count=Count('submission')).order_by('-sub_count')[:10]

    country_qs = (
        Submission.objects
        .values('festival__country')
        .annotate(count=Count('id'))
        .order_by('-count')[:10]
    )
    country_labels = [r['festival__country'] for r in country_qs]
    country_counts = [r['count'] for r in country_qs]

    film_type_qs = (
        Submission.objects
        .values('film__filmType')
        .annotate(count=Count('id'))
    )
    type_labels = [FILM_TYPE_LABELS.get(r['film__filmType'], r['film__filmType']) for r in film_type_qs]
    type_counts = [r['count'] for r in film_type_qs]

    african_map = {
        r['festival__is_african']: r['count']
        for r in Submission.objects.values('festival__is_african').annotate(count=Count('id'))
    }
    african_counts = [african_map.get(False, 0), african_map.get(True, 0)]

    template = loader.get_template('all.html')
    context = {
        'total': total,
        'unique_festivals': unique_festivals,
        'selection_rate': selection_rate,
        'total_fees': total_fees,
        'year_labels': json.dumps(year_range),
        'sent_by_year': json.dumps(sent_by_year),
        'selected_by_year': json.dumps(selected_by_year),
        'top_films': top_films,
        'country_labels': json.dumps(country_labels),
        'country_counts': json.dumps(country_counts),
        'type_labels': json.dumps(type_labels),
        'type_counts': json.dumps(type_counts),
        'african_counts': json.dumps(african_counts),
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='/admin/login')
def index(request):
    year, month_id = map(int, time.strftime("%Y %m").split())
    return HttpResponseRedirect(F'/cinema/reports/{year}/{month_id}/')

def _to_monthly(qs, month_key):
    by_month = {row[month_key]: row['count'] for row in qs}
    return [by_month.get(m, 0) for m in range(1, 13)]


@login_required(login_url='/admin/login')
def byYear(request, year):
    sent_qs = (
        Submission.objects
        .filter(dateSubmission__year=year)
        .values('dateSubmission__month')
        .annotate(count=Count('id'))
    )
    selected_qs = (
        Submission.objects
        .filter(responseDate__year=year, response='SELECTIONED')
        .values('responseDate__month')
        .annotate(count=Count('id'))
    )
    template = loader.get_template('year.html')
    context = {
        'year': year,
        'sent_data': json.dumps(_to_monthly(sent_qs, 'dateSubmission__month')),
        'selected_data': json.dumps(_to_monthly(selected_qs, 'responseDate__month')),
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='/admin/login')
def byMonth(request, year, month_id):
    template = loader.get_template('index.html')
    context = {
        'movies_list': Film.objects.annotate(
            total_sent=Count('submission'),
            sent_this_month=Count('submission', filter=Q(
                submission__dateSubmission__year=year,
                submission__dateSubmission__month=month_id,
            ))
        ),
        'current_month_name': calendar.month_name[month_id],
        'current_year': time.strftime("%Y"),
        'total_sent_this_month': Submission.objects.filter(
            dateSubmission__year=year,
            dateSubmission__month=month_id,
        ).count(),
    }
    return HttpResponse(template.render(context, request))


def inscriptionByMonthAndFilm(request, month_id, year, film_id):
    template = loader.get_template('report/film.html')
    currentFilm = Film.objects.get(id=film_id)
    subList = Submission.objects.filter(dateSubmission__year=year).filter(dateSubmission__month=month_id).filter(film_id = film_id)  
    selectList = Submission.objects.filter(responseDate__year=year).filter(responseDate__month=month_id).filter(film_id = film_id).filter(response__iexact = 'SELECTIONED')
    rejectList = Submission.objects.filter(responseDate__year=year).filter(responseDate__month=month_id).filter(film_id = film_id).filter(response__iexact = 'REFUSED') 

    context = {
        'submissions_list': subList, 
        'select_list': selectList,
        'reject_list': rejectList,
        'current_month_name': calendar.month_name[month_id],
        'current_year': time.strftime("%Y"),
        'current_film': currentFilm
    }
    return HttpResponse(template.render(context, request))


def docxReport(request, month_id, year, lang,film_id):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    document = generateDocXReport(month_id, year, lang, film_id)
    document.save(response)
    response['Content-Disposition'] = F'attachment; filename={document.core_properties.title}-{month_id}-{year}.docx'
    return response

def getCleanDate(dirtyDate):
    if(dirtyDate.strip()):
        return " - " + dirtyDate.strip() + " - "

def generateDocXReport(month_id, year, lang, film_id):
    langMap = dict(fr={'template': 'template-fr.docx', 'locale': 'fr_FR', 'emptyList': 'Pas Encore.'},
                   en={'template': 'template-en.docx', 'locale': 'en_US', 'emptyList': 'Not yet.'})

    locale.setlocale(locale.LC_TIME, langMap.get(lang).get('locale'))

    file_path = os.path.join(MEDIA_ROOT, 'reportTemplate/')
    currentFilm =  Film.objects.get(id=film_id)
    subList = Submission.objects.filter(dateSubmission__year=year).filter(dateSubmission__month=month_id).filter(film_id=film_id)

    selectList = Submission.objects.filter(responseDate__year=year).filter(responseDate__month=month_id).filter(film_id=film_id).filter(response__iexact='SELECTIONED')
    rejectList = Submission.objects.filter(responseDate__year=year).filter(responseDate__month=month_id).filter(film_id=film_id).filter(response__iexact='REFUSED') 

    projList = Projection.objects.filter(films__id=film_id).filter(date__year=year).filter(date__month=month_id)

    subOutput, selectOutput, rejectOutput, projOutput = [], [], [], []

    for item in subList:
        festival_dict = model_to_dict(item.festival)
        festival_dict['country'] = {'name': item.festival.country.name, 'code': str(item.festival.country)}
        subOutput.append({'festival': festival_dict})
    if not subOutput:
        subOutput.append({'festival': {'name': langMap[lang]['emptyList'], 'country': {'name': '', 'code': ''}}})

    for item in selectList:
        festival_dict = model_to_dict(item.festival)
        festival_dict['country'] = {'name': item.festival.country.name, 'code': str(item.festival.country)}
        selectOutput.append({'festival': festival_dict})
    if not selectOutput:
        selectOutput.append({'festival': {'name': langMap[lang]['emptyList'], 'country': {'name': '', 'code': ''}}})

    for item in rejectList:
        festival_dict = model_to_dict(item.festival)
        festival_dict['country'] = {'name': item.festival.country.name, 'code': str(item.festival.country)}
        rejectOutput.append({'festival': festival_dict})
    if not rejectOutput:
        rejectOutput.append({'festival': {'name': langMap[lang]['emptyList'], 'country': {'name': '', 'code': ''}}})

    for item in projList:
        proj_dict = model_to_dict(item)
        proj_dict['country'] = {'name': item.country.name, 'code': str(item.country)}
        projOutput.append({'projection': proj_dict, 'date': item.date})
    if not projOutput:
        projOutput.append({'projection': {'location': langMap[lang]['emptyList'], 'country': {'name': '', 'code': ''}}})

    document = DocxTemplate(file_path + langMap[lang]['template'])

    dic = {'INSCRIPTIONS_LIST': subOutput,
           'MOVIE_NAME': currentFilm.name.upper(),
           'CURRENT_DATE': format_datetime(date.today(), format='dd MMMM YYYY', locale=langMap[lang]['locale']),
           'TARGET_MONTH': format_datetime(datetime.datetime(1900, int(month_id), 1), format='MMMM', locale=langMap[lang]['locale']),
           'TARGET_YEAR': str(year),
           'SELECTIONS_LIST': selectOutput,
           'REJECTIONS_LIST': rejectOutput,
           'PROJECTIONS_LIST': projOutput,
           }
    document.render(dic)

    document.core_properties.title = currentFilm.name+"-"+lang
    return document
