import Herramientas
#from Articulo import Articulo Guarda en BD utilizando el objeto Articulo
import requests
from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element, SubElement, Comment
import json
class LaVozMiPueblo:
    site_name= "lavozdemipueblo.com" 
    links = []
    articulos = []
    

    def scrap(self):
        
        r = requests.get('https://lavozdemipueblo.com',headers={"User-Agent": "XY"})
        

        try:
            homePage = BeautifulSoup(r.content, 'html.parser')
            portada = homePage.find('div', attrs={'class': 'featured-slider post-slider'})
            deportes = homePage.find('div', attrs={'class': 'row gutter-parent-10'})

            for x in portada.find_all('div',attrs={'class', 'post-img-wrap'}):     
                x = x.find('a',href=True)
                self.links.append(x.attrs['href'])  
            
            for x in deportes.find_all('div',attrs={'class', 'post-img-wrap'}):     
                x = x.find('a',href=True)
                self.links.append(x.attrs['href'])  
            
            
            self.links = list(dict.fromkeys(self.links)) # Elimina duplicados

            for link in self.links:
                texto_articulo=""
                title = ""  
                try:

                    info1 = requests.get(link,headers={"User-Agent": "XY"})
                    sou = BeautifulSoup(info1.content, 'html.parser')

                    date = sou.find('div', attrs={'class': 'date'})
                    published_date = date.text.replace('\n','')
                    url = link
                    
                    so = sou.find('div', attrs={'class': 'entry-content'})

                    for txt in  so.find_all('li'):
                        texto_articulo += " "+ txt.text
                    for txt in  so.find_all('p'):
                        texto_articulo += " "+ txt.text
                    
                    
                    # Titulo
                    titulo = sou.find('header', attrs={'class': 'entry-header'})
                    titulo = sou.find('h1', attrs={'class': 'entry-title'})
                    title = titulo.text.replace('\n','')
                    texto_articulo = texto_articulo.replace('\n','')
                    #self.articulos.append(Articulo(self.site_name,title,texto_articulo,url, published_date)) -- guarda datos
                    #print("Titulo: "+title+"--"+texto_articulo+"=="+published_date)
                except Exception as e:
                    err = str(e) + "-LaVozMiPueblo-" + str(link) + "---\n\n\n"

        except Exception as e:
            err = str(e) + "-LaVozMiPueblo-"
            print(err)

test = LaVozMiPueblo ()
test.scrap()