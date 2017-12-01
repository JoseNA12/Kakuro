import threading
from queue import Queue
import time


class Hilo:
    def __init__(self):

        self.tarea_completada = threading.Lock()  # esta variable se encarga de mantener una sincronia entre los hilos
        self.cola = Queue()
        self.miFuncion = funcion

    def getTareaCompletada(self):
        return self.tarea_completada

    def threader(self):
        while True:
           # print(self.miFuncion())
            tarea = self.cola.get()  # Obtener la tarea de la cola
            self.miFuncion()

            #self.funcionX(tarea)  # Función a ejecutar !!
            self.cola.task_done()  # Se indica a la cola que la tarea terminó


###### La prueba comienza aqui ######

#hilos = Hilo()


def prueba():
    numero_hilos = int(input('Cuantos hilos desea utilizar? '))
    for counter in range(numero_hilos):
        thread = threading.Thread(target=hilos.threader)  # Crear el hilo, target es la funcion que quiero ejecutar
        thread.start()  # Iniciar el hilo

    numero_tareas = int(input('Cuantas tareas quiere realizar? cada tarea tarda 1 segundo: '))
    start = time.time()  # Iniciar el cronómetro

    # La primer tarea es la última en ejecutarse, y la última tarea la primera en ejecutarse
    for tarea in range(numero_tareas):
        hilos.cola.put(tarea)  # Meter a la cola la tarea

        hilos.cola.join()  # Ejecutar el hilo

    print('El trabajo tomó: ', time.time() - start, ' segundos')


#prueba()