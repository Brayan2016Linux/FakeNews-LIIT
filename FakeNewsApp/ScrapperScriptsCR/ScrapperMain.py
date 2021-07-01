from .CRHoy import CRHoy
from .DiarioExtra import DiarioExtra
from .Monumental import Monumental
from .Nacion import Nacion
from .Repretel import Repretel
from .PrensaLibre import PrensaLibre
from .Seminario import Seminario
from .ElFinanciero import ElFinanciero
from .AmeliaRueda import AmeliaRueda
from .Teletica import Teletica
from .Herramientas import *


def scrapAll():
    total = 0

    total += scrapCRHoy()
    total += scrapDiarioExtra()
    total += scrapMonumental()
    total += scrapNacion()
    total += scrapPrensaLibre()
    total += scrapRepretel()
    total += scrapSeminario()
    total += scrapElFinanciero()
    total += scrapAmeliaRueda()
    total += scrapTeletica()
    print("Total de articulos: "+str(total))
    

def scrapCRHoy():
    crHoy = CRHoy()
    crHoy.scrap()
    for c in crHoy.articulos:
        c.printTitle()
    return crHoy.articulos

def scrapDiarioExtra():
    diarioExtra = DiarioExtra()
    diarioExtra.scrap()
    for d in diarioExtra.articulos:
        d.printTitle()
    return len(diarioExtra.articulos)

def  scrapMonumental():
    monumental = Monumental()
    monumental.scrap()
    for m in monumental.articulos:
        m.printTitle()
    return len(monumental.articulos)

def scrapNacion():
    nacion = Nacion()
    nacion.scrap()
    for n in nacion.articulos:
        n.printTitle()
    return len(nacion.articulos)

def scrapRepretel():
    repretel = Repretel()
    repretel.scrap()
    for r in repretel.articulos:
        r.printTitle()
    return len(repretel.articulos)

def scrapPrensaLibre():
    prensaLibre = PrensaLibre()
    prensaLibre.scrap()
    for p in prensaLibre.articulos:
        p.printTitle()
    return len(prensaLibre.articulos)

def scrapSeminario():
    seminario = Seminario()
    seminario.scrap()
    for s in seminario.articulos:
        s.printTitle()
    return len(seminario.articulos)

def scrapElFinanciero():
    elFinanciero = ElFinanciero()
    elFinanciero.scrap()
    for n in elFinanciero.articulos:
        n.printTitle()
    return len(elFinanciero.articulos)

def scrapAmeliaRueda():
    ameliaRueda = AmeliaRueda()
    ameliaRueda.scrap()
    for n in ameliaRueda.articulos:
        n.printTitle()
    return len(ameliaRueda.articulos)

def scrapTeletica():
    teletica = Teletica()
    teletica.scrap()
    for n in teletica.articulos:
        n.printTitle()
    return teletica.articulos
    


