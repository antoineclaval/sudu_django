from django.shortcuts import render

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

from django.http import HttpResponse
from django.template import loader


from .models import Film
from .models import Submission
from .models import Festival
from .models import ResponseChoice

from docx import Document

import os, locale
from datetime import date, time
import datetime
from sudu.settings import BASE_DIR
from babel.dates import format_date, format_datetime, format_time

from io import StringIO
from zipfile import ZipFile


def image_upload(request):
    if request.method == "POST" and request.FILES["image_file"]:
        image_file = request.FILES["image_file"]
        fs = FileSystemStorage()
        filename = fs.save(image_file.name, image_file)
        image_url = fs.url(filename)
        print(image_url)
        return render(request, "upload.html", {
            "image_url": image_url
        })
    return render(request, "upload.html")

#         zf.writestr(movieID, generateDocXReport(month,year, lang, movieID).save(iostream).getvalue())

def generateReport(request):
    response = HttpResponse(content_type='application/zip')
    movie_id_list = request.GET.getlist('movie') 
    month = request.GET['month']
    year = request.GET['year']
    lang = request.GET['lang']
    print (movie_id_list)
    print(   "/" + month + "/" + year + "/" )
  
    in_memory = StringIO()
    zip = ZipFile(in_memory, "a")
        
    zip.writestr("file1.txt", "some text contents")
    zip.writestr("file2.csv", "csv,data,here")
    
    # fix for Linux zip files read in Windows
    for file in zip.filelist:
        file.create_system = 0        
    zip.close()

    response = HttpResponse(mimetype="application/zip")
    response["Content-Disposition"] = "attachment; filename=two_files.zip"
    
    in_memory.seek(0)    
    response.write(in_memory.read())
    return response


def index(request):
    template = loader.get_template('index.html')
    context = {
        'movies_list': Film.objects.all()
    }
    return HttpResponse(template.render(context, request))

def inscriptionByMonthAndFilm(request, month_id, year, film_id):
    currentFilm =  Film.objects.get(id=film_id)
    subList = Submission.objects.filter(dateSubmission__year=year).filter(dateSubmission__month=month_id).filter(film_id = film_id)
    output = ', '.join([q.festival.name for q in subList])
    print(output)
    s = F'{month_id} - {currentFilm.name} \n {output}'
    return HttpResponse(s)


def docxReport(request, month_id, year, lang,film_id):

    langMap = dict(fr = {'template': 'TEMPLATE _ Suivi de diffusion.docx', 'locale': 'fr_FR', 'emptyList' : 'Pas Encore.'},
        en = {'template': 'TEMPLATE _ Distribution Tracking.docx', 'locale': 'en_US', 'emptyList' : 'Not yet.'})

    locale.setlocale(locale.LC_TIME, langMap.get(lang).get('locale'))

    file_path = os.path.join(BASE_DIR, 'temp/')
    currentFilm =  Film.objects.get(id=film_id)
    subList = Submission.objects.filter(dateSubmission__year=year).filter(dateSubmission__month=month_id).filter(film_id = film_id)

    selectList = Submission.objects.filter(dateSubmission__year=year).filter(film_id = film_id).filter(response__iexact = 'SELECTIONED')
    rejectList = Submission.objects.filter(dateSubmission__year=year).filter(film_id = film_id).filter(response__iexact = 'REFUSED')

    subOutput, selectOutput, rejectOutput = "","",""

    print("\nInscriptions:")
    for item in subList:
        print(item.festival.name + " (" +  item.festival.country.name +")")
        subOutput += (item.festival.name + " (" +  item.festival.country.name +")\n") 
    if not subOutput:
        subOutput = langMap[lang]['emptyList']

    print("\Selection:")
    for item in selectList:
        print(item.festival.name + " (" +  item.festival.country.name +")")
        selectOutput += (item.festival.name + " (" +  item.festival.country.name +")\n") 
    if not selectOutput:
        selectOutput = langMap[lang]['emptyList']

    print("\Rejection:")
    for item in rejectList:
        print(item.festival.name + " (" +  item.festival.country.name +")")
        rejectOutput += (item.festival.name + " (" +  item.festival.country.name +")\n") 
    if not rejectOutput:
        rejectOutput = langMap[lang]['emptyList']



    document = Document(file_path + langMap[lang]['template'])

    dic = {'INSCRIPTIONS_LIST':subOutput,
        'MOVIE_NAME':currentFilm.name, 
        'CURRENT_DATE': format_datetime(date.today(), format='dd MMMM YYYY', locale=langMap[lang]['locale']),
        'TARGET_MONTH': format_datetime(datetime.datetime(1900, int(month_id),1), format='MMMM',locale=langMap[lang]['locale']),
        'TARGET_YEAR': str(year),
        'SELECTIONS_LIST': selectOutput,
        'REJECTIONS_LIST': rejectOutput,
        'PROJECTIONS_LIST': langMap[lang]['emptyList']
        }

    for p in document.paragraphs:
        pItems = p.text.split(" ")
        for item in pItems:
            item = item.strip()
            if item in dic.keys():
                p.text = p.text.replace(item,dic[item])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = F'attachment; filename={currentFilm.name}-{month_id}-{year}-{lang}.docx'
    document.save(response)
    return response




