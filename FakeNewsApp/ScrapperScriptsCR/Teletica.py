from .Herramientas import *
from .Articulo import Articulo
import requests
from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element, SubElement, Comment
import json

class Teletica:
    site_name="teletica.com"
    links = []
    articulos = [] #nuevo

    def __init__(self):
            self.site_name="teletica.com"
            self.links=[]
            self.articulos=[]

    def scrap(self):
        
        
        try:
            
            enlace = "https://teletica.com/"

            for l in getUltimas(enlace):
                self.links.append(l)
            for l in getMasLeidas(enlace):
                self.links.append(l)
            for l in getNoticias(enlace):
                self.links.append(l)
           
            for l in getDeportes(enlace):
                self.links.append(l)
            for l in getEntretenimiento(enlace):
                self.links.append(l)
            
            for l in getEstilo(enlace):
                self.links.append(l)
            
            self.links = list(dict.fromkeys(self.links)) # Elimina duplicados

            for link in self.links:
                texto_articulo="" #nuevo
                title = ""  #nuevo
                try:

                    info1 = get_simple(link)
                    sou = BeautifulSoup(info1, 'html.parser')

                    #date = sou.find('a', attrs={'class': 'date'})
                    
                    url = link
                    t = sou.find('div', attrs={'class','text-editor'})
                    for txt in  t.find_all('p', recursive=False):
                        if not txt.has_attr('class'):
                            texto_articulo += " "+ txt.text
                    
                    # Titulo
                    titulo = sou.find('h2')
                    title = titulo.text

                    
                    published_date =  None #Pendiente: Extraer fecha del JSON
                    
                
                    self.articulos.append(Articulo(self.site_name, title, texto_articulo, url, published_date))

                except Exception as e:
                    err = str(e) + "-TELETICA-" + str(link) + "---"

                

        except Exception as e:
            err = str(e) + "-TELETICA-"
            print(err)



def getUltimas(ul):
    url="https://teletica.com/widget/GetLastNews?categoryId=1&from=0&to=5&authorId=0"
    urls = []
    r = get_especial(url)
    j = json.loads(r)
    for x in range (0,5) :
        try:
            urls.append(ul+str(j[x]['Id'])+"_"+ j[x]['Url'])
        except Exception as e:
            err = str(e) + "-TELETICA-"
            print(err)
    return urls

def getMasLeidas(ul):
    url = "https://teletica.com/Widget/GetMostRead"
    urls = []
    r = get_especial(url)
    j = json.loads(r)
    for x in range (0,5) :
        try:
            urls.append(ul+str(j[x]['Id'])+"_"+ j[x]['Url'])
        except Exception as e:
            err = str(e) + "-TELETICA-"
            print(err)
    return urls

def getNoticias(ul):
    url = "https://teletica.com/asset/getMore/?slug=noticias&from=0&to=9"
    urls = []
    r = get_especial(url)
    j = json.loads(r)
    j= json.loads(j)
    for x in range (0,9) :
        try:
            urls.append(ul+str(j[x]['Id'])+"_"+ j[x]['Url'])
        except Exception as e:
            err = str(e) + "-TELETICA-"
            print(err)
    return urls
    
    

def getDeportes(ul):
    url = "https://teletica.com/asset/getMore/?slug=deportes&from=0&to=5"
    urls = []
    r = get_especial(url)
    j = json.loads(r)
    j= json.loads(j)
    for x in range (0,5) :
        try:
            urls.append(ul+str(j[x]['Id'])+"_"+ j[x]['Url'])
        except Exception as e:
            err = str(e) + "-TELETICA-"
            print(err)
    return urls

def getEntretenimiento(ul):
    url = "https://teletica.com/asset/getMore/?slug=entretenimiento&from=0&to=5"
    urls = []
    r = get_especial(url)
    j = json.loads(r)
    j= json.loads(j)
    for x in range (0,5) :
        try:
            urls.append(ul+str(j[x]['Id'])+"_"+ j[x]['Url'])
        except Exception as e:
            err = str(e) + "-TELETICA-"
            print(err)
    return urls

def getEstilo(ul):
    url = "https://teletica.com/asset/getMore/?slug=estilo-de-vida&from=0&to=5"
    urls = []
    r = get_especial(url)
    j = json.loads(r)
    j= json.loads(j)
    for x in range (0,5) :
        try:
            urls.append(ul+str(j[x]['Id'])+"_"+ j[x]['Url'])
        except Exception as e:
            err = str(e) + "-TELETICA-"
            print(err)
    return urls
