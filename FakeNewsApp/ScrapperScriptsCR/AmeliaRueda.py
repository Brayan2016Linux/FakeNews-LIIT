from .Herramientas import *
from .Articulo import Articulo
import requests
from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element, SubElement, Comment
import json

class AmeliaRueda:
    site_name="ameliarueda.com"
    url="https://www.ameliarueda.com/"
    links = []
    articulos = [] #nuevo

    def scrap(self):
        
        

        try:
            
            for l in getAbridora(self.url):
                self.links.append(l)
            for l in getConversa(self.url):
                self.links.append(l)
            for l in getArticulos(self.url):
                self.links.append(l)
            
            self.links = list(dict.fromkeys(self.links)) # Elimina duplicados

            for link in self.links:
                texto_articulo="" #nuevo
                title = ""  #nuevo
                try:

                    info1 = Herramientas.get_simple(link)
                    sou = BeautifulSoup(info1, 'html.parser')

                    #date = sou.find('a', attrs={'class': 'date'})
                    
                    url = link
                    t = sou.find('div', attrs={'class','ar-entry__text'})
                    for txt in  t.find_all('p'):
                        if not txt.has_attr('class'):
                            texto_articulo += " "+ txt.text
                    
                    # Titulo
                    titulo = sou.find('h1', attrs={'class','ar-entry__title'})
                    title = titulo.text

                    
                    published_date =  getDate(link)
                    
                
                    self.articulos.append(Articulo(self.site_name, title, texto_articulo, url, published_date))

                except Exception as e:
                    err = str(e) + "-AMELIARUEDA-" + str(link) + "---"

                

        except Exception as e:
            err = str(e) + "-AMELIARUEDA-"
            print(err)



def getAbridora(ul):
    #abridora, de primero, debe saber
    url="https://cmsapi.ameliarueda.com//endpoints/home-entries"
    urls = []
    r = Herramientas.get_especial(url)
    j = json.loads(r)
    try:
        urls.append(ul+'nota/'+ j['abridora'][0]['url_title'])
    except Exception as e:
            err = str(e) + "-AMELIARUEDA-"
            print(err)
    for x in range (0,5) :
        try:
            urls.append(ul+'nota/'+ j['articulos-deportes'][x]['url_title'])
        except Exception as e:
            err = str(e) + "-AMELIARUEDA-"
            print(err)
    return urls


def getConversa(ul):
    url="https://cmsapi.ameliarueda.com//endpoints/api-entries?channel=articulo%7Cdeportes&offset=0&limit=25&category=&entryId=58302%7C58328%7C58287%7C58264%7C58238&media_category="
    urls = []
    r = Herramientas.get_especial(url)
    j = json.loads(r)
    for x in range (0,5) :
        try:
            urls.append(ul+'nota/'+ j[x]['url_title'])
        except Exception as e:
            err = str(e) + "-AMELIARUEDA-"
            print(err)

    return urls


def getArticulos(ul):
    # todos los articulos
    url="https://cmsapi.ameliarueda.com//endpoints/api-entries?channel=articulo%7Cdeportes&offset=0&limit=25&category=&entryId=&media_category="
    urls = []
    r = Herramientas.get_especial(url)
    j = json.loads(r)

    for x in range (0,24) :
        try:
            urls.append(ul+'nota/'+ j[x]['url_title'])
        except Exception as e:
            err = str(e) + "-AMELIARUEDA-"
            print(err)

    return urls

def getDate(titulo):
    date=""
    try:
        titulo = titulo[33:]
        url='https://cmsapi.ameliarueda.com/endpoints/api-nota/'+titulo+'?channel=articulo&show_categories=yes'
        r = Herramientas.get_especial(url)
        j = json.loads(r)
        date = j[0]['entry_date']
    except Exception as e:
            err = str(e) + "-AMELIARUEDA-"
            print(err)

    return date.replace('-',' ')

