from django.contrib.auth.models import User
from django import forms
from .models import Dominio

class UrlForm(forms.ModelForm):
    

    class Meta:
        model = Dominio
        fields = ['url']

