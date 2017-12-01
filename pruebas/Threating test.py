import threading
from queue import Queue
import time


tarea_completada = threading.Lock() # esta variable se encarga de mantener una sincronia entre los hilos
cola = Queue()

def funcionX(tarea):
    time.sleep(1)

    with tarea_completada:
        print('Hilo: ',threading.current_thread().name,' Tarea numero: ',tarea)


def threader():
    while True:
        tarea = cola.get()
        funcionX(tarea)
        cola.task_done()

######La prueba comienza aqui##########################################################################

def prueba():
    
    numero_hilos = int(input('Cuantos hilos desea utilizar? '))
    for counter in range(numero_hilos):
        thread = threading.Thread(target = threader)
        thread.start()


    numero_tareas = int(input('Cuantas tareas quiere realizar? cada tarea tarda 1 segundo: '))
    start = time.time()

    for tarea in range(numero_tareas):
        cola.put(tarea)

    cola.join()

    print('El trabajo tomo: ',time.time()-start,' segundos')

    
prueba()

