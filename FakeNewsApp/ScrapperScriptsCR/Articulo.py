import requests
import json
from newspaper import Article

class Articulo:
    title=""
    subtitle=""
    text=""
    site_name="ScrapperCR"
    url="scrapperCR.com"
    published_date=None
    category="None"
    tags=""
    highlighted=""
    lead=""
    paragraphs=""
    top_image=""

    
    def __init__(self, site_name, title, text, url, published_date):
        self.title = title
        self.text= text
        self.site_name=site_name
        self.url=url
        self.published_date = published_date
        #self.top_image = self.getImage(url)

    def printTitle(self):
        print(self.site_name + "   "+self.title)

    def printArticle(self):
        print("Sitio: "+self.site_name + "   Titulo: "+self.title+"   Texto: "+self.text+"   Fecha: "+self.published_date)

    def save(self):
        try:
        # Codigo para guardar en la base de datos

            self.crearRegistroDB(self.title, self.text, self.site_name, self.published_date, self.url)
            #print(self.site_name + "   "+self.title)

        except Exception as e:
            print(e)
    
    def crearRegistroDB(self,title, text, site_name, fecha, url_a):
        null = None
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        url = 'http://172.16.13.13/WebScrapper/api/newarticle/'
        request = requests.post(url, json={"title": title,"text": text,"site_name": site_name,"category": null,"highlighted": null,"lead": null,"paragraphs": null,"published_date": fecha,"subtitle": null,"tags": null,"url": url_a}, headers=headers)
        print(str(request.status_code) + ": "+"Site: "+ site_name +  ">> "+title)

    def getImage(url):
        article = Article(url)
        article.download()
        article.parse()
        return article.top_image
    
