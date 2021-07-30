from django.shortcuts import render
from django.http import HttpResponse
import validators
import math
from .models import Verbo
from .models import Dominio
import requests,json
import newspaper
from newspaper import Article
from serpapi import GoogleSearchResults
from bs4 import BeautifulSoup
from django.utils.html import format_html
from django.template.loader import render_to_string
from .tokenizer_text import tokenize_text as tkt
from .data_graph import data_graph as tg
from .readability import readability as rd
import whois
from .domainCert import *
from .ScrapperScriptsCR import ScrapperMain, CRHoy


def scrapperView(request):
    if request.GET.get('teletica-btn'):
        articulos = []
        articulos = ScrapperMain.scrapTeletica()
        n= len(articulos)
        nSlides= n//4 + math.ceil((n/4)-(n//4))
        param = {'articulos':articulos, 'nSlides':nSlides}
        return render(request,"FakeNewsApp/scrapper.html", param)   

    if request.GET.get('crhoy-btn'):
        articulos = []
        articulos = ScrapperMain.scrapCRHoy()
        n= len(articulos)
        nSlides= n//4 + math.ceil((n/4)-(n//4))
        param = {'articulos':articulos, 'nSlides':nSlides}
        return render(request,"FakeNewsApp/scrapper.html", param)  
    
    if request.GET.get('nacion-btn'):
        articulos = []
        articulos = ScrapperMain.scrapNacion()
        n= len(articulos)
        nSlides= n//4 + math.ceil((n/4)-(n//4))
        param = {'articulos':articulos, 'nSlides':nSlides}
        return render(request,"FakeNewsApp/scrapper.html", param) 

    else:
        return render(request,"FakeNewsApp/scrapper.html")
    


def indexView(request):
    if request.GET.get('analizar-btn'):
        url_main = request.GET['url']
        
        if url_main is not "":
            valid=validators.url(url_main)
            if valid:
                r = requests.get(url_main)
                url = url_main.split('/')
                if len(url)>3 and (r.status_code == 200 or r.status_code == 403):
                    if Dominio.objects.filter(url=url[2]).exists():
                        dominios = Dominio.objects.get(url=url[2])
                        if dominios.blacklist:
                            if dominios.blacklist == 'C':
                                black = "Confiable"
                            elif dominios.blacklist == 'I':
                                black = "Intermedio"
                            elif dominios.blacklist == 'N':
                                black = "No confiable"
                            else:
                                black = "No definido"
                        else:
                            black = "No definido"
                        hit = True
                        authors = ""
                        if str(dominios) == 'www.crhoy.com':
                            crh = CRHoy.CRHoy()
                            title, text, publish_date= crh.getArticle(url_main)
                            publish_date = None
                            top_image=None
                            imgSearch = None
                        else:
                            article = Article(url_main)
                            article.download()
                            article.parse()
                            text = article.text   
                            publish_date = article.publish_date
                            top_image=article.top_image
                            for a in article.authors:
                                authors += a + ", "
                            authors = authors[:-2] 
                            imgSearch = searchImg(article.top_image) 

                        figCap = getNyTimesImgDesc(url_main)
                        quotes= getQuotes(text)

                        hostinfo = get_certificate(url[2].replace("www.",""),443)
                        domainInfo = print_basic_info(hostinfo)

                        graph_html, nodeFreq_html, gexf_string =graph(text)  #Pendiente agregar variable: gexf_string
                        nodeFreq_html = str(nodeFreq_html).replace("\\n","").replace("b\'","").replace("\'","")
                        gexf_string = str(gexf_string.replace("\\n",""))
                        #domain = get_whois_data(url[2])
                        #whois.query('google.com')
                        rd_score = readability_score(text) #Agrega índice de readability
                        rd_score = rd_score.split('. ')
                        data= [url[2], black, str(dominios.confianza), authors , publish_date, top_image,figCap,imgSearch,quotes]
                        param = {'data':data, 'hit':hit, 'graph_html':graph_html, 
                        'nodeFreq_html':nodeFreq_html,'article_text':text, 'dm_registrar': domainInfo, 'gexf_string':gexf_string,'rd_score':rd_score}
                        return render(request,"FakeNewsApp/index.html", param)
                    else:
                        hit = False
                        article = Article(url_main)
                        article.download()
                        article.parse()
                        authors = ""

                        figCap = getNyTimesImgDesc(url_main)
                        imgSearch = searchImg(article.top_image)

                        quotes= getQuotes(article.text)

                        for a in article.authors:
                            authors += a + ", "
                        authors = authors[:-2]

                        hostinfo = get_certificate(url[2].replace("www.",""),443)
                        domainInfo = print_basic_info(hostinfo)

                        graph_html, nodeFreq_html, gexf_string=graph(article.text)  #Pendiente agregar variable: gexf_string
                        nodeFreq_html = str(nodeFreq_html).replace("\\n","").replace("b\'","").replace("\'","")
                        gexf_string = str(gexf_string.replace("\\n",""))
                        
                        rd_score = readability_score(article.text) #Agrega índice de readability
                        rd_score = rd_score.split('. ')
                        data= [url[2], authors , article.publish_date, article.top_image,figCap,imgSearch,quotes]
                        errorHit="No se puede determinar el nivel de confianza del dominio (aún no se encuentra en nuestras listas)"
                        param = {'errorHit':errorHit,'hit':hit, 'data':data,'graph_html':graph_html, 'nodeFreq_html':nodeFreq_html, 'article_text':article.text, 'dm_registrar': domainInfo, 'gexf_string':gexf_string, 'rd_score':rd_score}
                        return render(request,"FakeNewsApp/index.html", param) 
                else:
                    hit = False
                    errorHit="URL probablemente no valido"
                    return render(request,"FakeNewsApp/index.html",{'errorHit':errorHit, 'hit':hit})
            else:
                hit = False
                errorHit="URL probablemente no valido"
                return render(request,"FakeNewsApp/index.html",{'errorHit':errorHit,'hit':hit})
        else:
                hit = False
                errorHit="URL probablemente no valido"
                return render(request,"FakeNewsApp/index.html",{'errorHit':errorHit,'hit':hit})   
    else:
        return render(request,"FakeNewsApp/index.html")




