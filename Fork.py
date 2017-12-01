
# Example from
# https://docs.python.org/3/library/multiprocessing.html
from multiprocessing import Process
import os
"""
def info(title):
    print(title)
    print('module name:', __name__)
    if hasattr(os, 'getppid'):  # only available on Unix
        print('parent process:', os.getppid())
    print('process id:', os.getpid())

def funcionX(name):
    info('function f')
    print('hello', name)

def main():
    info('main line')
    p = Process(target=funcionX, args=('bob',))
    p.start()
    p.join()


if __name__ == '__main__':
    main()
"""

# !/usr/bin/env python
# -*- coding: utf-8 -*-
from multiprocessing import Process, Queue
from urllib.request import urlopen
from urllib.error import URLError
from time import time
from queue import Empty

# Carácteres alfanuméricos.
NAME_VALID_CHARS = [chr(i) for i in list(range(48, 58)) + list(range(97, 123))]


def chars_filter(s):
    """Remover carácteres inválidos."""
    return "".join([c if c in NAME_VALID_CHARS else "" for c in s.lower()])


def download_page_content(url):
    print("Downloading %s..." % url)
    try:
        r = urlopen(url)
    except URLError as e:
        print("Error al acceder a %s." % url)
        print(e)
    else:
        filename = chars_filter(url.lower()) + ".html"
        try:
            f = open(filename, "w")
        except IOError as e:
            print("Error al abrir %s." % filename)
            print(e)
        else:
            f.write(str(r.read()))
            f.close()
            r.close()


def worker(queue):
    """
    Toma un ítem de la cola y descarga su contenido,
    hasta que la misma se encuentre vacía.
    """
    while True:
        try:
            url = queue.get_nowait()
        except Empty:
            break
        else:
            download_page_content(url)


def main():
    urls = (
        "http://python.org/",
        "http://perl.org/",
        "http://ruby-lang.org/",
        "http://rust-lang.org/",
        "http://php.net/",
        "http://stackless.com/",
        "http://pypy.org/",
        "http://jython.org/",
        "http://ironpython.net/"
    )

    queue = Queue(9)
    for url in urls:
        queue.put(url)

    processes = []
    for i in range(3):
        processes.append(Process(target=worker, args=(queue,)))
        processes[i].start()
        print("Proceso %d lanzado." % (i + 1))

    for process in processes:
        process.join()

    print("La ejecución a concluído.")


if __name__ == "__main__":
    main()