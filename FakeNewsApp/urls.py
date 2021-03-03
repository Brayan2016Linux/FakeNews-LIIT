from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView



app_name='FakeNewsApp'
urlpatterns = [
   path('', views.indexView, name='index'),
]