def getNyTimesImgDesc(url):
    r = requests.get(url)                    
    try:
        article = BeautifulSoup(r.content, 'html.parser')
        figCap = article.find('figcaption')
        text = figCap.text
        return text
    except Exception as e:
        err = str(e) + "-NyTimesImgDesc Error-"
        return ""
        

def searchImg(urlImg):
    url = "https://www.google.com/searchbyimage?hl=en-US&image_url="+urlImg
    return url


def getQuotes(text):
    import re
    quotes = re.findall(r'"(.*?)"', text)
    quotes+= re.findall(r'“(.*?)”', text)
    #quotes+= re.findall('"([^"]*)"', text)
    #quotes+= re.findall('“([^"]*)”', text)
    quotes+= re.findall(r'«(.*?)»', text)
    
    return searchVerbs(quotes)
    
def searchVerbs(quotes):
    allVerbs = list(Verbo.objects.all())
    quotes0 = []
    
    
    for q in quotes:
        replace = False
        wlist = q.split(" ")
        for verb in allVerbs:
            for w in wlist:
                v = str(w).rfind(verb.radicalRegular)
                if(v != -1):
                    wlist = list(map(lambda b: b.replace(w,format_html('<strong><font size="+2">{}</font></strong>',w)), wlist))

                #q = q.replace(verb.radicalRegular,format_html('<strong><font size="+2">{}</font></strong>',verb.radicalRegular))
                #replace = True
        q = " ".join(wlist)

                
         
        quotes0.append(q)
               
            
    return quotes0



def graph(text):
    gap = 1
    #Create Tokens from text:
    token_text = tkt(text, with_stopwords=False)
    source, target = token_text.get_source_target_graph(gap=gap)
    
    #Create Graph:
    text_graph = tg(source, target)
    text_graph.plot_wordcloud(save=False,html=True)
    #text_graph.plot_node_metric(metric='pagerank', html=True) #Por ahora sustituido con la nube de palabras
    text_graph.set_nx_layout(layout='spring')
    #Genera la red y la envía como html para ser renderizada por la página web:
    text_graph.draw_graph_metrics(save=False,html=True, metric='pagerank', with_labels=True, with_values=False)
    #Generación texto para descargar gephi, (pendiente botón para descarga):
    text_graph.save_to_gephi() #se crea variable text_graph.gexf_string

    return text_graph.graph_html_string, text_graph.nodeFreq_html_string, text_graph.gexf_string #Devuelve las salidad de datagraph en formato texto


def readability_score(text):
    rd_ = rd(text)
    return rd_.fernandez_huerta_score_web + rd_.count_score_web
    



