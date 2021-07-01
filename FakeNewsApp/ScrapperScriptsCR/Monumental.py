from .Herramientas import *
from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element, SubElement, Comment
from .Articulo import Articulo
import requests #Nuevo

class Monumental:
    site_name="monumental.co.cr" #nuevo
    links = []
    articulos = []

    def scrap(self):
        
        
        r = requests.get('http://www.monumental.co.cr/') #nuevo
        try:
            #codigo = Herramientas.obtenerCodigoTiempo()
            #Herramientas.crearCarpeta(directorio, codigo, "monumental.COM")
            
            
            homePage = BeautifulSoup(r.content, 'html.parser')
            portadaCarousel  = homePage.find('div',{'id': 'homeSlider'})
            noticiasPortada = homePage.find('div', attrs={'class', 'col-md-9 cont-noticias'})
            #masLeido = homePage.find('div', attrs={'class', 'col-md-12 noticias'})


            for x in portadaCarousel.find_all('h1'):     #nuevo
                x = x.find('a',href=True)
                if not x.has_attr('class'): 
                    if x.text != '\n\n':    
                        self.links.append( x.attrs['href'])  
                
            for article in noticiasPortada.find_all('article'): #nuevo
                for a in  article.find_all('a',href=True):
                    if  a.has_attr('title'): 
                        self.links.append( a.attrs['href'])  
            #mas leido
            #for p in masLeido.find_all('p'):
            #    p = p.find('a',href=True)
            #    if  p.has_attr('href'): 
            #        self.links.append( p.attrs['href'])

            self.links = list(dict.fromkeys(self.links)) # Elimina duplicados
            
            for link in self.links:
                texto_articulo="" #nuevo
                title = ""  #nuevo
                try:

                    info1 = Herramientas.get_simple(link)
                    sou = BeautifulSoup(info1, 'html.parser')
                    texto = sou.find('div', attrs={'class': 'the-content'})
                    for p in texto.find_all('p'):
                        if  p.string:
                                texto_articulo += " "+ p.string

                    # Titulo
                    titulo = sou.find('h2')
                    title = titulo.text
                    url = link
                    try:
                        date = sou.find('h3', attrs={'class', 'fechahora'})
                        published_date = date.text
                    except Exception as e:
                        published_date = None
                        err = str(e) + "-monumental-" + str(link) + "---"
                        print(err)
                    self.articulos.append(Articulo(self.site_name,title,texto_articulo,url, published_date))
                except Exception as e:
                    err = str(e) + "-monumental-" + str(link) + "---"
                    print(err)

                
                

        except Exception as e:
            err = str(e) + "-monumental-"
            print(err)