def generateDocXReport(month_id, year, lang,film_id):

    langMap = dict(fr = {'template': 'TEMPLATE _ Suivi de diffusion.docx', 'locale': 'fr_FR', 'emptyList' : 'Pas Encore.'},
        en = {'template': 'TEMPLATE _ Distribution Tracking.docx', 'locale': 'en_US', 'emptyList' : 'Not yet.'})

    locale.setlocale(locale.LC_TIME, langMap.get(lang).get('locale'))

    file_path = os.path.join(BASE_DIR, 'temp/')
    currentFilm =  Film.objects.get(id=film_id)
    subList = Submission.objects.filter(dateSubmission__year=year).filter(dateSubmission__month=month_id).filter(film_id = film_id)

    selectList = Submission.objects.filter(dateSubmission__year=year).filter(film_id = film_id).filter(response__iexact = 'SELECTIONED')
    rejectList = Submission.objects.filter(dateSubmission__year=year).filter(film_id = film_id).filter(response__iexact = 'REFUSED')

    subOutput, selectOutput, rejectOutput = "","",""

    print("\nInscriptions:")
    for item in subList:
        print(item.festival.name + " (" +  item.festival.country.name +")")
        subOutput += (item.festival.name + " (" +  item.festival.country.name +")\n") 
    if not subOutput:
        subOutput = langMap[lang]['emptyList']

    print("\Selection:")
    for item in selectList:
        print(item.festival.name + " (" +  item.festival.country.name +")")
        selectOutput += (item.festival.name + " (" +  item.festival.country.name +")\n") 
    if not selectOutput:
        selectOutput = langMap[lang]['emptyList']

    print("\Rejection:")
    for item in rejectList:
        print(item.festival.name + " (" +  item.festival.country.name +")")
        rejectOutput += (item.festival.name + " (" +  item.festival.country.name +")\n") 
    if not rejectOutput:
        rejectOutput = langMap[lang]['emptyList']



    document = Document(file_path + langMap[lang]['template'])

    dic = {'INSCRIPTIONS_LIST':subOutput,
        'MOVIE_NAME':currentFilm.name, 
        'CURRENT_DATE': format_datetime(date.today(), format='dd MMMM YYYY', locale=langMap[lang]['locale']),
        'TARGET_MONTH': format_datetime(datetime.datetime(1900, int(month_id,1), format='MMMM',locale=langMap[lang]['locale'])),
        'TARGET_YEAR': str(year),
        'SELECTIONS_LIST': selectOutput,
        'REJECTIONS_LIST': rejectOutput,
        'PROJECTIONS_LIST': langMap[lang]['emptyList']
        }

    for p in document.paragraphs:
        pItems = p.text.split(" ")
        for item in pItems:
            item = item.strip()
            if item in dic.keys():
                p.text = p.text.replace(item,dic[item])

    #response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    #response['Content-Disposition'] = F'attachment; filename={currentFilm.name}-{month_id}-{year}-{lang}.docx'
# document.save(response)
    return document