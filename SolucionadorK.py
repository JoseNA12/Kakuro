"""
José Navarro A.
Josué Suárez C.
Kakuro
2017
TEC
"""

#!/usr/bin/env python

import math
import sys
import logging
import hashlib
from tkinter import messagebox
from Memoize import Memoize
from multiprocessing import Process, Queue
import time
from queue import Queue

#from Hilo import Hilo
import threading

def ActivarHilos(estado):
    Solucionador.conHilos = estado

def DesactivarHilos(estado):
    Solucionador.conHilos = estado

def ActivarForks(estado):
    Solucionador.conForks = estado

def DesactivarForks(estado):
    Solucionador.conForks = estado

def EjecutarForkHilo(funcion):
    if (Solucionador.conHilos == False) & (Solucionador.conForks == False):
        funcion()

    else:
        if Solucionador.conHilos:
            for x in range(10):
                thread = threading.Thread(target=funcion)
                #thread.daemon = True
                thread.start()
                thread.join()
        else:
            if Solucionador.conForks:
                processes = Process(target=funcion)
                processes.start()


@Memoize
def ObtenerSumas(casillaLlave, cantidadCasillasBlancas): #restante, longitudCasillasBlancas
    """
    Devuelve una lista de todas las sumas de la casilla dependiendo
    de la cantidad de casillas blancas
    Incluirá todas las sumas posibles de coeficientes.
    """
    if cantidadCasillasBlancas == 2:

        # Crear una matriz de sumas que contendrá un par ordenado de la llave - 'x' y 'x'
        sumas = [
            [casillaLlave - x, x] for x in range(1, casillaLlave - 1)
            if casillaLlave - x != x and x < 10 and (casillaLlave - x) < 10]
            # menor a 10 porque a huevo el maximo de casillas blancas es 9

    else:
        sumas = []

        for x in range(1, casillaLlave - 1):
            sumas.extend( # .extend -> se necesita para unir los elementos del vector
                [suma + [x] for suma in ObtenerSumas(casillaLlave - x, cantidadCasillasBlancas - 1) if x not in suma and x < 10])

    return sumas


@Memoize
def ObtenerSumasUnicas(casillaLlave, cantidadCasillasBlancas):
    """
    Devuelve un conjunto de sumas dependiendo de la llave deacuerdo
    a la cantidad de casillas blancas disponibles.
    Dicho conjunto se ordena de manera ascendente.
    """
    sumas = ObtenerSumas(casillaLlave, cantidadCasillasBlancas)
    sumasUnicas = set()

    for suma in sumas:
        sumasUnicas.add(tuple(sorted(suma))) # Cada suma unica obtenida, almacenarla como una tupla en el vector

    return list(sumasUnicas)

def ObtenerCombinaciones(numeros):
    """
    Obtener todas las permutaciones posibles de números dado un vector que contiene numeros
    Comportamiento:
    Entrada: [1, 2, 4]
    - Combina: [2, 4] [1, 4] [1, 2]
    Retorna: [[2, 4, 1], [4, 2, 1], [1, 4, 2], [4, 1, 2], [1, 2, 4], [2, 1, 4]]
    """
    combos = []

    if len(numeros) == 2:
        return [[numeros[0], numeros[1]], [numeros[1], numeros[0]]]

    else:
        for numero in numeros:
            numero2 = numeros[:]  # Copie todos los elementos de numeros
            numero2.remove(numero)
            combos.extend([x + [numero] for x in ObtenerCombinaciones(numero2)])

    return combos


def ReestablecerAtributosClases():
    """
    Necesario para resolver kakuros de manera consecutiva.
    Cada vez que se procede a resolver un kakuro, deben estar "limpios"
    """
    Solucionador.solucion = {}
    Solucionador.soluciones = {}
    Solucionador.solucionesParciales = {}
    Solucionador.celdasHorizontales = {}
    Solucionador.celdasVerticales = {}
    Solucionador.celdasUnicas_V = []
    Solucionador.celdasUnicas_H = []
    Solucionador.ancho = 0
    Solucionador.alto = 0

    Celda.coordenadasModificadas = []
    Celda.suponerCoordsHorizontales = {}
    Celda.suponerCoordsVerticales = {}
    Celda.minimoRestante = 0


class VariablesParsear(object):
    def __init__(self):
        self.identificadorLinea  = None
        self.celdas = None
        self.celdasHorizontales = None
        self.vertical = None

    def setVariables(self, pIdentificadorLinea, pCeldas, pCeldasHorizontales, pVertical):
        self.identificadorLinea = pIdentificadorLinea
        self.celdas = pCeldas
        self.celdasHorizontales = pCeldasHorizontales
        self.vertical = pVertical

class VariablesAniadirCelda(object):
    def __init__(self):
        self.indiceLlave = None
        self.longitudCasillasBlancas = None
        self.casillaLlave = None
        self.diccionarioCelda = None
        self.vertical = None

    def setVariables(self, pIndiceLlave, pLongitudCasillasBlancas, pCasillaLlave, pDiccionarioCelda, pVertical):
        self.indiceLlave = pIndiceLlave
        self.longitudCasillasBlancas = pLongitudCasillasBlancas
        self.casillaLlave = pCasillaLlave
        self.diccionarioCelda = pDiccionarioCelda
        self.vertical = pVertical

