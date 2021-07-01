from .Herramientas import *
from .Articulo import Articulo
import requests
from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element, SubElement, Comment

class ElFinanciero:
    site_name="elfinanciero.com" #nuevo
    links = []
    articulos = []

    def scrap(self):
        
        r = requests.get('https://www.elfinancierocr.com')
        try:
            
            
            homePage = BeautifulSoup(r.content, 'html.parser')
            #portada  = homePage.find('main', attrs= {'class', 'ar-app nuxt-page-container'})
            portada = homePage.find('section', {'id': 'main-content'})
            masHistorias = homePage.find('div', attrs={'class': 'mas-noticias-chain pb-layout-item pb-chain pb-c-default-chain col-lg-9 col-md-9 col-sm-12 col-xs-12'})
            masLeido = homePage.find('aside', attrs={'class', 'line-up most-read full clearfix'})

            for x in portada.find_all('div',attrs={'class', 'headline xx-small normal-style'}):     #nuevo
                x = x.find('a',href=True)
                if not x.has_attr('class'): #nuevo
                    self.links.append("https://www.elfinancierocr.com" + x.attrs['href'])  #nuevo
            

            for ul in masHistorias.find_all('div', attrs={'class', 'headline small normal-style'}):
                l = ul.find('a',href=True)
                if not l.has_attr('class'): #nuevo
                    self.links.append("https://www.elfinancierocr.com" + l.attrs['href'])  #nuevo
            
            for ul in masLeido.find_all('h4'):
                ul = ul.find('a',href=True)
                if ul.has_attr('href'): #nuevo
                    self.links.append("https://www.elfinancierocr.com" + ul.attrs['href'])  #nuevo
            
            self.links = list(dict.fromkeys(self.links)) # Elimina duplicados

            for link in self.links:
                texto_articulo="" #nuevo
                title = ""  #nuevo
                try:

                    info1 = Herramientas.get_simple(link)
                    sou = BeautifulSoup(info1, 'html.parser')

                    #date = sou.find('a', attrs={'class': 'date'})
                    published_date = None #pediente: hay que tomar la fecha en el momento que se toma el link
                    url = link
                    for txt in  sou.find_all('p', attrs={'class': 'element element-paragraph'}):
                        texto_articulo += " "+ txt.text
                    
                    # Titulo
                    titulo = sou.find('div', attrs={'class': 'headline-hed-last'})
                    title = titulo.text
                    self.articulos.append(Articulo(self.site_name,title,texto_articulo,url,published_date))
                except Exception as e:
                    err = str(e) + "-ElFinanciero-" + str(link) + "---"

        except Exception as e:
            err = str(e) + "-ElFinanciero-"
            print(err)


