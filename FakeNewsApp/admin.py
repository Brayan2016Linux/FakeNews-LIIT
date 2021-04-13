from django.contrib import admin
from .models import Dominio, Verbo

admin.site.register(Dominio)
admin.site.register(Verbo)

radio_fields = {'blacklist': admin.VERTICAL}

