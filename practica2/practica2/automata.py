#-*-encoding:utf8-*-
import re
from practica2.core.models import Retrato

class analizar_texto:
    def __init__(self):
        self.letra_actual = ''
        self.estado_actual = 0
        self.valor_lexema = ''
        self.operadores = ['+','-','*','x','.','^']
        self.punt = [',',':',';','.']
        self.aceptacion = True
        self.reserv = ['teorema','Teorema','Matemático','matemático','Matemática','matemática',
        'Hilbert','Turing','Análisis','análisis','Euler','Fermat','Pitágoras','Autómata','autómata','Boole',
        'Cantor','Perelman','Experimentación','experimentación','Físico','físico','Física','física',
        'Astronomía','astronomía','Mecánica','mecánica','Newton','Einstein','Galileo','Modelo','modelo',
        'Tesla','Dinámica','dinámica','Partículas','partículas']
        self.log = ''
        self.imatch = 0
        self.lmatch = []

    def switch(self, estado):
        self.estados = {
            0: self.estado_cero,
            1: self.estado_uno,
            2: self.estado_dos,
            3: self.estado_tres,
            4: self.estado_cuatro,
            5: self.estado_cinco,
            6: self.estado_seis,
            7: self.estado_siete,
            8: self.estado_ocho,
            9: self.estado_nueve,
            10: self.estado_diez,
            11: self.estado_once,
            12: self.estado_doce,
            13: self.estado_trece,
            14: self.estado_catorce,
            15: self.estado_quince,
            16: self.estado_dieciseis,
        }

        func = self.estados.get(estado, lambda: 'No es un caracter válido')
        return func()

    def valuar_dato(self, dato):
        try:
            int(dato)
            return True
        except ValueError:
            return False
    
    def estado_cero(self):
        if self.valuar_dato(self.letra_actual) == False:
            if str(self.letra_actual) == self.operadores[1]:
                self.estado_actual = 1
                self.valor_lexema = self.valor_lexema + self.letra_actual
            else:
                self.estado_actual = 16
                self.valor_lexema = self.valor_lexema + self.letra_actual
        else:
            if int(self.letra_actual) >= 0:
                self.estado_actual = 2
                self.valor_lexema = self.valor_lexema + self.letra_actual
            else:
                self.aceptacion = False
                self.print_log ('Cadena no aceptada')
    
    def estado_uno(self):
        if self.valuar_dato(self.letra_actual) == True:
            if int(self.letra_actual) >= 0:
                self.estado_actual = 2
                self.valor_lexema = self.valor_lexema + self.letra_actual
            else:
                self.aceptacion = False
                self.print_log ('Cadena no aceptada')
        else:
            self.estado_actual = 16
            self.valor_lexema = self.valor_lexema + self.letra_actual

    def estado_dos(self):
        if self.valuar_dato(self.letra_actual) == False:
            if str(self.letra_actual) == self.operadores[4]:
                self.estado_actual = 3
                self.valor_lexema = self.valor_lexema + self.letra_actual
            elif str(self.letra_actual) == self.operadores[2] or str(self.letra_actual) == self.operadores[3]:
                self.estado_actual = 4
                self.valor_lexema = self.valor_lexema + self.letra_actual
            elif str(self.letra_actual) == self.operadores[0] or str(self.letra_actual) == self.operadores[1]:
                self.estado_actual = 5
                self.valor_lexema = self.valor_lexema + self.letra_actual
            elif str(self.letra_actual) == 'i':
                self.estado_actual = 11
                self.valor_lexema = self.valor_lexema + self.letra_actual
            elif str(self.letra_actual) == ' ':
                self.print_log ('Esto es un número entero '+ self.valor_lexema)
                self.aceptacion = False
            elif str(self.letra_actual) in self.punt:
                self.print_log ('Esto es un número entero '+ self.valor_lexema)
                self.aceptacion = False
            else:
                self.estado_actual = 16
                self.valor_lexema = self.valor_lexema + self.letra_actual
        else:
            self.estado_actual = 2
            self.valor_lexema = self.valor_lexema + self.letra_actual
            self.aceptacion = True
        
    def estado_tres(self):
        if self.valuar_dato(self.letra_actual) == True:
            if int(self.letra_actual) >= 0:
                self.estado_actual = 6
                self.valor_lexema = self.valor_lexema + self.letra_actual
            else:
                self.aceptacion = False
                self.print_log ('Cadena no aceptada')
        else:
            self.estado_actual = 16
            self.valor_lexema = self.valor_lexema + self.letra_actual

    def estado_cuatro(self):
        if self.valuar_dato(self.letra_actual) == True:
            if int(self.letra_actual) == 1:
                self.estado_actual = 7
                self.valor_lexema = self.valor_lexema + self.letra_actual
            else:
                self.aceptacion = False
                self.print_log ('Cadena no aceptada')
        else:
            self.estado_actual = 16
            self.valor_lexema = self.valor_lexema + self.letra_actual
    
    def estado_cinco(self):
        if self.valuar_dato(self.letra_actual) == True:
            if int(self.letra_actual) >=0:
                self.estado_actual = 8
                self.valor_lexema = self.valor_lexema + self.letra_actual
            else:
                self.aceptacion = False
                self.print_log ('Cadena no aceptada')
        else:
            self.estado_actual = 16
            self.valor_lexema = self.valor_lexema + self.letra_actual

    def estado_seis(self):
        if self.valuar_dato(self.letra_actual) == False:
            if str(self.letra_actual) == self.operadores[0] or str(self.letra_actual) == self.operadores[1]:
                self.estado_actual = 5
                self.valor_lexema = self.valor_lexema + self.letra_actual
            elif str(self.letra_actual) == self.operadores[2] or str(self.letra_actual) == self.operadores[3]:
                self.estado_actual = 4
                self.valor_lexema = self.valor_lexema + self.letra_actual
            elif str(self.letra_actual) == 'i':
                self.estado_actual = 11
                self.valor_lexema = self.valor_lexema + self.letra_actual
            elif str(self.letra_actual) == ' ':
                self.print_log ('Esto es un número real '+ self.valor_lexema)
                self.aceptacion = False
            elif str(self.letra_actual) in self.punt:
                self.print_log ('Esto es un número real '+ self.valor_lexema)
                self.aceptacion = False
            else:
                self.estado_actual = 16
                self.valor_lexema = self.valor_lexema + self.letra_actual
        else:
            self.estado_actual = 6
            self.valor_lexema = self.valor_lexema + self.letra_actual
            self.aceptacion = True
    
    def estado_siete(self):
        if self.valuar_dato(self.letra_actual) == True:
            if int(self.letra_actual) == 0:
                self.estado_actual = 9
                self.valor_lexema = self.valor_lexema + self.letra_actual
            else:
                self.aceptacion = False
                self.print_log ('Cadena no aceptada')
        else:
            self.estado_actual = 16
            self.valor_lexema = self.valor_lexema + self.letra_actual
    
    def estado_ocho(self):
        if self.valuar_dato(self.letra_actual) == False:
            if str(self.letra_actual) == self.operadores[4]:
                self.estado_actual = 10
                self.valor_lexema = self.valor_lexema + self.letra_actual
            elif str(self.letra_actual) == 'i':
                self.estado_actual = 11
                self.valor_lexema = self.valor_lexema + self.letra_actual
            else:
                self.estado_actual = 16
                self.valor_lexema = self.valor_lexema + self.letra_actual
        else:
            self.estado_actual = 8
            self.valor_lexema = self.valor_lexema + self.letra_actual
            self.aceptacion = True

    def estado_nueve(self):
        if self.valuar_dato(self.letra_actual) == False:
            if str(self.letra_actual) == self.operadores[5]:
                self.estado_actual = 12
                self.valor_lexema = self.valor_lexema + self.letra_actual
            else:
                self.estado_actual = 16
                self.valor_lexema = self.valor_lexema + self.letra_actual   
        else:
            self.aceptacion = False
            self.print_log ('Cadena no aceptada')

    def estado_diez(self):
        if self.valuar_dato(self.letra_actual) == True:
            if int(self.letra_actual) >= 0:
                self.estado_actual = 13
                self.valor_lexema = self.valor_lexema + self.letra_actual
            else:
                self.aceptacion = False
                self.print_log ('Cadena no aceptada')
        else:
            self.estado_actual = 16
            self.valor_lexema = self.valor_lexema + self.letra_actual

    def estado_once(self):
        if self.valuar_dato(self.letra_actual) == False:
            if str(self.letra_actual) == ' ':
                self.print_log ('Esto es un número complejo ',self.valor_lexema)
                self.aceptacion = False
            elif str(self.letra_actual) in self.punt:
                self.print_log ('Esto es un número complejo '+ self.valor_lexema)
                self.aceptacion = False
            else:
                self.estado_actual = 16
                self.valor_lexema = self.valor_lexema + self.letra_actual
        else:
            self.aceptacion = False
            self.print_log ('Cadena no aceptada')
    
    def estado_doce(self):
        if self.valuar_dato(self.letra_actual) == True:
            if int(self.letra_actual) >= 0:
                self.estado_actual = 14
                self.valor_lexema = self.valor_lexema + self. letra_actual
            else:
                self.aceptacion = False
                self.print_log ('Cadena no aceptada')
        else:
            if str(self.letra_actual) == self.operadores[1]:
                self.estado_actual = 15
                self.valor_lexema = self.valor_lexema + self.letra_actual
            else:
                self.estado_actual = 16
                self.valor_lexema = self.valor_lexema + self.letra_actual
    
    def estado_trece(self):
        if self.valuar_dato(self.letra_actual) == True:
            if int(self.letra_actual) >= 0:
                self.estado_actual = 13
                self.valor_lexema = self.valor_lexema + self.letra_actual
            else:
                self.aceptacion = False
                self.print_log ('Cadena no aceptada')
        else:
            if str(self.letra_actual) == 'i':
                self.estado_actual = 11
                self.valor_lexema = self.valor_lexema + self.letra_actual
            else:
                self.estado_actual = 16
                self.valor_lexema = self.valor_lexema + self.letra_actual
    
    def estado_catorce(self):
        if self.valuar_dato(self.letra_actual) == True:
            if int(self.letra_actual) >= 0:
                self.estado_actual = 14
                self.valor_lexema = self.valor_lexema + self.letra_actual
            else:
                self.aceptacion = False
                self.print_log ('Cadena no aceptada')
        else:
            if str(self.letra_actual) == ' ':
                self.print_log ('Número en notación científica '+ self.valor_lexema)
                self.aceptacion = False
            elif str(self.letra_actual) in self.punt:
                self.print_log ('Número en notación científica '+ self.valor_lexema)
            else:
                self.estado_actual = 16
                self.valor_lexema = self.valor_lexema + self.letra_actual
            
    def estado_quince(self):
        if self.valuar_dato(self.letra_actual) == True:
            if int(self.letra_actual) >= 0:
                self.estado_actual = 14
                self.valor_lexema = self.valor_lexema + self.letra_actual
            else:
                self.aceptacion = False
                self.print_log ('Cadena no aceptada')
        else:
            self.estado_actual = 16
            self.valor_lexema = self.valor_lexema + self.letra_actual

    def estado_dieciseis(self):
        if str(self.letra_actual) == ' ':
            if self.valor_lexema in self.reserv:
                self.print_log ('Esto es una palabra reservada '+ self.valor_lexema)
                self.aceptacion = False
            elif str(self.letra_actual) in self.punt:
                self.print_log ('Esto es unacadena '+ self.valor_lexema)
                self.aceptacion = False
            else:
                self.print_log ('Esto es una cadena '+ self.valor_lexema)
                self.aceptacion = False
        else:
            self.estado_actual = 16
            self.valor_lexema = self.valor_lexema + self.letra_actual
            self.aceptacion = True

    def analizar(self, cadena):
        cadena = str(cadena)
        palabras = cadena.split()
        for i in palabras:
            self.aceptacion = True
            self.valor_lexema = ""
            self.estado_acutal = 0
            i = i + ' '
            for x in i:
                if self.aceptacion == True:
                    self.letra_actual = x
                    self.switch(self.estado_actual)

