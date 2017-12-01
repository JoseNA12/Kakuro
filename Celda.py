
import TipoCelda

class CasillaGenerador: # Utizada para crear kakuros
    def __init__(self, tipoCelda):
        self.tipoCelda = tipoCelda

        self.valorSuperior = 0
        self.valorInferior = 0
        self.valorContenido = 0
        self.cantidadSuperior = 0
        self.cantidadInferior = 0

        self.valoresPosibilidades = []

    def asignarCeldaSuperior(self, valorSuperior, cantidadSuperior):

        self.setTipoCelda(TipoCelda.TipoCelda.ARRIBA)
        self.valorSuperior = valorSuperior
        self.cantidadSuperior = cantidadSuperior

    def asignarCeldaMixta(self, valorSuperior, valorInferior, cantidadSuperior, cantidadInferior):

        self.setTipoCelda(TipoCelda.TipoCelda.CENTRO)
        self.valorSuperior = valorSuperior
        self.valorInferior = valorInferior
        self.cantidadSuperior = cantidadSuperior
        self.cantidadInferior = cantidadInferior

    def asignarCeldaInferior(self, valorInferior, cantidadInferior):

        self.setTipoCelda(TipoCelda.TipoCelda.ABAJO)
        self.valorInferior = valorInferior
        self.cantidadInferior = cantidadInferior

    def asignarCeldaBlanco(self):
        self.setTipoCelda(TipoCelda.TipoCelda.BLANCO)

    def asignarCeldaNeutro(self):
        self.setTipoCelda(TipoCelda.TipoCelda.NEUTRO)

    def asignarCeldaNegro(self):
        self.setTipoCelda(TipoCelda.TipoCelda.NEGRO)

    def getTipoCelda(self):
        return self.tipoCelda
    def setTipoCelda(self, tipocelda):
        self.tipoCelda = tipocelda

    def getValorSuperior(self):
        return self.valorSuperior
    def setValorSuperior(self, valor):
        self.valorSuperior= valor

    def getValorInferior(self):
        return self.valorInferior
    def setValorInferior(self, valor):
        self.valorInferior = valor

    def getValorContenido(self):
        return self.valorContenido
    def setValorContenido(self, valor):
        self.valorContenido = valor

    def getCantidadSuperior(self):
        return self.cantidadSuperior
    def setCantidadSuperior(self, valor):
        self.cantidadSuperior = valor

    def getCantidadInferior(self):
        return self.cantidadInferior
    def setCantidadInferior(self, valor):
        self.cantidadInferior = valor

    def setValoresPosibilidades(self, vector, posibleValor):
        self.valoresPosibilidades = [vector, posibleValor]
    def getValoresPosibilidades(self):
        return self.valoresPosibilidades