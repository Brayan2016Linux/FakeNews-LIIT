from .Herramientas import *
from .Articulo import Articulo
import requests
from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element, SubElement, Comment

class PrensaLibre:
    site_name="laprensalibre.com"
    links = []
    articulos = [] #nuevo

    def scrap(self):
        
        r = requests.get('http://www.laprensalibre.cr')
        try:
            
            
            homePage = BeautifulSoup(r.content, 'html.parser')
            #portada  = homePage.find('main', attrs= {'class', 'ar-app nuxt-page-container'})
            portada = homePage.find('div', attrs={'class', 'bxslider'})
            nacional = homePage.find('div', attrs={'class', 'block1'})
            insolito = homePage.find('div', attrs={'class', 'block2 marginBottom32'})
            internacional = homePage.find('div', attrs={'class', 'block1 v2'})
            deportes = homePage.find('div', {'id': 'sportSlide'})

            for x in portada.find_all('a', href=True):     #nuevo
                if  x.has_attr('href'): #nuevo
                    self.links.append("http://www.laprensalibre.cr" + x.attrs['href'])  #nuevo
            

            for ul in nacional.find_all('a', href=True):
                if  ul.has_attr('href'): #nuevo
                    self.links.append("http://www.laprensalibre.cr" + ul.attrs['href'])  #nuevo
            
            for ul in insolito.find_all('a', href=True):
                if ul.has_attr('href'): #nuevo
                    self.links.append("http://www.laprensalibre.cr" + ul.attrs['href'])  #nuevo

            for ul in internacional.find_all('a', href=True):
                if ul.has_attr('href'): #nuevo
                    self.links.append("http://www.laprensalibre.cr" + ul.attrs['href'])
            
            for ul in deportes.find_all('a'):
                if ul.has_attr('href'): #nuevo
                    self.links.append("http://www.laprensalibre.cr" + ul.attrs['href'])

            

            self.links = list(dict.fromkeys(self.links)) # Elimina duplicados

            for link in self.links:
                texto_articulo="" #nuevo
                title = ""  #nuevo
                try:

                    info1 = Herramientas.get_simple(link)
                    sou = BeautifulSoup(info1, 'html.parser')

                    #date = sou.find('a', attrs={'class': 'date'})
                    
                    url = link
                    t = sou.find('section')
                    for txt in  t.find_all('p', recursive=False):
                        if not txt.has_attr('class'):
                            texto_articulo += " "+ txt.text
                    
                    # Titulo
                    titulo = sou.find('h1')
                    title = titulo.text

                    try:
                        try:
                            date = sou.find('div', attrs={'class', 'info'} )
                            published_date =  limpiarFecha(date.find(text=True,recursive=False ))
                        except Exception as e:
                            date = sou.find('div', attrs={'class', 'info'} )
                            published_date =  limpiarFecha(date.find('p',text=True,recursive=False ))
                    except Exception as e:
                        published_date = None
                        err = str(e) + "-laprensalibre-" + str(link) + "---"
                
                    self.articulos.append(Articulo(self.site_name, title, texto_articulo, url, published_date))

                except Exception as e:
                    err = str(e) + "-laprensalibre-" + str(link) + "---"

                

        except Exception as e:
            err = str(e) + "-laprensalibre-"
            print(err)

def limpiarFecha(fecha):

    t = fecha.split()
    t[2]=t[2].replace(',','')
    if t[2] == 'enero':
        mes = '21'
    elif t[2] == 'febrero':
        mes = '02'
    elif t[2] == 'marzo':
        mes = '03'
    elif t[2] == 'abril':
        mes = '04'
    elif t[2] == 'mayo':
        mes = '05'
    elif t[2] == 'junio':
        mes = '06'
    elif t[2] == 'julio':
        mes = '07'
    elif t[2] == 'agosto':
        mes = '08'
    elif t[2] == 'septiembre':
        mes = '09'
    elif t[2] == 'octubre':
        mes = '10'
    elif t[2] == 'noviembre':
        mes = '11'
    elif t[2] == 'diciembre':
        mes = '12'
    else:
        mes='00'
        print("Error con el Mes de la fecha extraida del articulo !!!")
    
    fechaLimpia = t[0]+'/'+mes+'/'+t[3]+' '+'00:00'+' '+'pm'
    
    return fechaLimpia


