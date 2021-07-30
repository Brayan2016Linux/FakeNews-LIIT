#!/usr/bin/python3
# -*- coding: utf-8 -*-

# =============================================================================
# Readability adaptación de legibilidad de A Muñoz F.
# =============================================================================
#
# Calcula la complejidad de un texto, basado es algoritmos de A Muñoz F.
# @Author: Brayan Rodriguez <bradrd2009jp@gmail.com>
# @Organization: LIIT-UNED 2021
# @Version: 0.0.1
# Miércoles 21 de julio de 2021

# ============================================================================
# Librerías
# ============================================================================

import numpy as np
import scipy as sc
import pandas as pd

import re
import statistics

#=========================Convertidor de cifras a letras =========================
# Implementado por AxiaCore.
# https://github.com/Axiacore/number-to-letters
# Siguiendo los cambios de A Muñoz F. (2016)
# https://github.com/amunozf/cifra-a-texto/blob/master/nal.py
# ================================================================================
UNIDADES = ( '','UN ','DOS ','TRES ','CUATRO ','CINCO ','SEIS ', 'SIETE ','OCHO ',
            'NUEVE ','DIEZ ','ONCE ','DOCE ','TRECE ','CATORCE ','QUINCE ','DIECISEIS ',
            'DIECISIETE ','DIECIOCHO ','DIECINUEVE ','VEINTE ')

DECENAS = ('VENTI','TREINTA ','CUARENTA ','CINCUENTA ','SESENTA ','SETENTA ',
          'OCHENTA ','NOVENTA ','CIEN ')

CENTENAS = ('CIENTO ', 'DOSCIENTOS ', 'TRESCIENTOS ', 'CUATROCIENTOS ', 'QUINIENTOS ',
    'SEISCIENTOS ', 'SETECIENTOS ', 'OCHOCIENTOS ', 'NOVECIENTOS ')

UNITS = (('',''), ('MIL ','MIL '), ('MILLON ','MILLONES '), ('MIL MILLONES ','MIL MILLONES '),
        ('BILLON ','BILLONES '), ('MIL BILLONES ','MIL BILLONES '),('TRILLON ','TRILLONES '),
        ('MIL TRILLONES','MIL TRILLONES'), ('CUATRILLON','CUATRILLONES'), 
        ('MIL CUATRILLONES','MIL CUATRILLONES'), ('QUINTILLON','QUINTILLONES'),
        ('MIL QUINTILLONES','MIL QUINTILLONES'), ('SEXTILLON','SEXTILLONES'),
        ('MIL SEXTILLONES','MIL SEXTILLONES'), ('SEPTILLON','SEPTILLONES'),
        ('MIL SEPTILLONES','MIL SEPTILLONES'), ('OCTILLON','OCTILLONES'),
        ('MIL OCTILLONES','MIL OCTILLONES'), ('NONILLON','NONILLONES'),
        ('MIL NONILLONES','MIL NONILLONES'), ('DECILLON','DECILLONES'),
        ('MIL DECILLONES','MIL DECILLONES'), ('UNDECILLON','UNDECILLONES'),
        ('MIL UNDECILLONES','MIL UNDECILLONES'), ('DUODECILLON','DUODECILLONES'),
        ('MIL DUODECILLONES','MIL DUODECILLONES'),)

