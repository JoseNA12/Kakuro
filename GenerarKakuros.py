
from TipoCelda import TipoCelda
from Celda import CasillaGenerador
import random
from multiprocessing import Process, Queue
import threading


class Generador:
    conHilos = False
    conForks = False

    def __init__(self, dimension):
        self.matrizKakuro = []
        self.dimension = dimension
        self.matrizHorizontal = []
        self.matrizVertical = []

    def ActivarHilos(self, estado):
            self.conHilos = estado

    def DesactivarHilos(self, estado):
        self.conHilos = estado

    def ActivarForks(self, estado):
        self.conForks = estado

    def DesactivarForks(self, estado):
        self.conForks = estado

    def EjecutarFuncionConHilos(self, funcion):
        if self.conHilos == False:
            funcion()

        else:
            thread = threading.Thread(target=funcion)
            thread.start()
            thread.join()

    def EjecutarFuncionConForks(self, funcion):
        if self.conForks == False:
            funcion()

        else:
            processes = Process(target=funcion)
            processes.start()

			
    def getMatrizKakuro(self):
        return self.matrizKakuro

    def getDimension(self):
        return self.dimension

    def setDimension(self, dimension):
        self.dimension = dimension

    def getMatrizHorizontal(self):
        return self.matrizHorizontal

    def getMatrizVertical(self):
        return self.matrizVertical

    def AniadirCero(self, numero):
        return "0" + str(numero)

    def meterEnMatrices(self):
        self.matrizHorizontal = []
        self.matrizVertical = []

        for i in range(self.dimension):
            self.matrizHorizontal.append([])
            self.matrizVertical.append([])

            for j in range(self.dimension):

                digitoSuperior = str(self.matrizKakuro[i][j].getValorSuperior())
                digitoInferior = str(self.matrizKakuro[i][j].getValorInferior())

                if digitoSuperior.isdigit():
                    if len(str(digitoSuperior)) == 1:
                        digitoSuperior = self.AniadirCero(digitoSuperior)

                if digitoInferior.isdigit():
                    if len(str(digitoInferior)) == 1:
                        digitoInferior = self.AniadirCero(digitoInferior)

                if (self.matrizKakuro[i][j].getTipoCelda() == TipoCelda.NEGRO):
                    self.matrizHorizontal[i].append("XX")
                    self.matrizVertical[i].append("XX")

                else:
                    if (self.matrizKakuro[i][j].getTipoCelda() == TipoCelda.BLANCO):
                        self.matrizHorizontal[i].append("00")
                        self.matrizVertical[i].append("00")
                    else:
                        if (self.matrizKakuro[i][j].getTipoCelda() == TipoCelda.LLAVE_H):
                            self.matrizHorizontal[i].append(digitoSuperior)
                            self.matrizVertical[i].append("XX")
                        else:
                            if (self.matrizKakuro[i][j].getTipoCelda() == TipoCelda.LLAVE_V):
                                self.matrizHorizontal[i].append("XX")
                                self.matrizVertical[i].append(digitoInferior)
                            else:
                                if (self.matrizKakuro[i][j].getTipoCelda() == TipoCelda.LLAVE_H_V):
                                    self.matrizHorizontal[i].append(digitoSuperior)
                                    self.matrizVertical[i].append(digitoInferior)

    def GenerarMatrizKakuro(self):

        self.matrizKakuro = []

        for indice in range(self.dimension):
            self.matrizKakuro.append([])

            for indice2 in range(self.dimension):
                casilla = CasillaGenerador(TipoCelda.BLANCO)
                self.matrizKakuro[indice].append(casilla)

    def tiposRandom(self, negro, blanco, llave_V, llave_H, llave_H_V):
        lista = []
        if negro:
            lista.append(TipoCelda.NEGRO)
        if blanco:
            lista.append(TipoCelda.BLANCO)
        if llave_V:
            lista.append(TipoCelda.LLAVE_V)
        if llave_H:
            lista.append(TipoCelda.LLAVE_H)
        if llave_H_V:
            lista.append(TipoCelda.LLAVE_H_V)

        select = int(random.random() * len(lista))
        return lista[select]

    def PrimerasFilasNegras(self):
        for i in range(self.dimension):
            for j in range(self.dimension):
                self.matrizKakuro[i][0].setTipoCelda(TipoCelda.NEGRO)
                self.matrizKakuro[0][j].setTipoCelda(TipoCelda.NEGRO)

    def GenerarTipos(self):
        tamanioKakuro = self.dimension * self.dimension
        limiteDeNegros = int((tamanioKakuro * 30) / 100) - 5

        coord_X_Y_Usadas = []

        contadorDeNegros = 0
        self.EjecutarFuncionConForks(self.PrimerasFilasNegras)
        self.EjecutarFuncionConHilos(self.PrimerasFilasNegras)


        while contadorDeNegros <= limiteDeNegros:
            coord_X = random.randint(1, self.dimension - 1)  # [i for i in range(1, self.dimension)]
            coord_Y = random.randint(1, self.dimension - 1)

            if (coord_X, coord_Y) not in coord_X_Y_Usadas:

                self.matrizKakuro[coord_X][coord_Y].setTipoCelda(TipoCelda.NEGRO)
                coord_X_Y_Usadas.append((coord_X, coord_Y))
                contadorDeNegros += 1

        for i in range(self.dimension):
            for j in range(self.dimension):

                if self.matrizKakuro[i][j].getTipoCelda() == TipoCelda.BLANCO:
                    blancosDerecha = self.verificarBlancosDerecha(i, j)
                    blancosAbajo = self.verificarBlancosAbajo(i, j)

                    if blancosDerecha[0] > 8:
                        self.matrizKakuro[i][j + 8].setTipoCelda(TipoCelda.NEGRO)

                    if blancosAbajo[0] > 8:
                        self.matrizKakuro[i + 8][j].setTipoCelda(TipoCelda.NEGRO)


        i = 0
        while i != 4: # Verificar varias veces
            for a in range(self.dimension):

                for b in range(self.dimension):

                    if (self.matrizKakuro[a][b].getTipoCelda() == TipoCelda.BLANCO):
                        negrosArriba = self.verificarNegrosArriba(a, b)
                        negrosIzq = self.verificarNegrosIzquierda(a, b)
                        negrosAbajo = self.verificarNegrosAbajo(a, b)
                        negrosDer = self.verificarNegrosDerecha(a, b)

                        if (negrosArriba[1] == True) & (negrosAbajo[1] == True):
                            self.matrizKakuro[a][b].setTipoCelda(TipoCelda.NEGRO)

                        if (negrosIzq[1] == True) & (negrosDer[1] == True):
                            self.matrizKakuro[a][b].setTipoCelda(TipoCelda.NEGRO)

                        # Última fila
                        if (negrosArriba[1] == True) & (a == self.dimension - 1):
                            self.matrizKakuro[a][b].setTipoCelda(TipoCelda.NEGRO)

                        # Última columna
                        if (negrosIzq[1] == True) & (b == self.dimension - 1):
                            self.matrizKakuro[a][b].setTipoCelda(TipoCelda.NEGRO)

            i += 1

        self.GenerarPermutaciones()
        self.AsignarLlavesCasillas()

        # self.EstablecerValoresLlave() # el del suarez
        # self.AsignarValoresCasillasBlancas() # el del suarez

    def CrearFormasTablero(self, dimension):

        if (self.dimension == 10):
            opcion = random.randint(1, 2)

            if opcion == 1:
                x = 9
                y = 4
                contador = 0

                while True:
                    if contador == 8:
                        break

                    if x == 5:
                        x = 9
                        y = 5

                    self.matrizKakuro[x][y].setTipoCelda(TipoCelda.NEGRO)
                    contador += 1
                    x -= 1

                self.matrizKakuro[9][3].setTipoCelda(TipoCelda.NEGRO)
                self.matrizKakuro[9][6].setTipoCelda(TipoCelda.NEGRO)

            if opcion == 2:
                x = 3
                y = 5
                contador = 0
                horizontal = False

                while True:
                    if contador == 10:
                        break

                    if x == 8:
                        horizontal = True
                        x = 5
                        y = 3

                    self.matrizKakuro[x][y].setTipoCelda(TipoCelda.NEGRO)
                    contador += 1

                    if horizontal == False:
                        x += 1
                    else:
                        y += 1

                self.matrizKakuro[4][4].setTipoCelda(TipoCelda.NEGRO)
                self.matrizKakuro[4][6].setTipoCelda(TipoCelda.NEGRO)
                self.matrizKakuro[6][4].setTipoCelda(TipoCelda.NEGRO)
                self.matrizKakuro[6][6].setTipoCelda(TipoCelda.NEGRO)

        if (self.dimension == 11):
            self.matrizKakuro[5][5].setTipoCelda(TipoCelda.NEGRO)  # Cuadrado del centro
            self.matrizKakuro[5][6].setTipoCelda(TipoCelda.NEGRO)
            self.matrizKakuro[6][5].setTipoCelda(TipoCelda.NEGRO)
            self.matrizKakuro[6][6].setTipoCelda(TipoCelda.NEGRO)

            self.matrizKakuro[1][5].setTipoCelda(TipoCelda.NEGRO)  # Cuadrado arriba
            self.matrizKakuro[1][6].setTipoCelda(TipoCelda.NEGRO)
            self.matrizKakuro[2][5].setTipoCelda(TipoCelda.NEGRO)
            self.matrizKakuro[2][6].setTipoCelda(TipoCelda.NEGRO)

            self.matrizKakuro[5][1].setTipoCelda(TipoCelda.NEGRO)  # Cuadrado izquierda
            self.matrizKakuro[5][2].setTipoCelda(TipoCelda.NEGRO)
            self.matrizKakuro[6][1].setTipoCelda(TipoCelda.NEGRO)
            self.matrizKakuro[6][2].setTipoCelda(TipoCelda.NEGRO)

            self.matrizKakuro[9][5].setTipoCelda(TipoCelda.NEGRO)  # Cuadrado abajo
            self.matrizKakuro[9][6].setTipoCelda(TipoCelda.NEGRO)
            self.matrizKakuro[10][5].setTipoCelda(TipoCelda.NEGRO)
            self.matrizKakuro[10][6].setTipoCelda(TipoCelda.NEGRO)

            self.matrizKakuro[5][9].setTipoCelda(TipoCelda.NEGRO)  # Cuadrado derecha
            self.matrizKakuro[5][10].setTipoCelda(TipoCelda.NEGRO)
            self.matrizKakuro[6][9].setTipoCelda(TipoCelda.NEGRO)
            self.matrizKakuro[6][10].setTipoCelda(TipoCelda.NEGRO)

        if (self.dimension >= 12):

            j = 1

            opcionMayor_A_16 = random.randint(5, 7)
            opcionMenor_A_16 = random.randint(6, 9)
            indice_i_2 = random.randint(11, 15)

            while j <= self.dimension - 1:  # Limite horizontal

                mayor_A_16 = False

                if (self.dimension >= 16):
                    opcion = opcionMayor_A_16
                    mayor_A_16 = True
                else:
                    opcion = opcionMenor_A_16

                i_1 = opcion
                i_2 = indice_i_2

                try:
                    self.matrizKakuro[i_1][j].setTipoCelda(TipoCelda.NEGRO)
                    self.matrizKakuro[i_1][j + 1].setTipoCelda(TipoCelda.NEGRO)

                    if mayor_A_16 == True:
                        self.matrizKakuro[i_2][j].setTipoCelda(TipoCelda.NEGRO)
                        self.matrizKakuro[i_2][j + 1].setTipoCelda(TipoCelda.NEGRO)
                        mayor_A_16 = False

                except:
                    print

                j += 2

            i = 1

            opcionMayor_A_16 = random.randint(5, 7)
            opcionMenor_A_16 = random.randint(6, 9)
            indice_i_2 = random.randint(11, 15)

            while i <= self.dimension - 1:  # Limite vertical

                mayor_A_16 = False

                if (self.dimension >= 16):
                    opcion = opcionMayor_A_16  # random.randint(5, 7)
                    mayor_A_16 = True
                else:
                    opcion = opcionMenor_A_16  # random.randint(6, 9)

                i_1 = opcion
                i_2 = indice_i_2  # random.randint(11, 15)

                try:
                    self.matrizKakuro[i][i_1].setTipoCelda(TipoCelda.NEGRO)
                    self.matrizKakuro[i + 1][i_1].setTipoCelda(TipoCelda.NEGRO)

                    if mayor_A_16 == True:
                        self.matrizKakuro[i][i_2].setTipoCelda(TipoCelda.NEGRO)
                        self.matrizKakuro[i + 1][i_2].setTipoCelda(TipoCelda.NEGRO)
                        mayor_A_16 = False

                except:
                    print

                i += 2

    def PerfeccionarTablero(self):

        for x in range(self.dimension):

            for y in range(self.dimension):

                existen_BlancosArriba = self.verificarBlancosArriba(x, y)
                existen_BlancosIzquierda = self.verificarBlancosIzquierda(x, y)
                existen_BlancosAbajo = self.verificarBlancosAbajo(x, y)
                existen_BlancosDerecha = self.verificarBlancosDerecha(x, y)

                existen_NegrosArriba = self.verificarNegrosArriba(x, y)
                existen_NegrosIzquierda = self.verificarNegrosIzquierda(x, y)
                existen_NegrosAbajo = self.verificarNegrosAbajo(x, y)
                existen_NegrosDerecha = self.verificarNegrosDerecha(x, y)

                if (x == self.dimension - 1) & (y == self.dimension - 1):  # Ultima casilla negra o blanca

                    if (existen_BlancosIzquierda[1] == True) & (existen_BlancosArriba[1] == True):
                        if (existen_BlancosIzquierda[0] > 1) & (existen_BlancosArriba[0] > 1):
                            opcion = random.randint(0, 1)
                            if opcion == 1:
                                self.matrizKakuro[x][y].setTipoCelda(TipoCelda.NEGRO)
                            else:
                                self.matrizKakuro[x][y].setTipoCelda(TipoCelda.BLANCO)

                else:

                    if (x == self.dimension - 1):  # Ultima fila

                        if (existen_BlancosArriba[1] == True) & (existen_BlancosArriba[0] > 1):
                            if (existen_BlancosIzquierda[1] == True) & (existen_BlancosIzquierda[0] > 1):
                                if (existen_BlancosDerecha[1] == True) & (existen_BlancosDerecha[0] > 1):
                                    self.matrizKakuro[x][y].setTipoCelda(TipoCelda.NEGRO)
                    else:
                        if (y == self.dimension - 1):  # Ultima columna

                            if (existen_BlancosArriba[1] == True) & (existen_BlancosArriba[0] > 1):
                                if (existen_BlancosIzquierda[1] == True) & (existen_BlancosIzquierda[0] > 1):
                                    if (existen_BlancosAbajo[1] == True) & (existen_BlancosAbajo[0] > 1):
                                        self.matrizKakuro[x][y].setTipoCelda(TipoCelda.NEGRO)

                            # TODO: PUTAAAAAAAAA
                            if (existen_BlancosArriba[1] == 1) & (existen_BlancosAbajo[1] == 1) & (
                                existen_BlancosIzquierda[1] > 1):
                                self.matrizKakuro[x][y].setTipoCelda(TipoCelda.NEGRO)
                            else:
                                if (existen_NegrosArriba[0] == True) & (existen_NegrosAbajo[0] == True) & (
                                    existen_BlancosIzquierda[1] > 1):
                                    self.matrizKakuro[x][y].setTipoCelda(TipoCelda.NEGRO)

                                    # TODO: ================================

                        else:
                            if (existen_BlancosArriba[1] == True) & (existen_BlancosArriba[0] > 1):
                                if (existen_BlancosIzquierda[1] == True) & (existen_BlancosIzquierda[0] > 1):
                                    if (existen_BlancosAbajo[1] == True) & (existen_BlancosAbajo[0] > 1):
                                        if (existen_BlancosDerecha[1] == True) & (existen_BlancosDerecha[0] > 1):
                                            self.matrizKakuro[x][y].setTipoCelda(TipoCelda.NEGRO)


                            else:
                                if (existen_BlancosArriba[1] == True) & (existen_BlancosArriba[0] > 1):
                                    if (existen_BlancosIzquierda[1] == True) & (existen_BlancosIzquierda[0] > 1):
                                        if (existen_BlancosAbajo[1] == True) & (existen_BlancosAbajo[0] > 1):
                                            if (existen_NegrosDerecha[1] == True):
                                                self.matrizKakuro[x][y].setTipoCelda(TipoCelda.NEGRO)

                                else:
                                    if (existen_BlancosArriba[1] == True) & (existen_BlancosArriba[0] > 1):
                                        if (existen_BlancosIzquierda[1] == True) & (existen_BlancosIzquierda[0] > 1):
                                            if (existen_NegrosAbajo[1] == True):
                                                if (existen_BlancosDerecha[1] == True) & (
                                                    existen_BlancosDerecha[0] > 1):
                                                    self.matrizKakuro[x][y].setTipoCelda(TipoCelda.NEGRO)

                                    else:
                                        if (existen_BlancosArriba[1] == True) & (existen_BlancosArriba[0] > 1):
                                            if (existen_NegrosIzquierda[1] == True):
                                                if (existen_BlancosAbajo[1] == True) & (existen_BlancosAbajo[0] > 1):
                                                    if (existen_BlancosDerecha[1] == True) & (
                                                        existen_BlancosDerecha[0] > 1):
                                                        self.matrizKakuro[x][y].setTipoCelda(TipoCelda.NEGRO)

                                        else:
                                            if (existen_NegrosArriba[1] == True):
                                                if (existen_BlancosIzquierda[1] == True) & (
                                                    existen_BlancosIzquierda[0] > 1):
                                                    if (existen_BlancosAbajo[1] == True) & (
                                                        existen_BlancosAbajo[0] > 1):
                                                        if (existen_BlancosDerecha[1] == True) & (
                                                            existen_BlancosDerecha[0] > 1):
                                                            self.matrizKakuro[x][y].setTipoCelda(TipoCelda.NEGRO)

    # El suarez
    def AsignarValoresCasillasBlancas(self):
        listaV = []

        for x in range(self.dimension):

            listaH = []

            for y in range(self.dimension):
                if (self.matrizKakuro[x][y].getTipoCelda() == TipoCelda.LLAVE_V) | (
                    self.matrizKakuro[x][y].getTipoCelda() == TipoCelda.LLAVE_H_V):
                    b = 1

                    while True:

                        digito = random.randint(1, 9)

                        if (digito in listaV) == False:
                            listaV.append(digito)
                            self.matrizKakuro[x + b][y].setValorContenido(digito)
                            b += 1

                            if x + b == self.dimension:
                                listaV = []
                                break

                            if self.matrizKakuro[x + b][y].getTipoCelda() != TipoCelda.BLANCO:
                                listaV = []
                                break

                else:
                    if self.matrizKakuro[x][y].getTipoCelda() == TipoCelda.BLANCO:

                        if self.matrizKakuro[x][y].getValorContenido() == 0:

                            while True:

                                digito = random.randint(1, 9)
                                if (digito in listaH) == False:
                                    listaH.append(digito)
                                    self.matrizKakuro[x][y].setValorContenido(digito)
                                    break

                                elif (x == self.dimension - 1) & (y == self.dimension - 1):
                                    break

                        else:
                            if (self.matrizKakuro[x][y].getValorContenido() in listaH) == False:
                                listaH.append(self.matrizKakuro[x][y].getValorContenido())
                            else:

                                digito = random.randint(1, 9)
                                if (digito in listaH) == False:
                                    listaH.append(digito)
                                    self.matrizKakuro[x][y].setValorContenido(digito)

                    else:
                        listaH.clear()

        """
        for i in range(self.dimension):
            for o in range(self.dimension):
                print(self.matrizKakuro[i][o].getValorContenido())
                """
        self.EstablecerValoresLlave()

    def EstablecerValoresLlave(self):

        for i in range(self.dimension):
            listaV = []
            listaH = []
            for j in range(self.dimension):

                if (self.matrizKakuro[i][j].getTipoCelda() == TipoCelda.LLAVE_V) | (
                            self.matrizKakuro[i][j].getTipoCelda() == TipoCelda.LLAVE_H_V):
                    b = 1
                    while True:
                        if i + b >= self.dimension:
                            listaV = []
                            break;
                        elif self.matrizKakuro[i + b][j].getTipoCelda() == TipoCelda.BLANCO:

                            numero = random.randint(1, 9)
                            # print(numero)
                            if (numero in listaV) == False:
                                try:
                                    self.matrizKakuro[i + b][j].setValorContenido(numero)
                                    listaV.append(numero)
                                    b += 1
                                except:
                                    listaV = []
                                    break


                        else:
                            listaV = []
                            break


            else:
                if (self.matrizKakuro[i][j].getTipoCelda() == TipoCelda.BLANCO):
                    if self.matrizKakuro[i][j].getValorContenido() == 0:
                        numero = random.randint(1, 9)
                        if numero in listaH == False:
                            self.matrizKakuro[i][j].setValorContenido(numero)
                            listaH.append(numero)
                        else:
                            listaH.append(self.matrizKakuro[i][j].getValorContenido())

        self.EstablecerSumatoria()

    def EstablecerSumatoria(self):
        for i in range(self.dimension):

            for j in range(self.dimension):
                suma = 0
                if self.matrizKakuro[i][j].getTipoCelda() == TipoCelda.LLAVE_H:
                    b = 1
                    while True:
                        try:
                            if self.matrizKakuro[i][j + b].getTipoCelda() == TipoCelda.BLANCO:
                                suma += self.matrizKakuro[i][j + b].getValorContenido()
                                b += 1
                            else:
                                self.matrizKakuro[i][j].setValorSuperior(suma)
                                suma = 0
                                break
                        except:
                            self.matrizKakuro[i][j].setValorSuperior(suma)
                            suma = 0
                            break
                else:
                    if self.matrizKakuro[i][j].getTipoCelda() == TipoCelda.LLAVE_V:
                        b = 1
                        while True:
                            try:
                                if self.matrizKakuro[i + b][j].getTipoCelda() == TipoCelda.BLANCO:
                                    suma += self.matrizKakuro[i + b][j].getValorContenido()
                                    b += 1
                                else:
                                    self.matrizKakuro[i][j].setValorInferior(suma)
                                    suma = 0
                                    break
                            except:
                                self.matrizKakuro[i][j].setValorInferior(suma)
                                suma = 0
                                break

                    else:
                        if self.matrizKakuro[i][j].getTipoCelda() == TipoCelda.LLAVE_H_V:
                            b = 1
                            while True:
                                try:
                                    if self.matrizKakuro[i][j + b].getTipoCelda() == TipoCelda.BLANCO:
                                        suma += self.matrizKakuro[i][j + b].getValorContenido()
                                        b += 1
                                    else:
                                        self.matrizKakuro[i][j].setValorSuperior(suma)
                                        suma = 0
                                        break
                                except:
                                    self.matrizKakuro[i][j].setValorSuperior(suma)
                                    suma = 0
                                    break

                            b = 1
                            while True:
                                try:
                                    if self.matrizKakuro[i + b][j].getTipoCelda() == TipoCelda.BLANCO:
                                        suma += self.matrizKakuro[i + b][j].getValorContenido()
                                        b += 1
                                    else:
                                        self.matrizKakuro[i][j].setValorInferior(suma)
                                        suma = 0
                                        break
                                except:
                                    self.matrizKakuro[i][j].setValorInferior(suma)
                                    suma = 0
                                    break

    # =========================================


    # El navarro
    def GenerarPermutaciones(self):
        posibilidades = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        for i in range(self.dimension):
            for j in range(self.dimension):

                if (self.matrizKakuro[i][j].getTipoCelda() == TipoCelda.BLANCO):

                    izq = []
                    der = []
                    arriba = []
                    abajo = []

                    a = 1
                    while (self.matrizKakuro[i][j - a].getTipoCelda() == TipoCelda.BLANCO):
                        izq.append(self.matrizKakuro[i][j - a].getValorContenido())
                        a += 1

                    b = 1
                    try:
                        while (self.matrizKakuro[i][j + b].getTipoCelda() == TipoCelda.BLANCO):
                            der.append(self.matrizKakuro[i][j + b].getValorContenido())
                            b += 1
                    except:
                        print

                    c = 1
                    try:
                        while(self.matrizKakuro[i + c][j].getTipoCelda() == TipoCelda.BLANCO):
                            abajo.append(self.matrizKakuro[i + c][j].getValorContenido())
                            c += 1
                    except:
                        print

                    d = 1
                    while (self.matrizKakuro[i - d][j].getTipoCelda() == TipoCelda.BLANCO):
                        arriba.append(self.matrizKakuro[i - d][j].getValorContenido())
                        d += 1

                    valores = arriba + abajo + izq + der

                    k = 0
                    while k <= 8:
                        if posibilidades[k] not in valores:
                            self.matrizKakuro[i][j].setValorContenido(posibilidades[k])
                            break

                        k += 1


    def AsignarLlavesCasillas(self):

        for i in range(self.dimension):

            for j in range(self.dimension):

                if (self.matrizKakuro[i][j].getTipoCelda() == TipoCelda.NEGRO):
                    blancasDerecha = self.verificarBlancosDerecha(i, j)
                    blancasAbajo = self.verificarBlancosAbajo(i, j)
                    valorLlaveH = 0
                    valorLlaveV = 0

                    if ((blancasDerecha[1] == True) & (blancasDerecha[0] > 1)) & ((blancasAbajo[1] == True) & (blancasAbajo[0] > 1)):
                        self.matrizKakuro[i][j].setTipoCelda(TipoCelda.LLAVE_H_V)

                        a = 1
                        try:
                            while self.matrizKakuro[i][j + a].getTipoCelda() == TipoCelda.BLANCO:
                                valorLlaveH += self.matrizKakuro[i][j + a].getValorContenido()
                                a += 1
                        except:
                            print
                        finally:
                            self.matrizKakuro[i][j].setValorSuperior(valorLlaveH)

                        b = 1
                        try:
                            while self.matrizKakuro[i + b][j].getTipoCelda() == TipoCelda.BLANCO:
                                valorLlaveV += self.matrizKakuro[i + b][j].getValorContenido()
                                b += 1
                        except:
                            print
                        finally:
                            self.matrizKakuro[i][j].setValorInferior(valorLlaveV)

                    else:
                        if (blancasDerecha[1] == True) & (blancasDerecha[0] > 1):
                            self.matrizKakuro[i][j].setTipoCelda(TipoCelda.LLAVE_H)

                            a = 1
                            try:
                                while self.matrizKakuro[i][j + a].getTipoCelda() == TipoCelda.BLANCO:
                                    valorLlaveH += self.matrizKakuro[i][j + a].getValorContenido()
                                    a += 1
                            except:
                                print
                            finally:
                                self.matrizKakuro[i][j].setValorSuperior(valorLlaveH)

                        else:
                            if (blancasAbajo[1] == True) & (blancasAbajo[0] > 1):
                                self.matrizKakuro[i][j].setTipoCelda(TipoCelda.LLAVE_V)

                                b = 1
                                try:
                                    while self.matrizKakuro[i + b][j].getTipoCelda() == TipoCelda.BLANCO:
                                        valorLlaveV += self.matrizKakuro[i + b][j].getValorContenido()
                                        b += 1
                                except:
                                    print
                                finally:
                                    self.matrizKakuro[i][j].setValorInferior(valorLlaveV)


                                # self.EstablecerValoresLlave()

    # =========================================


    def verificarNegrosArriba(self, x, y):
        b = 1
        contador = 0

        try:
            while (self.matrizKakuro[x - b][y].getTipoCelda() == TipoCelda.NEGRO):
                contador += 1
                b += 1

            return [contador, True] if contador != 0 else [0, False]
        except:
            return [contador, True] if contador != 0 else [contador, False]

    def verificarNegrosIzquierda(self, x, y):
        b = 1
        contador = 0

        try:
            while (self.matrizKakuro[x][y - b].getTipoCelda() == TipoCelda.NEGRO):
                contador += 1
                b += 1

            return [contador, True] if contador != 0 else [0, False]
        except:
            return [contador, True] if contador != 0 else [contador, False]

    def verificarNegrosAbajo(self, x, y):
        b = 1
        contador = 0

        try:
            while (self.matrizKakuro[x + b][y].getTipoCelda() == TipoCelda.NEGRO):
                contador += 1
                b += 1

            return [contador, True] if contador != 0 else [contador, False]
        except:
            return [contador, True] if contador != 0 else [contador, False]

    def verificarNegrosDerecha(self, x, y):
        b = 1
        contador = 0

        try:
            while (self.matrizKakuro[x][y + b].getTipoCelda() == TipoCelda.NEGRO):
                contador += 1
                b += 1

            return [contador, True] if contador != 0 else [contador, False]
        except:
            return [contador, True] if contador != 0 else [contador, False]

    def verificarBlancosArriba(self, x, y):
        b = 1
        contador = 0

        try:
            while (self.matrizKakuro[x - b][y].getTipoCelda() == TipoCelda.BLANCO):
                contador += 1
                b += 1

            return [contador, True] if contador != 0 else [0, False]
        except:
            return [contador, True] if contador != 0 else [contador, False]

    def verificarBlancosIzquierda(self, x, y):
        b = 1
        contador = 0

        try:
            while (self.matrizKakuro[x][y - b].getTipoCelda() == TipoCelda.BLANCO):
                contador += 1
                b += 1

            return [contador, True] if contador != 0 else [0, False]
        except:
            return [contador, True] if contador != 0 else [contador, False]

    def verificarBlancosAbajo(self, x, y):
        b = 1
        contador = 0

        try:
            while (self.matrizKakuro[x + b][y].getTipoCelda() == TipoCelda.BLANCO):
                contador += 1
                b += 1

            return [contador, True] if contador != 0 else [contador, False]
        except:
            return [contador, True] if contador != 0 else [contador, False]

    def verificarBlancosDerecha(self, x, y):
        b = 1
        contador = 0

        try:
            while (self.matrizKakuro[x][y + b].getTipoCelda() == TipoCelda.BLANCO):
                contador += 1
                b += 1

            return [contador, True] if contador != 0 else [contador, False]
        except:
            return [contador, True] if contador != 0 else [contador, False]

    def verificarArriba(self, x, y):  # Verificar si se puede poner una casilla NO BLANCA abajo

        tipo = self.matrizKakuro[x - 1][y].getTipoCelda()
        if (tipo == TipoCelda.LLAVE_H_V) | (tipo == TipoCelda.LLAVE_V):
            return False

        else:
            return True

    def verificarIzquierda(self, x,
                           y):  # Verificar si a la izquierda hay una casilla H_V, o H. False si tiene, True si no

        tipo = self.matrizKakuro[x][y - 1].getTipoCelda()
        if (tipo == TipoCelda.LLAVE_H_V) | (tipo == TipoCelda.LLAVE_H):
            return False

        else:
            return True

    def verificarDerecha(self, x, y):
        if y == self.dimension - 1:
            return False
        else:
            return True


    def obtenerRangoHorizontal(self, a, b):

        contador = 1
        y = b + 1

        if (y == self.dimension - 1):
            return 1

        try:
            contador = 0
            while self.matrizKakuro[a][y].getTipoCelda() == TipoCelda.BLANCO:
                contador += 1
                y += 1
        except IndexError:
            print

        return contador

    def obtenerRangoVertical(self, a, b):

        contador = 1
        x = a + 1

        if (x == self.dimension - 1):
            return 1

        try:
            contador = 0

            while self.matrizKakuro[x][b].getTipoCelda() == TipoCelda.BLANCO:
                contador += 1
                x += 1
        except IndexError:
            print

        return contador

    def calcularNumeroLlave(self, numeroCasillasLibre):
        valorMaximo = self.diccionarioValoresLlaveMaximos(numeroCasillasLibre)
        valorMinimo = self.diccionarioValoresLlaveMinimos(numeroCasillasLibre)

        llaveGenerada = random.randint(valorMinimo, valorMaximo)

        return llaveGenerada

    def switchValoresLlaveMaximos(self, numeroCasillasLibre):
        return {
            # Numero de casillas libre : Valores maximos a tomar
            1: 9,
            2: 17,
            3: 24,
            4: 30,
            5: 35,
            6: 39,
            7: 42,
            8: 44,
            9: 45
        }.get(numeroCasillasLibre)

    def switchValoresLlaveMinimos(self, numeroCasillasLibre):
        return {
            # Numero de casillas libre : Valores minimos a tomar
            1: 1,
            2: 3,
            3: 6,
            4: 10,
            5: 15,
            6: 21,
            7: 28,
            8: 36,
            9: 45
        }.get(numeroCasillasLibre)

    ##primer elemento de fila no puede ser casilla libre.  la ultima casilla matriz no puede tener casillas horizontales. Segunda fila no debe tener llaves a menos
    # que existan casillas libres a a partir de 1


