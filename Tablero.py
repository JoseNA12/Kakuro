class Tablero(object):
    def __init__(self):
        self.tamanio = 0
        self.dimension = 0
        self.tamanioLetra = 0
        self.casillas = []

    def setTamanio(self, tamanio):
        self.tamanio = tamanio
    def getTamanio(self):
        return self.tamanio

    def setDimension(self, dimension):
        self.dimension = dimension
    def getDimension(self):
        return self.dimension

    def setTamanioLetra(self, tamanio):
        self.tamanioLetra = tamanio
    def getTamanioLetra(self):
        return self.tamanioLetra

    def addCasilla(self, pCasilla):
        self.casillas.append(pCasilla)
    def getCasillas(self):
        return self.casillas
    def deleteCasillas(self):
        self.casillas.clear()