###########################################################################################


    def print_log(self,mensaje):
        self.log += mensaje + '<br />'

    def get_log(self):
        return self.log

    def colorear_html(self, cadena):
        html = str(cadena)
        self.lmatch = []
        self.imatch = 0



        # fechas anaranjado
        fechas = re.findall(r'((\d{1,2}[-]\d{1,2}[-]\d{2})|(\d{1,2}/\d{1,2}/\d{2,4}))',html)
        html = re.sub(r'((\d{1,2}[-]\d{1,2}[-]\d{2})|(\d{1,2}/\d{1,2}/\d{2,4}))','~FECHA|',html)
        print('fechas:')
        print(fechas)

        # notacion cientifica morado
        ncientificas = re.findall(r'(?<!~)[-+]?[\d]+\.?[\d]*[Ee](?:[-+]?[\d]+)?',html)
        html = re.sub ('(?<!~)[-+]?[\d]+\.?[\d]*[Ee](?:[-+]?[\d]+)?','~NOTACIONC|',html)
        print('ncientificas:')
        print(ncientificas)
        print(html)

        # numero complejo rojo
        complejos = re.findall(r'[-+]?[\d]+\.?[\d]*[i]|[-+][i]',html)
        html = re.sub(r'[-+]?[\d]+\.?[\d]*[i]|[-+][i]','~COMPLEJO|',html)
        print('complejo:')
        print(complejos)

        # numero real verde
        reales = re.findall(r'[0-9]\.[0-9]+',html)
        html = re.sub (r'[0-9]\.[0-9]+','~REAL|',html)
        print('reales:')
        print(reales)

        # numero entero azul
        enteros = re.findall(r"(?<!~)[+-]?[0-9]+",str(html),re.M)
        print('enteros: ')
        print(enteros)
        html = re.sub(r"(?<!~)[+-]?[0-9]+",'~ENTERO|',html)
        
        print()

        print(html)
        # fechas anaranjado
        for fecha in fechas :
            if fecha[0] !='': html = html.replace('~FECHA|',self.agregar_color(str(fecha[0]),'orange'),1)
        # notacion cientifica morado
        for ncientifica in ncientificas : html = html.replace('~NOTACIONC|',self.agregar_color(str(ncientifica),'purple'),1)
        # numero complejo rojo
        for complejo in complejos : html = html.replace('~COMPLEJO|',self.agregar_color(str(complejo),'red'),1)
        # numero real verde
        for real in reales : html = html.replace('~REAL|',self.agregar_color(str(real),'green'),1)
        # numero entero azul
        for entero in enteros : html = html.replace('~ENTERO|',self.agregar_color(str(entero),'blue'),1)


        # palabras de interes gris
        for res in self.reserv:
            html = re.sub( res,self.agregar_color(res,'grey'),html,flags=re.I)

        # agregar retratos
        retratos = Retrato.objects.all()
        list_retratos = []
        for retrato in retratos:
            l = re.findall(retrato.nombre,str(html),re.I) 
            if l != []:  list_retratos.extend(l)
            for ret in l : html = html.replace(ret,self.agregar_color(str(ret),'darkgrey'),1)
        print('retratos:')
        print(list_retratos)
        print(html)
        
        
        print(list_retratos)

        # los saltos de linea
        html = re.sub(r'[\n]','<br />',html)

        # agregar retratos al final del documento
        html += "<br />"
        try:
            list_retratos = list(dict.fromkeys(list_retratos))
            print (list_retratos)
            for ret in list_retratos:
                retrato = Retrato.objects.filter(nombre__iexact=ret).first()
                html += '<img src="'+retrato.imagen.url+'" width="150px" height="auto" />'
            html += "<br />"
        except: 
            html += '<img src="" width="150px" height="auto" />'
            print("Una excepcion -----------")

        return html

    def agregar_color(self, cadena, color):
        return '<font color="'+color+'">'+cadena+'</font>'