MONEDAS = (
    {'country': 'Colombia', 'currency': 'COP', 'singular': 'PESO COLOMBIANO', 'plural': 'PESOS COLOMBIANOS', 'symbol': '$'},
    {'country': 'Estados Unidos', 'currency': 'USD', 'singular': 'DÓLAR', 'plural': 'DÓLARES', 'symbol': 'US$'},
    {'country': 'Europa', 'currency': 'EUR', 'singular': 'EURO', 'plural': 'EUROS', 'symbol': '€', 'decimalsingular':'Céntimo','decimalplural':'Céntimos'},
    {'country': 'México', 'currency': 'MXN', 'singular': 'PESO MEXICANO', 'plural': 'PESOS MEXICANOS', 'symbol': '$'},
    {'country': 'Perú', 'currency': 'PEN', 'singular': 'NUEVO SOL', 'plural': 'NUEVOS SOLES', 'symbol': 'S/.'},
    {'country': 'Costa Rica', 'currency': 'CRC', 'singular': 'COLON COSTARRICENSE', 'plural': 'COLONES OSTARRICENCES', 'symbol': '¢'},
    {'country': 'Reino Unido', 'currency': 'GBP', 'singular': 'LIBRA', 'plural': 'LIBRAS', 'symbol': '£'}
)

def hundreds_word(number):
    """Converts a positive number less than a thousand (1000) to words in Spanish
    Args:
        number (int): A positive number less than 1000
    Returns:
        A string in Spanish with first letters capitalized representing the number in letters
    Examples:
        >>> to_word(123)
        'Ciento Ventitres'
    """
    converted = ''
    if not (0 < number < 1000):
        return 'No es posible convertir el numero a letras'

    number_str = str(number).zfill(9)
    cientos = number_str[6:]

    if(cientos):
        if(cientos == '001'):
            converted += 'UN '
        elif(int(cientos) > 0):
            converted += '%s ' % __convert_group(cientos)

    return converted.title().strip()


def __convert_group(n):
    """Turn each group of numbers into letters"""
    output = ''

    if(n == '100'):
        output = "CIEN "
    elif(n[0] != '0'):
        output = CENTENAS[int(n[0]) - 1]

    k = int(n[1:])
    if(k <= 20):
        output += UNIDADES[k]
    else:
        if((k > 30) & (n[2] != '0')):
            output += '%sY %s' % (DECENAS[int(n[1]) - 2], UNIDADES[int(n[2])])
        else:
            output += '%s%s' % (DECENAS[int(n[1]) - 2], UNIDADES[int(n[2])])

    return output


def to_word(number, mi_moneda=None):

    """Converts a positive number less than:
    (999999999999999999999999999999999999999999999999999999999999999999999999)
    to words in Spanish
    Args:
        number (int): A positive number less than specified above
        mi_moneda(str,optional): A string in ISO 4217 short format
    Returns:
        A string in Spanish with first letters capitalized representing the number in letters
    Examples:
        >>> number_words(53625999567)
        'Cincuenta Y Tres Mil Seiscientos Venticinco Millones Novecientos Noventa Y Nueve Mil Quinientos Sesenta Y Siete'
    
        >>>> number_words(1481.01, 'EUR')
        'Mil Cuatrocientos Ochenta Y Un Euros con Un Céntimo'
    """
    if mi_moneda != None:
        try:
            moneda = filter(lambda x: x['currency'] == mi_moneda, MONEDAS).next()
            if int(number) == 1:
                entero = moneda['singular']
            else:
                entero = moneda['plural']
                if round(float(number) - int(number), 2) == float(0.01):
                    fraccion = moneda['decimalsingular']
                else:
                    fraccion = moneda['decimalplural']

        except:
            return "Tipo de moneda inválida"
    else:
        entero = ""
        fraccion = ""

    human_readable = []
    human_readable_decimals = []
    num_decimals ='{:,.2f}'.format(round(number,2)).split('.') #Sólo se aceptan 2 decimales
    num_units = num_decimals[0].split(',')
    num_decimals = num_decimals[1].split(',')
    #print num_units
    for i,n in enumerate(num_units):
        if int(n) != 0:
            words = hundreds_word(int(n))
            units = UNITS[len(num_units)-i-1][0 if int(n) == 1 else 1]
            human_readable.append([words,units])
    for i,n in enumerate(num_decimals):
        if int(n) != 0:
            words = hundreds_word(int(n))
            units = UNITS[len(num_decimals)-i-1][0 if int(n) == 1 else 1]
            human_readable_decimals.append([words,units])

    #filtrar MIL MILLONES - MILLONES -> MIL - MILLONES
    for i,item in enumerate(human_readable):
        try:
            if human_readable[i][1].find(human_readable[i+1][1]):
                human_readable[i][1] = human_readable[i][1].replace(human_readable[i+1][1],'')
        except IndexError:
            pass
    human_readable = [item for sublist in human_readable for item in sublist]
    human_readable.append(entero)
    for i,item in enumerate(human_readable_decimals):
        try:
            if human_readable_decimals[i][1].find(human_readable_decimals[i+1][1]):
                human_readable_decimals[i][1] = human_readable_decimals[i][1].replace(human_readable_decimals[i+1][1],'')
        except IndexError:
            pass
    human_readable_decimals = [item for sublist in human_readable_decimals for item in sublist]
    human_readable_decimals.append(fraccion)
    sentence = ' '.join(human_readable).replace('  ',' ').title().strip()
    if sentence[0:len('un mil')] == 'Un Mil':
        sentence = 'Mil' + sentence[len('Un Mil'):]
    if num_decimals != ['00']:
        sentence = sentence + ' con ' + ' '.join(human_readable_decimals).replace('  ',' ').title().strip()
    return sentence


