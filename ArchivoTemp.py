import tempfile

class Archivo:
    def __init__(self):
        self.archivo = None

    def CrearArchivoTemp(self):
        self.archivo = tempfile.TemporaryFile()

    def EscribirEnArchivoTemp(self, contenido):
        self.archivo.write(contenido.encode('utf-8'))

    def LeerArchivoTemp(self):
        self.archivo.seek(0)
        return self.archivo.read().decode('utf-8')

    def CerrarArchivoTemp(self):
        self.archivo.close()

    def ObtenerDirectorio(self):
        return tempfile.gettempdir() + '/' + tempfile.gettempprefix()
