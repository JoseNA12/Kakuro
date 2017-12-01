class Casilla(object): # Utilizada en MostrarKakuro (Kakuro sin resolver y resuelto)
    def __init__(self, pTipoCasilla, pPosicionX, pPosicionY):
        self.tipoCasilla = pTipoCasilla
        self.contenido = []
        self.posicionX = pPosicionX
        self.posicionY = pPosicionY

    def setTipoCasilla(self, pTipo):
        self.tipoCasilla = pTipo
    def getTipoCasilla(self):
        return self.tipoCasilla

    def addContenido(self, pElementoH, pElementoV):
        self.contenido.append(pElementoH)
        self.contenido.append(pElementoV)
    def getContenido(self):
        return self.contenido
    def deleteContenido(self):
        del self.contenido[:]

    def setPosicionX(self, pPosicionX):
        self.posicionX = pPosicionX
    def getPosicionX(self):
        return self.posicionX

    def setPosicionY(self, pPosicionY):
        self.posicionY = pPosicionY
    def getPosicionY(self):
        return self.posicionY