#=========================Separador de sílabas ===================================
# Implementado por A Muñoz F. (2016)
# https://github.com/amunozf/separasilabas/blob/master/separasilabas.py
# ================================================================================

class char:
    def __init__(self):
        pass
    
class char_line:
    def __init__(self, word):
        self.word = word
        self.char_line = [(char, self.char_type(char)) for char in word]
        self.type_line = ''.join(chartype for char, chartype in self.char_line)
        
    def char_type(self, char):
        if char in set(['a', 'á', 'e', 'é','o', 'ó', 'í', 'ú']):
            return 'V' #strong vowel
        if char in set(['i', 'u', 'ü']):
            return 'v' #week vowel
        if char=='x':
            return 'x'
        if char=='s':
            return 's'
        else:
            return 'c'
            
    def find(self, finder):
        return self.type_line.find(finder)
        
    def split(self, pos, where):
        return char_line(self.word[0:pos+where]), char_line(self.word[pos+where:])
    
    def split_by(self, finder, where):
        split_point = self.find(finder)
        if split_point!=-1:
            chl1, chl2 = self.split(split_point, where)
            return chl1, chl2
        return self, False
     
    def __str__(self):
        return self.word
    
    def __repr__(self):
        return repr(self.word)

class silabizer:
    def __init__(self):
        self.grammar = []
        
    def split(self, chars):
        rules  = [('VV',1), ('cccc',2), ('xcc',1), ('ccx',2), ('csc',2), ('xc',1), ('cc',1), ('vcc',2), ('Vcc',2), ('sc',1), ('cs',1),('Vc',1), ('vc',1), ('Vs',1), ('vs',1)]
        for split_rule, where in rules:
            first, second = chars.split_by(split_rule,where)
            if second:
                if first.type_line in set(['c','s','x','cs']) or second.type_line in set(['c','s','x','cs']):
                    #print 'skip1', first.word, second.word, split_rule, chars.type_line
                    continue
                if first.type_line[-1]=='c' and second.word[0] in set(['l','r']):
                    continue
                if first.word[-1]=='l' and second.word[-1]=='l':
                    continue
                if first.word[-1]=='r' and second.word[-1]=='r':
                    continue
                if first.word[-1]=='c' and second.word[-1]=='h':
                    continue
                return self.split(first)+self.split(second)
        return [chars]
        
    def __call__(self, word):
        return self.split(char_line(word))


