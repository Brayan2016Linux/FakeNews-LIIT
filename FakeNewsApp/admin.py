from django.contrib import admin
from import_export import resources
from .models import Dominio, Verbo

admin.site.register(Dominio)
admin.site.register(Verbo)

radio_fields = {'blacklist': admin.VERTICAL}

class VerboResource(resources.ModelResource):

    class Meta:
        model = Verbo