class Solucionador(object):

    celdasHorizontales = {}   # Coordenadas de las celdas horizontales
    celdasVerticales = {}     # Coordenadas de las celdas verticales
    celdasUnicas_H = []       # Lista de celdas horizontales únicas, contiene los objetos Celda
    celdasUnicas_V = []       # Lista de celdas verticales únicas, contiene los objetos Celda
    solucion = {}             # La solución actual
    matrizSolucion = []       # Matriz de la solución actual
    soluciones = {}           # Solución md5-hashes para soluciones
    solucionesParciales = {}  # Solución parcial md5-hashes para soluciones

    ancho = 0                 # Ancho del kakuro
    alto = 0                  # Alto del kakuro


    conHilos = False
    conForks = False
    variablesParsear = VariablesParsear()
    variablesAniadirCelda = VariablesAniadirCelda()

    def __init__(self, archivoTxt):
        vertical = False
        filasVerticales = []

        with open(archivoTxt, 'r') as archivoKakuro:     # Abrir el txt, 'r' -> leer

            for identificadorLinea, filaArchivo in enumerate(archivoKakuro):

                if len(filaArchivo.strip()) == 0: # .strip() para validar en caso de existir espacios entre digitos
                    vertical = True # Indicador de que ya se analizó la matriz horizontal

                else:
                    # celda contendrá vectores de cada fila del archivo
                    celdas = filaArchivo.strip().split(',') # Separa el texto donde encuentra comas

                    self.ancho = len(celdas)     # Obtener el ancho

                    if vertical:

                        if len(filasVerticales) == 0:
                            filasVerticales = [[] for _ in celdas] # Crear una matriz del tamaño de celdas

                        for indice, celda in enumerate(celdas):
                            filasVerticales[indice].append(celda)

                    else:
                        # TODO: ====================== Hilo y Fork ======================
                        self.variablesParsear.setVariables(identificadorLinea, celdas, self.celdasHorizontales, vertical)

                        self.PasearSecuencia()
                        #EjecutarForkHilo(self.PasearSecuencia) # Todo: Posible hilo
                        #EjecutarFuncionEnHilo(self.PasearSecuencia) # Si SoluciondorK.conHilos == True, ejecute con hilos, si no en el main thread
                        #EjecutarFuncionConForks(self.PasearSecuencia)

        self.alto = len(filasVerticales[0])   # Obtener el alto, columnas

        for indice, filaVertical in enumerate(filasVerticales): # A este punto ya se tiene la matriz vertical, entonces mandela a parsear

            # TODO: ====================== Hilo y Fork ======================
            self.variablesParsear.setVariables(indice, filaVertical, self.celdasVerticales, vertical)

            self.PasearSecuencia()
            #EjecutarForkHilo(self.PasearSecuencia) # Todo: No sirve
            #EjecutarFuncionEnHilo(self.PasearSecuencia)
            #EjecutarFuncionConForks(self.PasearSecuencia)

            # Al final, celdasH y celdasV tienen objetos celdas


    def PasearSecuencia(self): # Analiza cada fila de la matriz
        # indice: cantidad de filas
        # celdas contiene la fila
        # diccionarioCelda: primera llamada -> self.celdasHorizontales vacia
        # vertical
        #print("*** Estoy en PasearSecuencia ***")
        #print('Hilo actual: ', threading.current_thread().name)

        """ Explicación general:
        Parsea el TXT y separa las filas en vectores poniendoles un indice.
        Luego en añadirCelda a cada elemento de esa fila se le etiqueta con un identificador.
        Se guardan las coordenadas [Columna, Fila] de ese elemento
        En el init Celda lo que se hace es recorrer las casillas BLANCAS que abarca cada
        casilla LLAVE y se crea el objeto Celda de las casillas LLAVE, dentro de la información de este
        objeto se almacena las coordenadas de las casillas blancas correspondiendes.
        Se llama a ObtenerSumasUnicas el cual saca en forma de vector las POSIBLES soluciones
        a la casilla LLAVE.
        """

        # TODO: Requisito para el HILO
        indice = self.variablesParsear.identificadorLinea
        fila = self.variablesParsear.celdas
        diccionarioCelda = self.variablesParsear.celdasHorizontales
        vertical = self.variablesParsear.vertical
        # TODO: ===================================================

        casillaLlave = 0
        comienzo = [] # [Indice fila, indice columna + 1]
        longitudCasillasBlancas = 0 # Longitud de casillas blancas de la llave

        for identificador, celda in enumerate(fila): # Añade un indice empezando desde 0 a cada elemento de la lista

            # celda contendra cada elemento de las matrices

            if celda.isdigit(): # Devuelve true si todos los caracteres de la celda son dígitos y hay al menos un carácter, false en caso contrario
                if int(celda) > 0: # Identificar las llaves

                    if casillaLlave != 0:
                        # TODO: ====================== Hilo y Fork ======================
                        self.variablesAniadirCelda.setVariables(comienzo, longitudCasillasBlancas, casillaLlave, diccionarioCelda, vertical)

                        self.aniadirCelda()
                        #EjecutarForkHilo(self.aniadirCelda) # Todo: No sirve
                        #EjecutarFuncionEnHilo(self.aniadirCelda)
                        #EjecutarFuncionConForks(self.aniadirCelda)
                        #self.aniadirCelda(comienzo, longitudCasillasBlancas, casillaLlave, diccionarioCelda, vertical)

                    casillaLlave = int(celda) # Contiene contiene la llave
                    longitudCasillasBlancas = 0 # Longitud 0 porque estamos en otra casilla

                    # comienzo = [Indice fila,  indice columna + 1]
                    comienzo = [indice, identificador + 1] if vertical else [identificador + 1, indice]

                elif int(celda) == 0: # Encontró una casillas blanca 00
                    longitudCasillasBlancas += 1

        if casillaLlave != 0:
            # TODO: ====================== Hilo y Fork ======================
            self.variablesAniadirCelda.setVariables(comienzo, longitudCasillasBlancas, casillaLlave, diccionarioCelda, vertical)

            if Solucionador.conHilos == True:
                for x in range(10):
                    thread = threading.Thread(target=self.CalcularPosiblesSumas, args=(casillaLlave, longitudCasillasBlancas))
                    #thread.daemon = True
                    thread.start()
                    thread.join()



            self.aniadirCelda()
            #EjecutarForkHilo(self.aniadirCelda) # Todo: No sirve
            #EjecutarFuncionEnHilo(self.aniadirCelda)
            #EjecutarFuncionConForks(self.aniadirCelda)
            #self.aniadirCelda(comienzo, longitudCasillasBlancas, casillaLlave, diccionarioCelda, vertical)

    def CalcularPosiblesSumas(self, casillaLlave, cantCasillasBlancas):
        ObtenerSumas(casillaLlave, cantCasillasBlancas)

    def aniadirCelda(self):#, indiceLlave, longitudCasillasBlancas, casillaLlave, diccionarioCelda, vertical):
        # indiceLlave: indice donde esta la llave
        # longitudCasillasBlancas: cantidad de casillas blancas
        # casillaLlave: numero casilla llave
        # diccionarioCelda: matriz horizontal o vertical
        # vertical: si vamos por la matriz vertical
        #print("*** Estoy en AniadirCelda ***")
        #print('Hilo actual: ', threading.current_thread().name)

        # TODO: Requisito para el HILO
        indiceLlave = self.variablesAniadirCelda.indiceLlave
        longitudCasillasBlancas = self.variablesAniadirCelda.longitudCasillasBlancas
        casillaLlave = self.variablesAniadirCelda.casillaLlave
        diccionarioCelda = self.variablesAniadirCelda.diccionarioCelda
        vertical = self.variablesAniadirCelda.vertical
        # TODO: ===================================================

        if longitudCasillasBlancas == 0: # Si hay una llave y la longitud de casillas blancas disponibles es 0, hay un error en el kakuro
            messagebox.showinfo("Error", "Error en el kakuro en: %s. Es inválido" % (indiceLlave))
            raise Exception('Error en el kakuro en: %s' % (indiceLlave))

        # Clase Celda corresponde solo a las casillas llave. Cuando se crea el objeto celda, tiene una variable que le indica su rango de casillas blancas
        celda = Celda(casillaLlave, longitudCasillasBlancas, indiceLlave, vertical, self) # self -> enviar como parametro la clase

        indice = 1 if vertical else 0


        if vertical:
            self.celdasUnicas_V.append(celda) # Ir almacenando los objetos de tipo celda en las matrices
        else:
            self.celdasUnicas_H.append(celda)

        """# Generar el mapeo de la coordenada
        for _ in range(longitudCasillasBlancas):
            diccionarioCelda[tuple(indiceLlave)] = celda # Agregar a diccionarioCelda en el indice: indiceLlave, el elemento celda creado
            indiceLlave[indice] += 1 # Dic Celda = celdasHorizontales ó celdasVerticales"""

        if Solucionador.conHilos == True:
            for x in range(10):
                thread = threading.Thread(target=self.MapeoInstanciaCelda, args=(celda, longitudCasillasBlancas, indiceLlave, diccionarioCelda, indice))
             #   thread.daemon = True
                thread.start()
                thread.join()

        else:
            self.MapeoInstanciaCelda(celda, longitudCasillasBlancas, indiceLlave, diccionarioCelda, indice)

    def MapeoInstanciaCelda(self, celda, longitudCasillasBlancas, indiceLlave, diccionarioCelda, indice):
        # Generar el mapeo de la coordenada
        for _ in range(longitudCasillasBlancas):
            diccionarioCelda[tuple(indiceLlave)] = celda  # Agregar a diccionarioCelda en el indice: indiceLlave, el elemento celda creado
            indiceLlave[indice] += 1  # Dic Celda = celdasHorizontales ó celdasVerticales

    def AniadirSolucion(self, restante = 0):
        """
        Añade una solución a las soluciones. Si los números
        faltan añadirlos a las soluciones parciales.
        Devolver True si se agregó una nueva solución.
        """
        nuevaSolucion = False
        m = hashlib.md5()
        m.update(str(self.solucion.values()).encode('utf-8'))

        if m.hexdigest() not in self.soluciones:
            if restante > 0:
                self.solucionesParciales[m.hexdigest()] = restante

            self.soluciones[m.hexdigest()] = self.solucion.copy()
            nuevaSolucion = True

        return nuevaSolucion

    def Resolver(self, todoProbado, iteraciones, campoActual, limite): #kakuro.Resolver(True, 0, 1, 2) # todoProbado, iteraciones, campoActual, limite

        campoAnterior = 0
        # A huevo el maximo de iteraciones va a ser 45, con limite de 9 casillas blancas
        if len(self.solucion) < len(self.celdasHorizontales) and iteraciones < 45:

            campoAnterior = campoActual
            campoActual = 0

            # Iterar en ambos vectores de una vez
            for celda in self.celdasUnicas_H + self.celdasUnicas_V:

                campoActual += celda.LlenarCeldas()

            if campoAnterior == 0:

                for celda in self.celdasUnicas_H + self.celdasUnicas_V:
                    todoProbado &= celda.ProbarPosibilidades(limite) # digitos en todoProbado y en ProbarPosibilidades evaluado en el limite

                if todoProbado:
                    if Celda.minimoRestante > 0:

                        for solucionParcial in self.soluciones:
                            if len(solucionParcial) == Celda.minimoRestante:
                                self.solucion = solucionParcial

                    else:
                        print
                        # No haga la llamada recursiva

        if (iteraciones < 45):
            if campoAnterior == 0:
                self.Resolver(todoProbado, iteraciones + 1, campoActual, limite * 2)

            else:
                self.Resolver(todoProbado, iteraciones + 1, campoActual, limite)

        #logging.debug("Limite: %s" % limite)
        #logging.debug("Iteraciones: %s" % iteraciones)

    def VerificarSolucion(self):
        if (len(self.solucion) != len(self.celdasHorizontales)) & (len(self.solucion) + 1 != len(self.celdasHorizontales)):
            #print(len(self.solucion))
            #print(len(self.celdasHorizontales))
            #print("Sin solución.")
            print
        else:
            Celda.minimoRestante = 0
            self.AniadirSolucion()

        #self.MostrarSoluciones()
        self.FormarMatrizSolucion()

    """def MostrarSoluciones(self):
        indice = 1

        for llave in self.soluciones:
            if llave in self.solucionesParciales and Celda.minimoRestante != self.solucionesParciales[llave]:
                continue

            print("Solución %s:" % indice)

            for y in range(self.alto):
                for x in range(self.ancho):
                    if (x, y) in self.soluciones[llave]:
                        print("%i " % self.soluciones[llave][(x, y)])

                    elif (x, y) not in self.soluciones[llave] and (x, y) in self.celdasHorizontales:
                        print("X ")

                    else:
                        print("# ")

            indice += 1"""

    def FormarMatrizSolucion(self):

        for llave in self.soluciones:
            if llave in self.solucionesParciales and Celda.minimoRestante != self.solucionesParciales[llave]:
                continue

            for y in range(self.alto):
                Solucionador.matrizSolucion.append([])

                for x in range(self.ancho):
                    if (x, y) in self.soluciones[llave]:
                        Solucionador.matrizSolucion[y].append(self.soluciones[llave][(x, y)])

                    elif (x, y) not in self.soluciones[llave] and (x, y) in self.celdasHorizontales:
                        Solucionador.matrizSolucion[y].append("X")

                    else:
                        Solucionador.matrizSolucion[y].append("X")

            break # Obtener la primer solucion

        #Solucionador.matrizSolucion = self.matrizSolucion


