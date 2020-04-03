from django.shortcuts import render

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

from django.http import HttpResponse

from .models import Film
from .models import Submission
from .models import Festival
from .models import ResponseChoice

from docx import Document

import os, locale
from datetime import date, datetime, time
from sudu.settings import BASE_DIR

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


def index(request):
    return HttpResponse('cinema.index')

def inscriptionByMonthAndFilm(request, month_id, year, film_id):
    currentFilm =  Film.objects.get(id=film_id)
    subList = Submission.objects.filter(dateSubmission__year=year).filter(dateSubmission__month=month_id).filter(film_id = film_id)
    output = ', '.join([q.festival.name for q in subList])
    print(output)
    s = F'{month_id} - {currentFilm.name} \n {output}'
    return HttpResponse(s)


def docxReport(request, month_id, year, lang,film_id):
    locale.setlocale(locale.LC_TIME, "fr_FR.utf8")

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


    print("\Selection:")
    for item in selectList:
        print(item.festival.name + " (" +  item.festival.country.name +")")
        selectOutput += (item.festival.name + " (" +  item.festival.country.name +")\n") 


    print("\Rejection:")
    for item in rejectList:
        print(item.festival.name + " (" +  item.festival.country.name +")")
        rejectOutput += (item.festival.name + " (" +  item.festival.country.name +")\n") 


    document = Document(file_path + 'TEMPLATE _ Suivi de diffusion.docx')

    dic = {'INSCRIPTIONS_LIST':subOutput,
           'MOVIE_NAME':currentFilm.name, 
           'CURRENT_DATE': datetime.today().strftime('%d %B %Y'),
           'TARGET_MONTH': str(month_id),
           'TARGET_YEAR': str(year),
           'SELECTIONS_LIST': selectOutput,
           'REJECTIONS_LIST': rejectOutput,
           'PROJECTIONS_LIST':''
           }

    for p in document.paragraphs:
        pItems = p.text.split(" ")
        for item in pItems:
            item = item.strip()
          #  print ('/'+item+'/') 
            if item in dic.keys():
                p.text = p.text.replace(item,dic[item])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = F'attachment; filename={currentFilm.name}-{month_id}-{year}.docx'
    document.save(response)
    return response
