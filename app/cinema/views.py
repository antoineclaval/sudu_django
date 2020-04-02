from django.shortcuts import render

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

from django.http import HttpResponse

from .models import Film
from .models import Submission
from .models import Festival


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


def docxReport(request, month_id, year, film_id):
    currentFilm =  Film.objects.get(id=film_id)
    subList = Submission.objects.filter(dateSubmission__year=year).filter(dateSubmission__month=month_id).filter(film_id = film_id)
    output = ', '.join([q.festival.name for q in subList])
    print(output)
    s = F'{month_id} - {currentFilm.name} \n {output}'
    return HttpResponse(s)
