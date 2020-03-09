from import_export import resources
from .models import Festival
from .models import Film
from .models import Submission

class FestivalResource(resources.ModelResource):
    class Meta:
        model = Festival

class FilmResource(resources.ModelResource):
    class Meta:
        model = Film

class SubmissionResource(resources.ModelResource):
    class Meta:
        model = Submission