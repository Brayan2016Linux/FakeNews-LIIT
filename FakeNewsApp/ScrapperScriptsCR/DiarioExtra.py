from .Herramientas import *
from .Articulo import Articulo
from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element, SubElement, Comment
import requests #Nuevo

class DiarioExtra:
    
    site_name="diarioextra.com"
    links = []
    articulos = []
    
    def scrap(self):
        try:
                 #nuevo
                
                r = requests.get('http://www.diarioextra.com/home') #nuevo
                #r1_leidas = requests.get('http://www.diarioextra.com/home/leidas') #nuevo
                r2_destacadas = requests.get('http://www.diarioextra.com/home/destacadas') #nuevo
                #Portada
                homePage = BeautifulSoup(r.content, 'html.parser')
                portada  = homePage.find('div', attrs= {'class', 'mainNew'})
                portada1 = portada.find_all('a',href=True) #nuevo
                for x in portada1:     #nuevo
                    if not x.has_attr('class'): #nuevo
                        self.links.append("http://www.diarioextra.com"+ x.attrs['href'])  #nuevo
                #Mas Leidas        
                #homePage = BeautifulSoup(r1_leidas.content, 'html.parser')
                #for masleidas in homePage.find_all('li'):
                #    masleidas = masleidas.find('a',href=True)
                #    if not masleidas.has_attr('class'): #nuevo
                #            self.links.append("http://www.diarioextra.com"+ masleidas.attrs['href'])  #nuevo
                #Destacadas
                homePage = BeautifulSoup(r2_destacadas.content, 'html.parser')
                for destacadas in homePage.find_all('li'):
                    destacada = destacadas.find('a',href=True)
                    if not destacada.has_attr('class'): #nuevo
                            self.links.append("http://www.diarioextra.com"+ destacada.attrs['href'])  #nuevo
                
                self.links = list(dict.fromkeys(self.links)) # Elimina duplicados

                for link in self.links:
                    text="" #nuevo
                    title = ""  #nuevo
                    published_date=""
                    try:
                        info1 = Herramientas.get_simple(link)
                        sou = BeautifulSoup(info1, 'html.parser')
                        texto = sou.find('article')
                        for t in texto.find_all('p'):
                            text += " "+t.text
                        url = link
                        titulo = sou.find('h1')
                        title = titulo.text
                        try:
                            div = texto.find('div')
                            div = div.find('section')
                            date = div.find_all('p')
                            published_date = limpiarFecha(date[3].string + " "+ date[4].text)
                        except Exception as e:
                            published_date = None
                            err = str(e) + "-DIARIOEXTRA-" + str(link) + "No se logro obtener la fecha del articulo !"
                            print("No se logro obtener la fecha del articulo !")
                    
                        # Titulo
                        
                        self.articulos.append(Articulo(self.site_name,title,text,url,published_date))
                    except Exception as e:
                        err = str(e) + "-EXTRA-" + str(link) + "---"
                    
        except Exception as e:
            err = str(e) + "-EXTRA-"
            print(err)

def limpiarFecha(fecha):

    t = fecha.split()
    t[2]=t[2].replace(',','')
    if t[2] == 'Enero':
        mes = '21'
    elif t[2] == 'Febrero':
        mes = '02'
    elif t[2] == 'Marzo':
        mes = '03'
    elif t[2] == 'Abril':
        mes = '04'
    elif t[2] == 'Mayo':
        mes = '05'
    elif t[2] == 'Junio':
        mes = '06'
    elif t[2] == 'Julio':
        mes = '07'
    elif t[2] == 'Agosto':
        mes = '08'
    elif t[2] == 'Septiembre':
        mes = '09'
    elif t[2] == 'Octubre':
        mes = '10'
    elif t[2] == 'Noviembre':
        mes = '11'
    elif t[2] == 'Diciembre':
        mes = '12'
    else:
        mes='00'
        print("Error con el Mes de la fecha extraida del articulo !!!")
    
    fechaLimpia = t[1]+'/'+mes+'/'+t[3]+' '+t[5]+' '+t[6]
    
    return fechaLimpia