class VariablesBacktracking(object):
    def __init__(self):
        self.validos = None
        self.conjuntoValores = None
        self.indiceConjuntoValores = None

    def setVariables(self, pValidos, pConjuntoValores, pIndiceConjuntoValores):
        self.validos = pValidos
        self.conjuntoValores = pConjuntoValores
        self.indiceConjuntoValores = pIndiceConjuntoValores

class VariablesAniadirDigitoEncontrado(object):
    def __init__(self):
        self.coordenada = None
        self.digitoEncontrado = None
        self.probando = None

    def setVariables(self, pCoordenada, pDigitoEncontrado, pProbando = False):
        self.coordenada = pCoordenada
        self.digitoEncontrado = pDigitoEncontrado
        self.probando = pProbando

class VariablesRehacer(object):
    def __init__(self):
        coordenadaPrueba = None

    def setVariables(self, pCoordenadaPrueba):
        self.coordenadaPrueba = pCoordenadaPrueba

class Celda(object):

    coordenadasModificadas = []
    suponerCoordsHorizontales = {}
    suponerCoordsVerticales = {}
    minimoRestante = 0

    variablesBacktracking = VariablesBacktracking()
    variablesAniadirDigitoEncontrado = VariablesAniadirDigitoEncontrado()
    variablesRehacer = VariablesRehacer()

    def __init__(self, casillaLlave, longitudCasillasBlancas, indiceLlave, vertical, solucionador):
        self.solucionador = solucionador # Instancia de la clase Solucionador, se utilizan los indices -> (columna, fila): solucion
        self.longitudCasillasBlancas = longitudCasillasBlancas
        self.casillaLlave = casillaLlave # Contiene las casillas clave del kakuro

        # Contendrá celdasHorizontales o verticales
        # (2, 1): Llave: 3, Casillas blancas: 2, Secuencias: [(1, 2)] (Objetos de tipo Celda)
        self.intersecar = solucionador.celdasHorizontales if vertical else solucionador.celdasVerticales

        # Total de casillas blancas del tablero, da igual si son celda horizontales o verticales
        self.__class__.minimoRestante = len(solucionador.celdasHorizontales) # __class__ Es una referencia al tipo de la instancia actual

        # Obtener todas combinaciones de numeros segun las casillas blancas formando la casilla llave
        self.secuencias = ObtenerSumasUnicas(casillaLlave, longitudCasillasBlancas)

        if len(self.secuencias) == 0:

            messagebox.showinfo("Error", "El kakuro no tiene solución. \n\n Llave: " + str(self.casillaLlave) + " - Casillas blancas: "+str(self.longitudCasillasBlancas) + " - Indice Llave" + str(indiceLlave))
            raise Exception("Error en %s, no se encontraron secuencias de dígitos." % (indiceLlave,))

        # Crear un vector de 1 hasta 9 (identificador) tiendo como refencia un set()
        # {1: set(), 2: set(), 3: set(), 4: set(), 5: set(), 6: set(), 7: set(), 8: set(), 9: set()}
        self.digitoCoordenadas = {x: set() for x in range(1, 10)}

        # Si es vertical multiplique por a = 0 y b = 1. Si es horizontal por a = 1 y b = 0
        # Indice "comienzo": El primer valor representa la columna, el segundo la fila.
        (a, b) = (0, 1) if vertical else (1, 0)

        self.coordenadas = [(indiceLlave[0] + a * x, indiceLlave[1] + b * x) for x in range(longitudCasillasBlancas)]
        # Coordenadas guarda los pares ordenados [Columna, Fila] de todas las celdas blancas que corresponden a una casilla llave.

    def __repr__(self): # Cuando se hace el print del objeto, retorna lo siguiente:
        return "Llave: %d, Casillas blancas: %d, Secuencias: %s" % (self.casillaLlave, self.longitudCasillasBlancas, self.secuencias)

    def ObtenerDigitos(self):
        """
        Devuelve todos los dígitos posibles (excluyendo los dígitos ya encontrados) como una tupla de:

        todosLosDigitos - El conjunto que contiene la unión de todos los dígitos posibles.
        digitosRequeridos - Conjunto de dígitos comunes a todas las secuencias
        """
        digitosEncontrados = set(self.ObtenerDigitosEncontrados()) # Devuelve los dígitos ya encontrados de la solucion de la celda
        todosLosDigitos = set()

        # Combinaciones de los posibles numeros segun las casillas blancas formando la casilla llave
        digitosRequeridos = set(self.secuencias[0]) # Analizar primero, el primer vector de ese conjunto de numeros

        # self.secuencias = Todas las combinaciones de los posibles numeros segun las casillas blancas formando la casilla llave
        for secuencia in self.secuencias:

            # .issubset: True -> si el conjunto está contenido en el conjunto especificado, False lo contrario
            if digitosEncontrados.issubset(set(secuencia)) or len(digitosEncontrados) == 0:

                todosLosDigitos = todosLosDigitos | set(secuencia) # digitos en "todosLosDigitos" o "set(secuencia)" o ambos
                digitosRequeridos = digitosRequeridos & set(secuencia) # digitos en "digitosRequeridos" y "set(secuencia)"


        todosLosDigitos -= digitosEncontrados
        digitosRequeridos -= digitosEncontrados

        return todosLosDigitos, digitosRequeridos

    def ObtenerDigitosEncontrados(self):
        """
        Devuelve los dígitos ya encontrados de la solucion de la celda.
        Recorre las coordenadas que pertenecen a CADA casilla BLANCA, y revisa si están en el solucionador o no.
        Esto para saber si ya se les encontro valor o aun esta en proceso
        """
        digitosEncontrados = []

        for coordenada in self.coordenadas:
            #print(self.coordenadas)

            if coordenada in self.solucionador.solucion:
                digitosEncontrados.append(self.solucionador.solucion[coordenada])

        return digitosEncontrados

    def AniadirDigitoEncontrado(self):#, coordenada, digitoEncontrado, probando = False):
        #print("*** Estoy en AniadirDigitoEncontrado ***")
        #print('Hilo actual: ', threading.current_thread().name)

        # TODO: Requisito para el HILO
        coordenada = self.variablesAniadirDigitoEncontrado.coordenada
        digitoEncontrado = self.variablesAniadirDigitoEncontrado.digitoEncontrado
        probando = self.variablesAniadirDigitoEncontrado.probando
        # TODO: ==========================================

        # coordenada: Coordenada que no ha sido analizada en la solucion
        # digitoEncontrado: Posible valor que conforma la solucion de la llave. Se prueba cada digito del vector de posibles sumas
        self.solucionador.solucion[coordenada] = digitoEncontrado
        # Añadalo directamente como una solucion

        # TODO: PODA
        if not probando: # LlenarCeldas() es el unico que tiene la posiblidad de probar
            if coordenada in self.suponerCoordsHorizontales:
                # Si no se está probando, y la coord esta en las suposiciones, elimínela
                del self.suponerCoordsHorizontales[coordenada]

            if coordenada in self.suponerCoordsVerticales:
                del self.suponerCoordsVerticales[coordenada]

        # Si se llama directamente desde la función "Backtraking", el condicional de arriba no sucede y pasa directamente
        # a añadir la coordenada que no ha sido analizada en la solucion
        self.coordenadasModificadas.append(coordenada) # Nueva coordenada que no está en self.solucionador.solucion (Backtracking)

    def ProbarPosibilidades(self, limite): #TODO: *** PODA ***

        # todosLosDigitos, digitosRequeridos
        todosLosDigitos, digitosRequeridos = self.ObtenerDigitos()

        combos = []

        # Si la combinacion de ambos es equivalente, obtener las combinaciones de ambos vectores
        if len(todosLosDigitos) == len(digitosRequeridos) and len(todosLosDigitos) > 0:
            # Obtener todas las combinaciones posibles de números dado un vector
            combos = ObtenerCombinaciones(list(digitosRequeridos))

        else:
            restante = self.casillaLlave # Se necesita disminuir el valor de la llave
            longitudCasillasBlancas = self.longitudCasillasBlancas

            for coordenada in self.coordenadas:
                # Si la coordenada esta en la solucion de la casilla
                # a "restante" (casillaLlave) quitele ese valor ya encontrado para
                # seguir con las demas posibilidades de numeros

                if coordenada in self.solucionador.solucion: # TODO:  *** PODA ***
                    restante -= self.solucionador.solucion[coordenada] # Valor
                    longitudCasillasBlancas -= 1

            # Si estamos en el minimo de casillas blancas, calcule mediante "ObtenerSumas()"
            # el vector que conforma el valor de la permutacion restante con 2 y añádalo a "combos"
            if longitudCasillasBlancas == 2: # TODO:  *** PODA ***

                #subSecuencia = ObtenerSumasUnicas(restante, longitudCasillasBlancas)
                combos.extend(ObtenerSumas(restante, longitudCasillasBlancas))


        if len(combos) <= limite and len(combos) != 0:

            # TODO: ====================== Hilo y Fork ======================
            self.variablesBacktracking.setVariables([], combos, 0)

            self.Backtracking()
            #EjecutarForkHilo(self.Backtracking) # Todo: Posible hilo
            #EjecutarFuncionEnHilo(self.Backtracking)
            #EjecutarFuncionConForks(self.Backtracking)
            #self.Backtracking()#[], combos, 0)

        return (len(combos) <= limite) # True si es menor o igual, False lo opuesto

    def LlenarCeldaUnica(self, digitosRequeridos):
        recuento = 0

        # Crear un vector de 1 hasta 9 (identificador) tiendo como refencia un set()
        for digito, coordenadas in self.digitoCoordenadas.items(): # .items() forman un par ordenado con cada identificar y set()

            if len(coordenadas) == 1 and digito in digitosRequeridos:
                coordenada = coordenadas.pop() # Obtener el ultima elemento

                if coordenada not in self.solucionador.solucion:
                    recuento += 1

                    #logging.debug("Añadiendo: %s %s" % (coordenada, digito))

                    # TODO: ====================== Hilo y Fork ======================
                    self.variablesAniadirDigitoEncontrado.setVariables(coordenada, digito)

                    self.AniadirDigitoEncontrado()
                    #EjecutarForkHilo(self.AniadirDigitoEncontrado) #Todo: Dura ms mas
                    #EjecutarFuncionEnHilo(self.AniadirDigitoEncontrado)
                    #EjecutarFuncionConForks(self.AniadirDigitoEncontrado)

                    #self.AniadirDigitoEncontrado(coordenada, digito)

        return recuento

    """
        Esta funcion la llama con un celda.LlenarCeldas por lo tanto esta funcion agarra la informacion de esa celda(donde la clase celda almacena LLAVES y sus
        blancos ligados) y le saca los numeros encontrados de sus casillas blancas.
        En digitos1, digitos2 = self.ObtenerDigitos(), saca las combinaciones posibles para esa LLAVE
        En  digitos3, digitos4 = self.intersecar[coordenada].ObtenerDigitos() saca las combinaciones posibles de la posicion contraria. Es decir, si
        la celda LLAVE es HORIZONTAL, cuando el For recorre las coordenadas de las blancas y llama a intersecar, este devolveria la información de esa
        misma celda pero en su formato VERTICAL, esta info es la llave VERTICAL, num de casillas blancas, secuencia...
        esto mismo se aplicaría si la celda es VERTICAL, el intersecar devolvería HORIZONTAL.
        Por ultimo se compara el digitos1 y digitos3 y si solo tienen un elemento y es el mismo numero, este se convierte en solución para esa casilla
        ya que calza para VERTICAL y HORIZONTAL
        Cuando sale del For llama a cuentaLlena += self.LlenarCeldaUnica(digitos2) y retorna cuentaLlena
        Rellene los números en la ejecución y devuelva el número
        de los dígitos encontrados.
    """
    def LlenarCeldas(self, probar=False):

        # Crear un vector del 1 a 9, siendo estos la posicion conteniendo set()
        # {1: set(), 2: set(), 3: set(), 4: set(), 5: set(), 6: set(), 7: set(), 8: set(), 9: set()}
        self.digitoCoordenadas = {x: set() for x in range(1, 10)}

        # Dígitos ya encontrados de la solucion de la celda
        digitosEncontrados = self.ObtenerDigitosEncontrados()
     #   print("Digi Encontrados:", digitosEncontrados)
        # Comparar la longitud sin los numeros repetidos
        if len(digitosEncontrados) != len(set(digitosEncontrados)):
            return -1

        # digito1 -> Conjunto que contiene la unión de todos los dígitos posibles.
        # digito1 -> Conjunto de dígitos comunes a todas las secuencias
        digitos1, digitos2 = self.ObtenerDigitos()
        cuentaLlena = 0

        for coordenada in self.coordenadas:

            # self.solucionador.solucion -> (columna, fila):digitoSolución
            # Si a la coordenada aun no se le ha asignado una solución, entonces
            # devuelvame todos los dígitos posibles de esa coordenada
            if coordenada not in self.solucionador.solucion:
                # self.intersecar:
                #       Contendrá celdasHorizontales o verticales
                #       (2, 1): Llave: 3, Casillas blancas: 2, Secuencias: [(1, 2)], ...,

                digitos3, digitos4 = self.intersecar[coordenada].ObtenerDigitos() # Devuelve todos los dígitos posibles de esa coordenada
                digitoComun = digitos3 & digitos1 # Obtener los digitos de ambos conjuntos

                if len(digitoComun) == 1:
                    #TODO Poda
                    digitosEncontrados = digitoComun.pop()

                    #logging.debug("Encontró: %s %s" % (coordenada, digitosEncontrados))

                    # TODO: ====================== Hilo y Fork ======================
                    self.variablesAniadirDigitoEncontrado.setVariables(coordenada, digitosEncontrados, probar)

                    #EjecutarFuncionEnHilo(self.AniadirDigitoEncontrado)
                    #EjecutarForkHilo(self.AniadirDigitoEncontrado) # Todo: Dura mas
                    #EjecutarFuncionConForks(self.AniadirDigitoEncontrado)
                    self.AniadirDigitoEncontrado()

                    #self.AniadirDigitoEncontrado(coordenada, digitosEncontrados, probar)

                    if digitosEncontrados in digitos2:
                        digitos2.remove(digitosEncontrados)

                    cuentaLlena += 1

                elif len(digitoComun) == 0:
                    return -1

                for digito in digitoComun:
                    self.digitoCoordenadas[digito].add(coordenada)

                if probar and cuentaLlena != 0 and self.intersecar[coordenada].LlenarCeldas(probar) == -1:
                    return -1

        cuentaLlena += self.LlenarCeldaUnica(digitos2)

        return cuentaLlena

    def Rehacer(self):#, coordenadaPrueba):
        """
        Deshacer un cambio en la solución si un
        dígito colocado evita que se encuentre una solución.
        Se envia la coordenada que se estaba probando y se elimina
        de la solución
        """
        #print("*** Estoy en Rehacer ***")
        #print('Hilo actual: ', threading.current_thread().name)

        coordenadaPrueba = self.variablesRehacer.coordenadaPrueba

        coordenada = None

        while coordenada != coordenadaPrueba:
            coordenada = self.coordenadasModificadas.pop()  # Obtener el ultima elemento de las coordenadasMod
            # valor = self.solucionador.solucion[coordenada]
            # print(valor)

            del self.solucionador.solucion[coordenada] # Quite esa coordenada

    def Backtracking(self):#, validos, conjuntoValores, indiceConjuntoValores): # Probar valores

        #print("*** Estoy en Backtracking ***")
        #print('Hilo actual: ', threading.current_thread().name)

        # Combinaciones posibles de números dado un vector (combos)
        validos = self.variablesBacktracking.validos

        # Vector con las posibles sumas que conforman el numero llave
        conjuntoValores = self.variablesBacktracking.conjuntoValores
        # Indice que permite ir iterando en cada vector de las posibles sumas
        indiceConjuntoValores = self.variablesBacktracking.indiceConjuntoValores

        # Ir obteniedo cada vector de las posibles sumas
        valores = conjuntoValores[indiceConjuntoValores] # combos

        indiceDigito = 0
        eliminado = False
        coordenadasPrueba = []

        # self.coordenadas = Tiene la posición de las casillas blancas asociadas a cada casilla llave, la primera casilla blanca nada más

        for coordCelda in self.coordenadas:

            # Cada casilla tiene su solucion (clase Solucionador)
            if coordCelda not in self.solucionador.solucion: # self.solucionador -> la instania de la clase Solucionador
                # Ir almacenado y probando nuevas coordenadas -> AniadirDigitoEncontrado
                coordenadasPrueba.append(coordCelda)

                # TODO: Requisito para el HILO
                                    # valores[indiceDigito] -> vector del conjunto de las posibles sumas
                self.variablesAniadirDigitoEncontrado.setVariables(coordCelda, valores[indiceDigito])
                # TODO: ===========================================

                self.AniadirDigitoEncontrado()
                #EjecutarForkHilo(self.AniadirDigitoEncontrado) # TODO: Dura mas
                #EjecutarFuncionEnHilo(self.AniadirDigitoEncontrado)
                #EjecutarFuncionConForks(self.AniadirDigitoEncontrado)

                #self.AniadirDigitoEncontrado(coordCelda, valores[indiceDigito])

                indiceDigito += 1 # Obtener cada digito de cada vector de las posibles sumas

        for coordenadaPrueba in coordenadasPrueba: # Coordenadas que no estan en self.solucionador.solucion y que han sido añadidas como prueba

            # self.intersecar contiene celdasHorizontales o verticales
            # (2, 1): Llave: 3, Casillas blancas: 2, Secuencias: [(1, 2)] (Objetos de tipo Celda)
            if self.intersecar[coordenadaPrueba].LlenarCeldas(True) == -1: # Si no se encontro ningun digito en común
                eliminado = True
                break

        if not eliminado:
            validos.append(valores)

        if len(self.intersecar) == len(self.solucionador.solucion):
            self.solucionador.AniadirSolucion()
            # minimoRestante: total de casillas blancas del tablero
            self.__class__.minimoRestante = 0 # __class__ referencia al tipo de la instancia actual


        else:
            if (len(self.intersecar) - len(self.solucionador.solucion)) <= self.minimoRestante:
                self.__class__.minimoRestante = (len(self.intersecar) - len(self.solucionador.solucion))
                self.solucionador.AniadirSolucion(self.minimoRestante)


        self.variablesRehacer.setVariables(coordenadasPrueba[0])

        self.Rehacer()
        #EjecutarFuncionEnHilo(self.Rehacer)
        #EjecutarForkHilo(self.Rehacer) # Todo: No sirve
        #EjecutarFuncionConForks(self.Rehacer)

        #self.Rehacer(coordenadasPrueba[0])

        if (indiceConjuntoValores < len(conjuntoValores) - 1):

            # TODO: Requisito para el HILO
            self.variablesBacktracking.setVariables(validos, conjuntoValores, indiceConjuntoValores + 1)
            # TODO: =============================

            self.Backtracking()

            #EjecutarForkHilo(self.Backtracking) # Todo: No sirve
            #EjecutarFuncionEnHilo(self.Backtracking)  # vertical = False
            #EjecutarFuncionConForks(self.Backtracking)

            #self.Backtracking()#validos, conjuntoValores, indiceConjuntoValores + 1)

        else:
            if len(validos) == 1:
                #logging.debug("Añadiendo: %s %s" % (self.coordenadas[0], validos[0]))

                indiceDigito = 0

                for coordCelda in self.coordenadas:

                    if coordCelda not in self.solucionador.solucion:

                        # TODO: Requisito para el HILO
                        self.variablesAniadirDigitoEncontrado.setVariables(coordCelda, validos[0][indiceDigito])
                        # TODO: ===========================================

                        self.AniadirDigitoEncontrado()
                        #EjecutarForkHilo(self.AniadirDigitoEncontrado) # Todo: No sirve
                        #EjecutarFuncionEnHilo(self.AniadirDigitoEncontrado)
                        #EjecutarFuncionConForks(self.AniadirDigitoEncontrado)

                        #self.AniadirDigitoEncontrado(coordCelda, validos[0][indiceDigito])
                        indiceDigito += 1




def Ejecutar(direccion):
    #if len(sys.argv) == 3 and sys.argv[2] == '--debug':
        # Enable debug output
        #logging.basicConfig(level=logging.DEBUG, format="Debug: %(message)s", stream=sys.stdout)

    kakuro = Solucionador(direccion)
    try:
        start = time.time()
        kakuro.Resolver(True, 0, 1, 2) # todoProbado, iteraciones, campoActual, limite
        print('El trabajo tomó: ', time.time() - start, ' segundos')
        kakuro.VerificarSolucion()

    except:
        kakuro.soluciones[0] = kakuro.solucion
#        kakuro.MostrarSoluciones()
        raise

    ReestablecerAtributosClases()

