from .Herramientas import *
from .Articulo import Articulo
from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element, SubElement, Comment
import requests #Nuevo


class Repretel:
    site_name="repretel.com"
    links = []
    articulos = [] #nuevo

    def scrap(self):

        r = requests.get('https://www.repretel.com') #nuevo
        try:
            #codigo = Herramientas.obtenerCodigoTiempo()
            #Herramientas.crearCarpeta(directorio, codigo, "REPRETEL.COM")
            
            homePage = BeautifulSoup(r.content, 'html.parser')
            portada_1  = homePage.find('section', attrs= {'class', 'mb-3'})
            portada_2 = portada_1.find_all('a',href=True) #nuevo
            for x in portada_2:     #nuevo
                if not x.has_attr('class'): #nuevo
                    if x.text != '\n\n':    #nuevo
                        self.links.append( x.attrs['href'])  #nuevo
                

            
            for portada in homePage.find_all('div', attrs={'class', 'thumbail-noticias-secundarias'}):
                portada = portada.find('a',href=True)
                if not portada.has_attr('class'): #nuevo
                            self.links.append( portada.attrs['href'])  #nuevo
            
            self.links = list(dict.fromkeys(self.links)) # Elimina duplicados
            
            for link in self.links:
                texto_articulo="" #nuevo
                title = ""  #nuevo
                published_date= ""
                try:

                    info1 = Herramientas.get_simple(link)
                    sou = BeautifulSoup(info1, 'html.parser')
                    url = link
                    
                    
                    try:
                        date = sou.find('span', attrs={'class', 'ml-auto p-2 bd-highlight hrs_detalle-categoria'})
                        published_date = limpiarFecha(date.string)
                    except Exception as e:
                        published_date = None
                        err = str(e) + "-REPRETEL-" + str(link) + "No se logro obtener la fecha del articulo !"
                        print("No se logro obtener la fecha del articulo !")

                    
                    texto = sou.find('div', attrs={'class': 'texto_detalle-categoria'})
                    texto = texto.find('div', attrs={'class': 'col-12'})
                    texto_articulo = texto.text.replace('\n', ' ').replace('\r', ' ')
                    texto_articulo = texto_articulo.replace('\t', ' ').replace('\xa0', ' ')

                    # Titulo
                    titulo = sou.find('h2', attrs={'class': 'title_detalle-categoria'})
                    title = titulo.text
                    texto_articulo= texto_articulo.strip()
                    self.articulos.append(Articulo(self.site_name, title, texto_articulo, url, published_date))
                except Exception as e:
                    err = str(e) + "-REPRETEL-" + str(link) + "---"
                
        except Exception as e:
            err = str(e) + "-REPRETEL-"
            print(err)

def limpiarFecha(fecha):

    t = fecha.split()
    if t[3] == 'Enero':
        mes = '21'
    elif t[3] == 'Febrero':
        mes = '02'
    elif t[3] == 'Marzo':
        mes = '03'
    elif t[3] == 'Abril':
        mes = '04'
    elif t[3] == 'Mayo':
        mes = '05'
    elif t[3] == 'Junio':
        mes = '06'
    elif t[3] == 'Julio':
        mes = '07'
    elif t[3] == 'Agosto':
        mes = '08'
    elif t[3] == 'Septiembre':
        mes = '09'
    elif t[3] == 'Octubre':
        mes = '10'
    elif t[3] == 'Noviembre':
        mes = '11'
    elif t[3] == 'Diciembre':
        mes = '12'
    else:
        mes='00'
        print("Error con el Mes de la fecha extraida del articulo !!!")
    
    fechaLimpia = t[1]+'/'+mes+'/'+t[5]+' '+t[7]+' '+t[8]
    
    return fechaLimpia
