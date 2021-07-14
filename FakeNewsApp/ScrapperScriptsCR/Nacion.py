from django.utils.html import linebreaks
from .Herramientas import *
from .Articulo import Articulo
import requests
from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element, SubElement, Comment
import newspaper
from newspaper import Article

class Nacion:
    site_name="nacion.com" #nuevo
    links = []
    articulos = []

    def alt_getArticle(self,link):
        texto_articulo="" #nuevo
        title = ""  #nuevo
        info1 = get_simple(link)
        sou = BeautifulSoup(info1, 'html.parser')
        published_date = sou.find('time')
        published_date = published_date.text 
        title = sou.find('h1', attrs={'class': 'primary-font__PrimaryFontStyles-o56yd5-0 dEdODy headline'})
        title = title.text

        sou = sou.find('article',attrs={'class':'default__ArticleBody-xb1qmn-2 hIbUDc article-body-wrapper'})
        for txt in  sou.find_all('h2'):
            texto_articulo += " "+ txt.text
        
        for txt in  sou.find_all('p'):
            texto_articulo += " "+ txt.text

        return title, texto_articulo, published_date

    def getArticle(self, link):
        article = Article(link)
        article.download()
        article.parse() 

        return article.title,article.text, article.publish_date


    def scrap(self):
        
        r = requests.get('https://www.nacion.com')
        try:
            
            
            homePage = BeautifulSoup(r.content, 'html.parser')
            portada = homePage.find('div', attrs={'class': 'container-fluid double-chain chain-container'})
            ultimasNoticias = homePage.find('aside', attrs={'class':'col-sm-md-12 col-lg-xl-4 right-article-section ie-flex-100-percent-sm layout-section wrap-bottom'})
            destacado = homePage.find('div', attrs={'class', 'top-table-list-section top-table-list-section-small row'})

            for x in portada.find_all('h2'):     #nuevo
                x = x.find('a',href=True)
                self.links.append("https://www.nacion.com" + x.attrs['href'])  #nuevo
            
            ultimasNoticias = ultimasNoticias.find('div',attrs={'class':'top-table-list-container layout-section'})
            for x in ultimasNoticias.find_all('h2'):
                x = x.find('a',href=True)
                self.links.append("https://www.nacion.com" + x.attrs['href'])  #nuevo
            
            for x in destacado.find_all('h2'):
                x = x.find('a',href=True)
                self.links.append("https://www.nacion.com" + x.attrs['href'])  #nuevo
            
            self.links = list(dict.fromkeys(self.links)) # Elimina duplicados

            for link in self.links:
                
                try:
                    
                    title, texto_articulo, published_date= self.getArticle(link)
                    if len(texto_articulo)>200:
                        title, texto_articulo, published_date= self.alt_getArticle(link)
                    self.articulos.append(Articulo(self.site_name,title,texto_articulo,link,published_date))

                except Exception as e:
                    err = str(e) + "-NACION-" + str(link) + "---"
                    print(err)

        except Exception as e:
            err = str(e) + "-NACION-"
            print(err)

