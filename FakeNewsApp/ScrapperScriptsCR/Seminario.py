from .Herramientas import *
from .Articulo import Articulo
import requests
from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element, SubElement, Comment

class Seminario:
    site_name="seminariouniversidad.com"
    links = []
    articulos = [] #nuevo

    def scrap(self):
        
        r = Herramientas.get_especial('https://semanariouniversidad.com')
        try:
            
            
            homePage = BeautifulSoup(r, 'html.parser')
            #portada  = homePage.find('main', attrs= {'class', 'ar-app nuxt-page-container'})
            portada = homePage.find('div', attrs={'class', 'slider-wrap clearfix'})
            ultimaH = homePage.find('div', {'id': 'recent-tab-reedwanwidgets__tabs-3'})
            masInformacion = homePage.find('div', {'id': 'block4'})
        
            

            for x in portada.find_all('div', attrs={'class', 'item sitem'}):     #nuevo
                x = x.find('a', href=True, recursive=False)
                if  x.has_attr('href'): #nuevo
                    self.links.append(x.attrs['href'])  #nuevo
            

            for ul in ultimaH.find_all('h3', attrs={'class', 'entry-title'}):
                ul =  ul.find('a', href=True, recursive=False)
                if  ul.has_attr('href'): #nuevo
                    self.links.append(ul.attrs['href'])  #nuevo
            
            for ul in masInformacion.find_all('li'):
                ul = ul.find('a', href=True, recursive=False)
                if ul.has_attr('href'): #nuevo
                   self.links.append(ul.attrs['href'])  #nuevo

            

            #links.append(delImpreso(homePage)) #se recomienda correr esta funcione cada 8 dias
            #links.append(ultimaHora(homePage)) #se recomienda correr esta funcione cada 3 dias 

    
            self.links = list(dict.fromkeys(self.links)) # Elimina duplicados

            for link in self.links:
                texto_articulo="" #nuevo
                title = ""  #nuevo
                try:

                    info1 = Herramientas.get_especial(link)
                    sou = BeautifulSoup(info1, 'html.parser')

                    #date = sou.find('a', attrs={'class': 'date'})
                    
                    url = link
                    t = sou.find('div', attrs={'class', 'entry-content-text'})
                    for txt in  t.find_all('p', recursive=False):
                        if not txt.has_attr('class'):
                            texto_articulo += " "+ txt.text
                    
                    # Titulo
                    titulo = sou.find('h1', attrs={'class', 'entry-title'})
                    title = titulo.text

                    try:
                            date = sou.find('time', attrs={'class', 'meta-date updated'} )
                            published_date =  limpiarFecha(date.attrs['datetime'])
                            
                    except Exception as e:
                        published_date = None
                        err = str(e) + "-seminariouniversidad-" + str(link) + "---"
                
                    self.articulos.append(Articulo(self.site_name, title, texto_articulo, url, published_date))

                except Exception as e:
                    err = str(e) + "-seminariouniversidad-" + str(link) + "---"

                

        except Exception as e:
            err = str(e) + "-seminariouniversidad-"
            print(err)


def limpiarFecha(fecha):

    t = fecha.split('-')
    anio = t[0]
    mes = t[1]
    t = t[2].split('T')
    dia = t[0]
    t = t[1].split(':')
    hora = t[0]+':'+t[1]

    
   
    
    fechaLimpia = mes+'/'+dia+'/'+anio+' '+hora
    
    return fechaLimpia

def delImpreso(homePage):
        
        
        urls = []

        Imp = homePage.find('div', {'id': 'block-ajax-query-contentseven3'})
        slider = homePage.find('div', {'id': 'blockslider2'})

        for ul in Imp.find_all('h3', attrs={'class', 'entry-title'} ):
            ul = ul.find('a', href=True, recursive=False)
            if ul.has_attr('href'): #nuevo
                urls.append(ul.attrs['href'])  #nuevo
        
        for x in slider.find_all('div', attrs={'class', 'item sitem'}):     #nuevo
            x = x.find('a', href=True, recursive=False)
            if  x.has_attr('href'): #nuevo
             urls.append(x.attrs['href'])
        
        if not urls:
            return urls
     

def ultimaHora(homePage):
        urls = []
        uH = homePage.find('div', {'id': 'block-ajax-query-contenttwelve1'})
        for ul in uH.find_all('h3', attrs={'class', 'entry-title'} ):
            ul = ul.find('a', href=True, recursive=False)
            if ul.has_attr('href'): #nuevo
                urls.append(ul.attrs['href'])  #nuevo
        if not urls:
            return urls

