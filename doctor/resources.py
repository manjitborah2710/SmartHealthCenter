from import_export import resources
from .models import *

class PrescriptionResource(resources.ModelResource):
    class Meta:
        model = Prescription