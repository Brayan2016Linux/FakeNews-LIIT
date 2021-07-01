from django.urls import path
import django.urls
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView



app_name='FakeNewsApp'
urlpatterns = [
   path('', views.indexView, name='index'),
   path(r'search/', views.indexView, name='indexView'),
   path(r'scrapper/search/', views.indexView, name='scrapperSearch'),
   path('scrapper/', views.scrapperView, name='scrapper'),
]