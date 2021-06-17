import bs4
import Herramientas
from Articulo import Articulo
import requests
import json
from bs4 import BeautifulSoup

class CRHoy:
    site_name="crhoy.com"
    articulos = [] 
    links = []
    
    
    def scrap(self):
        
        try:
            r = Herramientas.get_especial('https://www.crhoy.com/site/dist/json/index2.json?v=')
            j = json.loads(r)
            for x in range (0,4) :
                self.links.append(j['slider'][x]['url'])

            for x in range(0,3):
                self.links.append(j['visualB'][x]['url'])

            for x in range(0,3):
                self.links.append(j['visualA'][x]['url'])

            for x in range(0,3):
                self.links.append(j['visualC'][x]['url'])
            
            for x in range(0,3):
                self.links.append(j['entretenimiento'][x]['url'])
            
            for x in range(0,3):
                self.links.append(j['deportes'][x]['url'])
            
            for x in range(0,3):
                self.links.append(j['enterese'][x]['url'])
           
            self.links = list(dict.fromkeys(self.links)) # Elimina duplicados

            for link in self.links :
                title=""
                text=""
                url=link
                published_date=""
                try:

                    info1 = Herramientas.get_especial(link)
                    sou = BeautifulSoup(info1, 'html.parser')
                    contenidos =sou.find('div', attrs={'class': 'contenido'})
                     
                    for p in contenidos.find_all( ['p', 'h2', 'h1'] , attrs={'class':None}):
                        if not ( p.parent is not None and p.parent.parent is not None and p.parent.parent.parent is not None and (p.parent.parent.parent)['class'][0] == 'leerMasOuter' ):
                            
                            
                            parrafo=""
                            for p2 in  p.contents:
                                if type(p2) is bs4.element.NavigableString :
                                    parrafo = parrafo + p2
                                else:
                                    if not p2.has_attr('class'):
                                        parrafo = parrafo + p2.getText()
                            
                            text = text + parrafo + " "
                        
                        

                    # Titulo
                    titulo = sou.find('h1', attrs={'class': 'text-left titulo'})
                    title = titulo.text.replace('\n', '')
                    
                    try:
                        date = sou.find('span', attrs={'class', 'fecha-nota'})
                        published_date = limpiarFecha(str(date.string))
                    except Exception as e:
                        published_date = None
                        err = str(e) + "-CRHOY-" + str(link) + "No se logro obtener la fecha del articulo !"
                        print(err+"\nNo se logro obtener la fecha del articulo !")
                    self.articulos.append(Articulo(self.site_name,title,text,url,published_date))
                except Exception as e:
                    err = str(e) + "-CRHOY-" + str(link) + "---"
                    print(err)
                
        except Exception as e:
            err = str(e) + "-CRHOY-"
            print(err)

def limpiarFecha(fecha):

        t = fecha.split()
        if t[0] == 'Enero':
            mes = '01'
        elif t[0] == 'Febrero':
            mes = '02'
        elif t[0] == 'Marzo':
            mes = '03'
        elif t[0] == 'Abril':
            mes = '04'
        elif t[0] == 'Mayo':
            mes = '05'
        elif t[0] == 'Junio':
            mes = '06'
        elif t[0] == 'Julio':
            mes = '07'
        elif t[0] == 'Agosto':
            mes = '08'
        elif t[0] == 'Septiembre':
            mes = '09'
        elif t[0] == 'Octubre':
            mes = '10'
        elif t[0] == 'Noviembre':
            mes = '11'
        elif t[0] == 'Diciembre':
            mes = '12'
        else:
            mes='00'
            print("Error con el Mes de la fecha extraida del articulo !!!")
        dia = t[1].replace(',', '')
        fechaLimpia = dia+'/'+mes+'/'+t[2]+' '+t[3]+' '+t[4]
        
        return fechaLimpia

