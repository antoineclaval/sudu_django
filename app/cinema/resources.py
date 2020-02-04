from import_export import resources
from .models import Festival

class FestivalResource(resources.ModelResource):
    class Meta:
        model = Festival