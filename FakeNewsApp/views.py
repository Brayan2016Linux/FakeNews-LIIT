from django.shortcuts import render
from django.http import HttpResponse
import validators
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


def indexView(request):
    
    if(request.POST):
        url_data = request.POST.dict()
        url_main = url_data.get("url")
        
        if url_main is not "":
            valid=validators.url(url_main)
            
            if valid:
                r = requests.get(url_main)
                url = url_main.split('/')
                if len(url)>3 and (r.status_code == 200):
                    
                    
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
                        article = Article(url_main)
                        article.download()
                        article.parse()     

                        authors = ""
                        for a in article.authors:
                            authors += a + ", "
                        authors = authors[:-2]

                        figCap = getNyTimesImgDesc(url_main)
                        imgSearch = searchImg(article.top_image)
                        imgTextSearch = searchImgText(figCap)

                        quotes= getQuotes(article.text)

                        graph_html, nodeFreq_html =graph(article.text)
                        nodeFreq_html = str(nodeFreq_html).replace("\\n","").replace("b\'","").replace("\'","")
            

                        #graph_html= render_to_string('FakeNewsApp/graph1.html')
                        #nodeFreq_html = render_to_string('FakeNewsApp/node_freq.html')

                        

                        data= [url[2], black, str(dominios.confianza), authors , article.publish_date, article.top_image,figCap,imgSearch,quotes]
                        return render(request,"FakeNewsApp/index.html",{'data':data, 'hit':hit, 'graph_html':graph_html, 'nodeFreq_html':nodeFreq_html})
                    else:
                        hit = False
                        article = Article(url_main)
                        article.download()
                        article.parse()
                        authors = ""

                        figCap = getNyTimesImgDesc(url_main)
                        imgSearch = searchImg(article.top_image)
                        imgTextSearch = searchImgText(figCap)

                        quotes= getQuotes(article.text)

                        for a in article.authors:
                            authors += a + ", "
                        authors = authors[:-2]

                        graph_html, nodeFreq_html =graph(article.text)

                        #graph_html= render_to_string('FakeNewsApp/graph1.html')
                        #nodeFreq_html = render_to_string('FakeNewsApp/node_freq.html')

                        

                        data= [url[2], authors , article.publish_date, article.top_image,figCap,imgSearch,quotes]
                        errorHit="No se puede determinar el nivel de confianza del dominio (a??n no se encuentra en nuestras listas): "
                        return render(request,"FakeNewsApp/index.html",{'errorHit':errorHit,'hit':hit, 'data':data,'graph_html':graph_html, 'nodeFreq_html':nodeFreq_html})
                else:
                    hit = False
                    errorHit="URL probablemente no valido"
                    return render(request,"FakeNewsApp/index.html",{'errorHit':errorHit, 'hit':hit})
            else:
                hit = False
                errorHit="URL probablemente no valido"
                return render(request,"FakeNewsApp/index.html",{'errorHit':errorHit,'hit':hit})
                
        
    return render(request, 'FakeNewsApp/index.html')



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

def searchImgText(txt):
    url = "https://www.google.com/search?q=" + txt
    return url.replace("\n", "")

def getQuotes(text):
    import re
    quotes = re.findall(r'"(.*?)"', text)
    quotes+=re.findall(r'???(.*?)???', text)
    
    return searchVerbs(quotes)

def searchVerbs(quotes):
    allVerbs = list(Verbo.objects.all())
    quotes0 = []
    
    for q in quotes:
        replace = False
        for verb in allVerbs:
            v = str(q).rfind(verb.radicalRegular)
            if(v != -1):
                q = q.replace(verb.radicalRegular,format_html('<strong><font size="+2">{}</font></strong>',verb.radicalRegular))
                replace = True
                
         
        quotes0.append(q)
               
            
    return quotes0


def graph(text):
    gap = 1
    #Create Tokens from text:
    token_text = tkt(text, with_stopwords=False)
    source, target = token_text.get_source_target_graph(gap=gap)
    
    #Create Graph:
    text_graph = tg(source, target)
    text_graph.plot_node_frequency(save=False,html=True)
    #text_graph.plot_node_metric(metric='pagerank', html=True) Pendiente
    text_graph.set_nx_layout(layout='spring')
    # Pendiente implementar generacion del gephi
    text_graph.draw_graph_metrics(save=False,html=True, metric='pagerank', with_labels=True, with_values=False, font_size=4)

    return text_graph.graph_html_string, text_graph.nodeFreq_html_string
