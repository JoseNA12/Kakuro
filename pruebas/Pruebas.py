
import hashlib
import threading
from Hilo import Hilo
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import time

def jeje_0(contador):
    return (contador, True) if contador != 0 else (contador, False)

def jeje_1():
    contador = 0
    i = 0
    while i < 10:
        contador += i
        i += 1

    print(contador)

def jeje_2(numero_1, numero_2):
    if (numero_1 in (1, 2, 3)) & (numero_2 in (7, 8, 9)):
        return True
    else:
        return False

def jeje_3():
    matriz = [[] for _ in range(10)]
    i = 0
    j = 0
    x = 0
    y = 0

    while i < 10:
        j = 0
        y = 0
        while j < 10:

            matriz[x].append(12)
            j += 2
            y += 1

        x += 1
        i += 2

    print(matriz)

def jeje_4():
    a = set('abracadabra')  # Letras unicas en a
    b = set('alacazam') # Letras unicas en b
    c = set()   # set() sin ningun contenido

    d = a - b   # letras en a pero no en b
    e = a | b   # letras en a o b o ambas
    f = a & b   # letras en a y b
    g = a ^ b   # letras en a o b pero no ambas

    h = {x for x in 'abracadabra' if x not in 'abc'}

    print("a: " + str(a))
    print("b: " + str(b))
    print("c: " + str(c))

    print("d: " + str(d))
    print("e: " + str(e))
    print("f: " + str(f))
    print("g: " + str(g))
    print("h: " + str(h))

def jeje_5():
    for indice, palabra in enumerate(['Viva', 'el', 'metal']):

        print(indice, palabra)

def jeje_6():
    lista = ['Kakuro', 'kakuculo', 'Kakita', 'kakauate', 'kankun', 'kingkong']

    for palabra in sorted(set(lista)):

        print(palabra)

def jeje_7():
    matriz = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],]

    nuevaMatriz = [[fila[i] for fila in matriz] for i in range(4)]

    print(nuevaMatriz)

def jeje_8():
    casilla = 19
    a = [[casilla - x, x] for x in range(1, casilla - 1)]

    print(a)

def jeje_9():

    x = 12
    y = 21

    def funcion_1(num):
        print("Función 1: " + str(num + x + y))

    def funcion_2(num):
        print("Función 2: " + str(num + 5))

    funcion_1(12)

def jeje_10():
    solucion = {"(1, 2)": 1 , "(3, 4)": 2, "(5, 6)": 3, "(7, 8)": 4, "(10, 11)": 5}

    m = hashlib.md5()
    m.update(str(solucion.values()).encode('utf-8'))

    # .decode('utf-8')
    # .encode('utf-8') -> Los objetos Unicode deben codificarse antes del hash

    #m.update("1D1A1E1413".encode('utf-8'))

    print(m.hexdigest())
    print(m.digest_size)
    print(m.block_size)

def jeje_11():
    class Kakuro:
        def __init__(self, a, b):
            self.A = a
            self.B = b

        def __repr__(self):
            return "Kakuro(): A: %s, B: %d" % (self.A, self.B, )

    def __str__(self):
        return "Miembro de Kakuro :)"

    k = Kakuro(12, 97)

    print(k)

    print(repr(k))


class Pruebas:

    miHilo = None
    holi = "Vacio"

    def __init__(self):
        self.miHilo = Hilo(self.jeje_12_sub_1)
        self.holi = "JOjojojo"

    def __getattribute__(self, name):
        if name == 'holi':
            return 0
        else:
            return object.__getattribute__(self, name)

    def jeje_12_sub_1(self,tarea):

        with self.miHilo.tarea_completada:
            a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
            b = []

            for i in range(len(a)):
                for j in range(len(a)):

                    b.append(4)

            print("\n" + str(i) + " itearaciones" + "\n")
            print('Hilo: ', threading.current_thread().name, ' Tarea numero: ',tarea)

        print("b",b)

    def jeje_12(self):

        cantHilos = 50
        catTareas = 10

        for counter in range(cantHilos):
            thread = threading.Thread(target = self.miHilo.threader) # Crear el hilo, target es la funcion que quiero ejecutar
            thread.start()  # Iniciar el hilo

        # La primer tarea es la última en ejecutarse, y la última tarea la primera en ejecutarse
        for tarea in range(catTareas):
            self.miHilo.cola.put(tarea)  # Meter a la cola la tarea

            self.miHilo.cola.join()  # Ejecutar el hilo
      #  jeje_12_sub_1()



def jeje_13():
    a = [1, 2, 3, 4]
    b = [6, 7, 8, 9]

    c = a + b

    if 5 not in c:
        print("No esta el 5")

def jeje_14():
    a = []
    b = (12, 4)
    c = (21, 7)

    a.append((21, 7))

    if b not in a:
        print("(12, 4) no esta en a")

    if c not in a:
        print("(21, 7) no esta en a")

def jeje_15(numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9]): # Obtener combinaciones

    combos = []

    if len(numeros) == 2:
        print(numeros)
        return [[numeros[0], numeros[1]], [numeros[1], numeros[0]]]

    else:
        for numero in numeros:
            numero2 = numeros[:]
            numero2.remove(numero)
            combos.extend([x + [numero] for x in jeje_15(numero2)])


    print(len(combos))
    print(combos)
    return combos

def jeje_16():
    i = 0
    while i != 362892:
        i += 1

jeje_16()