# ===========================================================================================
# Clase: Readability basada en:
# Gallego, Alejandro. Análisis de algoritmos para determinar el nivel de complejidad de 
# textos sanitarios y recomendaciones para mejorar el empoderamiento de un paciente. Tesis, Valencia, 
# España: Escuela Técnica Superior de Ingenieros de Telecomunicación de la Universitat Politècnica     
# de València. Universidad Politécnica de Valencia, 2017.
# https://riunet.upv.es/handle/10251/91777
# Repositorio:
# https://github.com/amunozf/legibilidad/blob/master/legibilidad.py
# ============================================================================================

class readability:
    def __init__(self, text):
        self.text = text

        #Cálculos preliminares:
        self.count_all_syllables_N2W = self.count_all_syllables(self.numbers2words(self.text))
        self.num_words_N2W = self.count_words(self.numbers2words(self.text))

        self.num_syllables = self.count_all_syllables(self.text) 
        self.num_sentences = self.count_sentences(self.text)  
        self.num_letters = self.count_letters(self.text)
        self.num_words = self.count_words(self.text)

        #Indices, tuplas o valores:
        self.fernandez_huerta_score = self.fernandez_huerta()
        self.inflesz_score = self.inflesz()
        self.szigriszt_pazos_score = self.szigriszt_pazos()
        self.gutierrez_score = self.gutierrez()
        self.munoz_score = self.munoz()
        self.crawford_score = self.crawford()

        #Texto para página web:
        self.fernandez_huerta_score_web = self.fernandez_huerta_score_w()
        self.inflesz_score_web = self.inflesz_score_w()
        self.szigriszt_pazos_score_web = self.szigriszt_pazos_score_w()
        self.gutierrez_score_web = self.gutierrez_score_w()
        self.mu_score_web = self.mu_score_w()
        self.crawford_score_web = self.crawford_score_w()
        self.count_score_web = self.general_count_w()
        

    #============================== Counter letters, words, sentences, paragraph =============

    def count_letters(self, text):
        """Contador de letras en un texto"""
        count = 0
        for char in text:
            if char.isalpha():
                count += 1
        if count == 0:
            count = 1
        return count

    def letter_dict(self, text):
        """Diccionario de cuenta letras"""
        text = text.lower()
        replacements = {'á': 'a','é': 'e','í': 'i','ó': 'o','ú': 'u','ü': 'u'}
        for i, j in replacements.items():
            text = text.replace(i, j)
        letterlist = list(filter(None,map(lambda c: c if c.isalpha() else '', text)))
        letterdict = dict()
        for letter in letterlist:
            letterdict[letter] = letterdict.get(letter,0) + 1
        return letterdict

    def count_words(self, text):
        """Contador de palabras"""
        count = 1
        text = ''.join(filter(lambda x: not x.isdigit(), text))
        clean = re.compile('\W+')
        text = clean.sub(' ', text).strip()
        if len(text.split()) > 0:
            count = len(text.split())
        return count

    def textdict(self, wordlist):
        """Diccionario de palabras contadas"""
        wordlist = ''.join(filter(lambda x: not x.isdigit(), wordlist))
        clean = re.compile('\W+')
        wordlist = clean.sub(' ', wordlist).strip()
        wordlist = wordlist.split()
        # Word count dictionary
        worddict = dict()
        for word in wordlist:
            worddict[word.lower()] = worddict.get(word,0) + 1
        return worddict

    def count_sentences(self, text):
        """Contador de oraciones"""
        text = text.replace("\n","")
        count = 1
        sentence_end = re.compile('[.:;!?\)\()]')
        sentences=sentence_end.split(text)
        sentences = list(filter(None, sentences))
        if len(sentences) > 0:
            count = len(sentences)
        return count


    def count_paragraphs(self, text):
        """Contador de párrafos"""
        count = 1
        text = re.sub('<[^>]*>', '', text)
        text = list(filter(None, text.split('\n')))
        if len(text) > 0:
            count = len(text)
        return count

    def numbers2words(self, text):
        """Convierte cifras en palabras""" 
        new_text = []
        for word in text.split():
            formato_numerico = re.compile("^[\-]?[1-9][0-9]*\.?[0-9]+$")
            if re.match(formato_numerico,word):
                if type(word) == "int":
                    word = int(word)
                else:
                    word = float(word)
                word = to_word(word)  #convierte números a palabras
            new_text.append(word.lower())
        
        text = ' '.join(new_text)
        return text

    def count_syllables(self, word):
        """Cuenta las sílabas de una plabra"""
        word = re.sub(r'\W+', '', word)
        syllables = silabizer()
        return len(syllables(word))

    def count_all_syllables(self, text):
        """Cuenta todas las sílabas del texto"""
        text = ''.join(filter(lambda x: not x.isdigit(), text))
        clean = re.compile('\W+')
        text = clean.sub(' ', text).strip()
        text = text.split()
        text = filter(None, text)
        total = 0
        for word in text:
            total += self.count_syllables(word)
        if total == 0:
            total = 1
        return total

    # ================================== Índices y Métricas ============================

    #Fernández Huerta
    def Pval(self):
        """Calcula la media de sílabas por palabra (P)"""
        syllables = self.count_all_syllables_N2W
        words = self.num_words_N2W
        #syllables = self.num_syllables #Calibrado con las métricas
        #words = self.num_words
        return round(syllables / words,2)

    def Fval(self):
        """Calcula la media de palabras por oración (F)"""
        sentences = self.num_sentences
        words = self.num_words_N2W
        #words = self.num_words
        return round(words / sentences,2)

    def fernandez_huerta(self):
        """Calcula el índice de legibilidad de Fernandez Huerta 1959"""
        fernandez_huerta = 206.84 - 60*self.Pval() - 1.02*self.Fval()
        return round(fernandez_huerta,2)

    #INFLESZ:
    """Fuente-Cortez, Beatriz E. de la, & García-Vielma, Catalina. (2021). Análisis de legibilidad de   
       formatos de consentimiento informado para pruebas genéticas en México. Gaceta médica de México, 
       157(1), 55-59. Epub 18 de junio de 2021.https://doi.org/10.24875/gmm.20000087
    """

    def inflesz(self):
        """Calcula el índice de legibilidad de INFLESZ, Barrio-Cantalejo 2003"""
        inflesz = 206.835 - 62.35 * (self.num_syllables / self.num_words) - (self.num_words / self.num_sentences)
        return round(inflesz,2)

    #Szigriszt-pazos
    def szigriszt_pazos(self):
        """Calcula el índice de legibilidad Szigriszt Pazos 1992"""
        sp = 206.835 - 62.3 * (self.count_all_syllables_N2W / self.num_words_N2W) - (self.num_words_N2W / self.num_sentences)
        return round(sp,2)

    #Gutiérrez
    def gutierrez(self):
        """Índice de legibilidad de Gutiérrez de Polini (1972)"""
        legibguti = 95.2 - 9.7 * (self.num_letters / self.num_words) - 0.35 * (self.num_words / self.num_sentences) 
        return round(legibguti, 2)

    #Muñoz Baquedano y Muñoz Urra
    def munoz(self):
        """Índice de legibilidad de Muñoz Baquedano y Muñoz Urra (2006)"""
        n = self.num_words
        # Delete all digits
        text = ''.join(filter(lambda x: not x.isdigit(), self.text))
        # Cleans it all
        clean = re.compile('\W+')
        text = clean.sub(' ', text).strip()
        text = text.split() # word list
        word_lengths = []
        for word in text:
            word_lengths.append(len(word))
        # The mean calculation needs at least 1 value on the list, and the variance, two. If somebody enters only one word or, what is worse, a figure, the calculation breaks, so this is a 'fix'
        try:
            mean = statistics.mean(word_lengths)
            variance = statistics.variance(word_lengths)
            mu = (n / (n - 1)) * (mean / variance) * 100
            return round(mu, 2)
        except:
            return 0
    
    #Crawford  
    def crawford(self):
        """Fórmula de legibilidad de Crawford, años de escuela necesarios para entender el texto"""
        sentences = self.num_sentences
        words = self.num_words_N2W
        syllables = self.count_all_syllables_N2W
        SeW = 100 * sentences / words # number of sentences per 100 words (mean)
        SiW = 100 * syllables / words # number of syllables in 100 words (mean)
        years = -0.205 * SeW + 0.049 * SiW - 3.407
        years = round(years,2)
        return years

    # ================================== Interpretación ============================

    def fernandez_huerta_readability_score(self):
        """
        Return fernandez_huerta interpretation readability score:
        ---------------
        input:
            readability: value of readability of a text
        output:
            tuple in spanish: ('Nivel', 'Grado escolar')
        """
        readability = self.fernandez_huerta_score
        readability_score = ('','')

        if readability < 30:
            readability_score = ('muy difícil', 'especializado')
        elif readability >= 30 and readability < 50:
            readability_score = ('difícil', 'cursos selectivos')
        elif readability >= 50 and readability < 60:
            readability_score = ('algo difícil', 'preuniversitario')
        elif readability >= 60 and readability < 70:
            readability_score = ('normal', '7 - 8 grado')
        elif readability >= 70 and readability < 80:
            readability_score = ('algo fácil', '6 grado')
        elif readability >= 80 and readability < 90:
            readability_score = ('fácil', '5 grado')
        else:
            readability_score = ('muy fácil', '4 grado')

        return readability_score

    def szigriszt_pazos_readability_score(self):
        """
        Return szigriszt interpretation pazos readability score:
        ---------------
        input:
            readability: value of readability of a text
        output:
            level in spanish
        """
        readability = self.szigriszt_pazos_score
        readability_score = ''

        if readability <= 15:
            readability_score = 'muy difícil'
        elif readability > 15 and readability <= 35:
            readability_score = 'árido'
        elif readability > 35 and readability <= 50:
            readability_score = 'bastante difícil'
        elif readability > 50 and readability <= 65:
            readability_score = 'normal'
        elif readability > 65 and readability <= 75:
            readability_score = 'bastante fácil'
        elif readability > 75 and readability <= 85:
            readability_score = 'fácil'
        else:
            readability_score = 'mMuy fácil'

        return readability_score


    def inflesz_readability_score(self):
        """
        Return inflesz interpretation readability score:
        ---------------
        input:
            readability: value of readability of a text
        output:
            tuple in spanish: ('Nivel', 'Grado escolar')
        """
        readability = self.szigriszt_pazos_score
        readability_score = ('', '')

        if readability <= 40:
            readability_score = ('muy difícil', 'universitario-científico')
        elif readability > 40 and readability <= 55:
            readability_score = ('algo difícil','bachilletaro-divulgación')
        elif readability > 55 and readability <= 65:
            readability_score = ('normal','prensa general-deportiva')
        elif readability > 65 and readability <= 80:
            readability_score = ('bastante fácil','textos de primaria-novela')
        else:
            readability_score = ('muy fácil','educación primaria-cómics')

        return readability_score


    def gutierrez_readability_score(self):
        """
        Return Gutierrez interpretation readability score:
        ---------------
        input:
            readability: value of readability of a text
        output:
            level in spanish
        """
        readability = self.gutierrez_score
        readability_score = ''

        if readability <= 33.33:
            readability_score = 'difícil'
        elif readability > 33.33 and readability <= 66.66:
            readability_score = 'normal'
        else:
            readability_score = 'fácil'

        return readability_score


    def munoz_readability_score(self):
        """
        Return Muñoz and Muñoz interpretation readability score:
        ---------------
        input:
            readability: value of readability of a text
        output:
            level in spanish
        """
        readability = self.munoz_score
        readability_score = ''

        if readability < 31:
            readability_score = 'muy difícil'
        elif readability >= 31 and readability < 51:
            readability_score = 'difícil'
        elif readability >= 51 and readability < 61:
            readability_score = 'un poco difícil'
        elif readability >= 61 and readability < 71:
            readability_score = 'adecuado'
        elif readability >= 71 and readability < 81:
            readability_score = 'un poco fácil'
        elif readability >= 81 and readability < 91:
            readability_score = 'fácil'
        else:
            readability_score = 'muy fácil'

        return readability_score


    # ============================== Análisis de texto ===============================

    def general_count_w(self):
        output_score = 'Número de sílabas: %s. Número de palabras: %s. Número de oraciones: %s'%(self.num_syllables,self.num_words,self.num_sentences)
        return output_score

    def fernandez_huerta_score_w(self):
        #Fernandez Huerta:
        output_score = ''
        fh = self.fernandez_huerta_score
        readability_fh = self.fernandez_huerta_readability_score()
        output_score += 'Índice Fernandez Huerta: %0.2f. Nivel: %s. Grado escolar: %s. '%(fh, readability_fh[0], readability_fh[1])
        return output_score
        
    def szigriszt_pazos_score_w(self):
        #Szigriszt_pazos
        output_score = ''
        sp = self.szigriszt_pazos_score
        readability_sp = self.szigriszt_pazos_readability_score()
        output_score += 'Índice Szigriszt_Pazos: %0.2f. Nivel: %s.\n'%(sp, readability_sp)
        return output_score  

    def inflesz_score_w(self):
        #Inflesz:
        output_score = ''
        inflesz_score = self.inflesz_score
        readability_in = self.inflesz_readability_score()
        output_score += 'Índice Inflesz: %0.2f. Nivel: %s. Grado: %s.\n'%(inflesz_score, readability_in[0], readability_in[1])
        return output_score

    def mu_score_w(self):
        #Muñoz & Muñoz:
        output_score = ''
        mu = self.munoz_score
        readability_mu = self.munoz_readability_score()
        output_score += 'Índice Muñoz Baquedano and Muñoz Urra (mu): %0.2f. Nivel: %s.\n'%(mu, readability_mu)
        return output_score

    def gutierrez_score_w(self):
        #Gutierrez
        output_score = ''
        g = self.gutierrez_score
        readability_g = self.gutierrez_readability_score()
        output_score += 'Índice Gutiérrez: %0.2f. Nivel: %s.\n'%(g, readability_g)
        return output_score

    def crawford_score_w(self):
        #Crawford:
        output_score = ''
        c = self.crawford_score
        output_score += 'Índice de Crawford: se requieren %0.2f años de escolaridad para entender el texto.'%c
        return output_score
   

if __name__ == '__main__':
    print("Módulo de Legibilidad")
    
    TextoDePrueba = '''
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam id erat vitae ligula semper pellentesque. Vestibulum vel rhoncus ex. Vivamus ut elit vel est tempus eleifend venenatis et nunc. Nam varius interdum lorem eu hendrerit. Integer sed suscipit felis. Vivamus felis ligula, semper id ipsum vitae, placerat rutrum lectus. Nunc ullamcorper consequat urna, in finibus metus sollicitudin eget. Maecenas mollis tincidunt diam sed facilisis. Vestibulum malesuada quam in ex malesuada bibendum. In hac habitasse platea dictumst. Maecenas maximus volutpat enim, vitae euismod nulla vulputate eget. Mauris eget pellentesque arcu. Etiam molestie nunc a lorem gravida imperdiet. 
'''

    # Muestra la lecturabilidad
    rd = readability(TextoDePrueba)
    print(rd.fernandez_huerta_score_web)
    print(rd.inflesz_score_web)
    print(rd.crawford_score_web)
    print(rd.gutierrez_score_web)
    print(rd.szigriszt_pazos_score_web)
    print(rd.mu_score_web)
    print(rd.count_score_web)
    

