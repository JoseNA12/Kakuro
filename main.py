"""
José Navarro A.
Josué Suárez C.
Kakuro
2017
TEC
"""

from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from enum import Enum
import Tablero
import Casilla
import TipoCelda
#from ArchivoTemp import Archivo
import SolucionadorK
from GenerarKakuros import Generador
#from Hilo import Hilo


class InterfazUsuario():
    def __init__(self, master):
        self.ventanaPrincipal = master
        self.ventanaPrincipal.title("Kakuro AA")
        self.ventanaPrincipal.geometry("500x400") # +420+100
        self.ventanaPrincipal.resizable(0, 0)  # Evita expandir la ventana

        self.canvas = Canvas(self.ventanaPrincipal, bg="white")
        self.canvas.pack(side="top", fill="both", expand=True)

        # MENU
        self.menusBarra = Menu(self.ventanaPrincipal)  # Aquí van los submenús (Operaciones y Acerca de..)

        self.menuArchivo = Menu(self.menusBarra, tearoff=0)
        self.menusBarra.add_cascade(label="  Archivo  ", menu=self.menuArchivo)  # Se añade a la barra del menú
        self.menuArchivo.add_command(label="Abrir Kakuro", command=lambda: kakuro.AbrirKakuro())
        self.menuArchivo.add_command(label="Guardar Kakuro", command=lambda: kakuro.GuardarKakuro())

        self.menuOperaciones = Menu(self.menusBarra, tearoff=0)
        self.menusBarra.add_cascade(label="  Operaciones  ", menu=self.menuOperaciones)  # Se añade a la barra del menú

        self.menuGenerar = Menu(self.menuOperaciones, tearoff=0)
        self.menuHilos = Menu(self.menuOperaciones, tearoff=0)
        self.menuForks = Menu(self.menuOperaciones, tearoff=0)

        self.menuOperaciones.add_cascade(label="Generar Kakuro", menu=self.menuGenerar)
        self.menuOperaciones.add_command(label="Resolver Kakuro", command=lambda: kakuro.ResolverKakuro())

        self.menuGenerar.add_command(label="10x10", command=lambda:kakuro.CrearTablero(10, 67.5, self.TamanioLetra(10)))
        self.menuGenerar.add_command(label="11x11", command=lambda:kakuro.CrearTablero(11, 61.5, self.TamanioLetra(11)))
        self.menuGenerar.add_command(label="12x12", command=lambda:kakuro.CrearTablero(12, 56.5, self.TamanioLetra(12)))
        self.menuGenerar.add_command(label="13x13", command=lambda:kakuro.CrearTablero(13, 52,   self.TamanioLetra(13)))
        self.menuGenerar.add_command(label="14x14", command=lambda:kakuro.CrearTablero(14, 48.5, self.TamanioLetra(14)))
        self.menuGenerar.add_command(label="15x15", command=lambda:kakuro.CrearTablero(15, 45,   self.TamanioLetra(15)))
        self.menuGenerar.add_command(label="16x16", command=lambda:kakuro.CrearTablero(16, 42.3, self.TamanioLetra(16)))
        self.menuGenerar.add_command(label="17x17", command=lambda:kakuro.CrearTablero(17, 39.8, self.TamanioLetra(17)))
        self.menuGenerar.add_command(label="18x18", command=lambda:kakuro.CrearTablero(18, 37.5, self.TamanioLetra(18)))
        self.menuGenerar.add_command(label="19x19", command=lambda:kakuro.CrearTablero(19, 35.6, self.TamanioLetra(19)))
        self.menuGenerar.add_command(label="20x20", command=lambda:kakuro.CrearTablero(20, 33.8, self.TamanioLetra(20)))

        self.menuEjecucion = Menu(self.menusBarra, tearoff=0)
        self.menusBarra.add_cascade(label="  Ejecución  ", menu=self.menuEjecucion)  # Se añade a la barra del menú

        self.estadoHilos = BooleanVar()
        self.estadoHilos.set(False)
        self.menuEjecucion.add_checkbutton(label="Hilos", onvalue=1, offvalue=False, variable=self.estadoHilos, command=lambda:self.EjecucionHilos(self.estadoHilos.get()))

        self.estadoForks = BooleanVar()
        self.estadoForks.set(False)
        self.menuEjecucion.add_checkbutton(label="Forks", onvalue=1, offvalue=False, variable=self.estadoForks, command=lambda:self.EjecucionForks(self.estadoForks.get()))

        self.acercaDeMenu = Menu(self.menusBarra, tearoff=0)
        self.menusBarra.add_cascade(label=" Acerca de..  ", menu=self.acercaDeMenu)  # Se añade a la barra del menú
        self.acercaDeMenu.add_command(label="Información", command=lambda: messagebox.showinfo("Acerca de..",
                                                                                          "Instituto Tecnológico de Costa Rica \nIngeniería en Computación \nAnálisis de Algoritmos \n\nJosé Navarro Acuña \nJosúe Suárez Campos \n2017"))
        self.ventanaPrincipal.config(menu=self.menusBarra)

        # --------------------------------------------------------------------------------------------------------------------

    def DimensionCuadrado(self, tamanioTablero):
        return {
            # Tamaño tablero : dimension cuadrado
            10: 67.5,
            11: 61.5,
            12: 56.5,
            13: 52,
            14: 48.5,
            15: 45,
            16: 42.3,
            17: 39.8,
            18: 37.5,
            19: 35.6,
            20: 33.8
        }.get(tamanioTablero)

    def TamanioLetra(self, tamanioTablero):
        return {
            # Tamaño tablero : tamanio letra
            10: 19,
            11: 18,
            12: 17,
            13: 16,
            14: 14,
            15: 14,
            16: 13,
            17: 13,
            18: 13,
            19: 13,
            20: 12
        }.get(tamanioTablero)

    def PosicionCasillaLlaveHorizontal(self, tamanioTablero, coord, coordX):
        if(coordX):
            return {
                # Tamaño tablero : dimension cuadrado
                10: coord + 48,
                11: coord + 45,
                12: coord + 42,
                13: coord + 38,
                14: coord + 36,
                15: coord + 34,
                16: coord + 32,
                17: coord + 30,
                18: coord + 28,
                19: coord + 26,
                20: coord + 24
            }.get(tamanioTablero)
        else:
            return {
                # Tamaño tablero : dimension cuadrado
                10: coord + 15,
                11: coord + 16,
                12: coord + 16,
                13: coord + 16,
                14: coord + 14,
                15: coord + 12,
                16: coord + 10,
                17: coord + 8,
                18: coord + 8,
                19: coord + 7,
                20: coord + 7
            }.get(tamanioTablero)

    def PosicionCasillaLlaveVertical(self, tamanioTablero, coord, coordX):
        if(coordX):
            return {
                # Tamaño tablero : dimension cuadrado
                10: coord + 20,
                11: coord + 18,
                12: coord + 16,
                13: coord + 14,
                14: coord + 13,
                15: coord + 12,
                16: coord + 11,
                17: coord + 11,
                18: coord + 13,
                19: coord + 11,
                20: coord + 9
            }.get(tamanioTablero)
        else:
            return {
                # Tamaño tablero : dimension cuadrado
                10: coord + 50,
                11: coord + 46,
                12: coord + 42,
                13: coord + 38,
                14: coord + 36,
                15: coord + 34,
                16: coord + 32,
                17: coord + 30,
                18: coord + 28,
                19: coord + 26,
                20: coord + 24
            }.get(tamanioTablero)

    def PosicionCasillaBlanca(self, tamanioTablero, coord):
        return {
            # Tamaño tablero : dimension cuadrado
            10: coord + 34,
            11: coord + 30,
            12: coord + 27,
            13: coord + 27,
            14: coord + 25,
            15: coord + 23,
            16: coord + 22,
            17: coord + 20,
            18: coord + 19,
            19: coord + 18,
            20: coord + 17
        }.get(tamanioTablero)

    def EjecucionHilos(self, estado):
        print("Hilos Main -> " + str(estado))

        if estado == True:
            Generador.ActivarHilos(self, estado)
            SolucionadorK.ActivarHilos(estado)
        else:
            Generador.DesactivarHilos(self, estado)
            SolucionadorK.DesactivarHilos(estado)

    def EjecucionForks(self, estado):
        print("Forks Main -> " + str(estado))

        if estado == True:
            Generador.ActivarForks(self, estado)
            SolucionadorK.ActivarForks(estado)
        else:
            Generador.DesactivarForks(self, estado)
            SolucionadorK.DesactivarForks(estado)

class Kakuro(object):
    def __init__(self):
        self.pathBuscarKakuro = ""
        self.matrizHorizontal = []
        self.matrizVertical = []
        self.matriz = []
        self.listaCeldas = []

    def __repr__(self):
        return "Kakuro: Path: %d \n MatrizH: %d \n MatrizV: %d \n Matriz: %d \n Celdas: %d" \
               % (self.pathBuscarKakuro, self.matrizHorizontal, self.matrizVertical, self.matriz, self.listaCeldas)

    def setPathBuscarKakuro(self, path):
        self.pathBuscarKakuro = path
    def getPathBuscarKakuro(self):
        return self.pathBuscarKakuro

    def LimpiarMatrices(self):
        self.matrizHorizontal.clear()
        self.matrizVertical.clear()

    def CrearArchivoKakuroTemp(self, tamanioKakuro):
        nombreArchivo = "KakuroTemp.AA"
        archivoTmp = open(nombreArchivo, "w")

        contenido = self.ObtenerMatrices(tamanioKakuro, True)
        archivoTmp.write(contenido)

        kakuro.setPathBuscarKakuro(nombreArchivo)
        archivoTmp.close()

    def ObtenerMatrices(self, tamanioKakuro, kakuroGenerado): # self.matrizHorizontal + self.matrizVertical
        contenido = ""

        for vector in self.matrizHorizontal:
            contenido += ",".join(vector) + "\n"

        contenido += "\n" # Separador en el archivo entre cada matriz

        for vector in self.matrizVertical:
            contenido += ",".join(vector) + "\n"

        return contenido

    def CrearTablero(self, tamano, dimension, tamanioLetra):
        interfazUsuario.canvas.delete("all")
        tableroKakuro.setTamanio(tamano)
        tableroKakuro.setDimension(dimension) # Define el tamaño de cada cuadrado
        tableroKakuro.setTamanioLetra(tamanioLetra)

        kakuro.GenerarKakuro()

    def GenerarKakuro(self):

        tableroKakuro.deleteCasillas()
        SolucionadorK.Solucionador.matrizSolucion = []
        SolucionadorK.ReestablecerAtributosClases()

        tamanioKakuro = tableroKakuro.getTamanio()
        dimensionKakuro = tableroKakuro.getDimension()
        tamanioLetra = tableroKakuro.getTamanioLetra()

        generar = Generador(tamanioKakuro)
        generar.GenerarMatrizKakuro()
        generar.GenerarTipos()
        #generar.GenerarBloques()
        generar.meterEnMatrices()

        self.matrizHorizontal = generar.getMatrizHorizontal()
        self.matrizVertical = generar.getMatrizVertical()


        self.CrearArchivoKakuroTemp(tamanioKakuro)
        self.MostrarKakuro(False)

    def ResolverKakuro(self):
        try:
            SolucionadorK.Ejecutar(kakuro.getPathBuscarKakuro())

            self.MostrarKakuro(True)

        except FileNotFoundError:
            messagebox.showinfo("Error",
                                "Primero genere un kakuro o busque uno en su directorio local")
        except IndexError:
            messagebox.showinfo("Error",
                                "El kakuro no tiene solución")
        except RecursionError:
            self.ResolverKakuro()

    def AbrirKakuro(self):
        try:
            ftypes = [('.txt file', "*.txt")]
            ttl = "Buscar Kakuro..."
            dir1 = 'C:\\'
            direccionArchivo = askopenfilename(filetypes=ftypes, initialdir=dir1, title=ttl)

            if(direccionArchivo is ""): # En caso de cerrar la ventana y no abrir nada
                return

            tableroKakuro.deleteCasillas()
            SolucionadorK.ReestablecerAtributosClases()
            kakuro.setPathBuscarKakuro(direccionArchivo)

            with open(kakuro.getPathBuscarKakuro(), 'r') as f:

                self.matriz = [linea.strip().split(',') for linea in f] # Obtener una matriz completa del archivo (matriz horizontal + matriz vertical)

            tableroKakuro.setTamanio(len(list(self.matriz[0])))
            tableroKakuro.setDimension(interfazUsuario.DimensionCuadrado(tableroKakuro.getTamanio()))
            tableroKakuro.setTamanioLetra(interfazUsuario.TamanioLetra(tableroKakuro.getTamanio()))

            self.matrizHorizontal = self.ObtenerMatrizKakuro(self.matriz, tableroKakuro.getTamanio(), 0)
            self.matrizVertical = self.ObtenerMatrizKakuro(self.matriz, tableroKakuro.getTamanio(), tableroKakuro.getTamanio() + 1)

            self.MostrarKakuro(False)

        except FileNotFoundError:
            print ("El archivo no existe!")

    def MostrarKakuro(self, mostrarRespuesta):

        tamanioKakuro = tableroKakuro.getTamanio()
        dimensionKakuro = tableroKakuro.getDimension()
        tamanioLetra = tableroKakuro.getTamanioLetra()

        if(mostrarRespuesta != True):

            x = 0
            y = 0
            for i in range(tamanioKakuro + 1):
                y = i * dimensionKakuro
                for j in range(tamanioKakuro + 1):
                    x = j * dimensionKakuro

                    if(i != tamanioKakuro) & (j != tamanioKakuro): # Se usan i y j desde 0 hasta i-1 y j-1 el tamaño del tablero

                        elemento_H = self.matrizHorizontal[i][j]
                        elemento_V = self.matrizVertical[i][j]

                        casillaKakuro = None

                        if(elemento_H == "XX") & (elemento_V == "XX"):
                            colorCasilla = "gray"
                            interfazUsuario.canvas.create_rectangle(x, y, x + dimensionKakuro, y + dimensionKakuro,
                                                                    fill=colorCasilla)  # "gray"

                            casillaKakuro = Casilla.Casilla(TipoCelda.TipoCelda.NEGRO, x, y)
                            casillaKakuro.addContenido("XX", "XX")

                        if(elemento_H.isdigit()) | (elemento_V.isdigit()):
                            if(elemento_H == "00") & (elemento_V == "00"):
                                colorCasilla = "white"
                                # colorTexto = "red"
                                interfazUsuario.canvas.create_rectangle(x, y, x + dimensionKakuro, y + dimensionKakuro,
                                                                        fill=colorCasilla)  # "gray"

                                casillaKakuro = Casilla.Casilla(TipoCelda.TipoCelda.BLANCO,
                                                        interfazUsuario.PosicionCasillaBlanca(tamanioKakuro, x),
                                                        interfazUsuario.PosicionCasillaBlanca(tamanioKakuro, y))

                                casillaKakuro.addContenido("00", "00")

                            else:
                                colorCasilla = "gray"
                                colorTexto = "white"
                                interfazUsuario.canvas.create_rectangle(x, y, x + dimensionKakuro, y + dimensionKakuro,
                                                                        fill=colorCasilla)  # "gray"
                                interfazUsuario.canvas.create_line(x, y, x + dimensionKakuro, y + dimensionKakuro)

                                if(elemento_H == "XX"):
                                    interfazUsuario.canvas.create_text(interfazUsuario.PosicionCasillaLlaveVertical(tamanioKakuro, x, True),
                                                                       interfazUsuario.PosicionCasillaLlaveVertical(tamanioKakuro, y, False),
                                                                       fill=colorTexto,
                                                                       font="Times " + str(tamanioLetra) + " bold",
                                                                       text=elemento_V)
                                else:
                                    if(elemento_V == "XX"):
                                        interfazUsuario.canvas.create_text(interfazUsuario.PosicionCasillaLlaveHorizontal(tamanioKakuro, x, True),
                                                                       interfazUsuario.PosicionCasillaLlaveHorizontal(tamanioKakuro, y, False),
                                                                       fill=colorTexto,
                                                                       font="Times " + str(tamanioLetra) + " bold",
                                                                       text=elemento_H)
                                    else:
                                        # Agregue los dos
                                        interfazUsuario.canvas.create_text(
                                            interfazUsuario.PosicionCasillaLlaveVertical(tamanioKakuro, x, True),
                                            interfazUsuario.PosicionCasillaLlaveVertical(tamanioKakuro, y, False),
                                            fill=colorTexto,
                                            font="Times " + str(tamanioLetra) + " bold",
                                            text=elemento_V)
                                        interfazUsuario.canvas.create_text(
                                            interfazUsuario.PosicionCasillaLlaveHorizontal(tamanioKakuro, x, True),
                                            interfazUsuario.PosicionCasillaLlaveHorizontal(tamanioKakuro, y, False),
                                            fill=colorTexto,
                                            font="Times " + str(tamanioLetra) + " bold",
                                            text=elemento_H)

                                casillaKakuro = Casilla.Casilla(TipoCelda.TipoCelda.LLAVE_H_V, x, y)
                                casillaKakuro.addContenido(elemento_H, elemento_V)

                        tableroKakuro.addCasilla(casillaKakuro)

            SolucionadorK.Solucionador.matrizSolucion = []
            interfazUsuario.ventanaPrincipal.geometry('{}x{}'.format(int(x), int(y))) # ('{}x{}+{}+{}'.format(int(x), int(y), 340, 0))

        else: # Mostrar la respuesta del kakuro

            colorTexto = "red"
            casillasKakuro = tableroKakuro.getCasillas()

            matrizSolucion = SolucionadorK.Solucionador.matrizSolucion
            vectorSolucion = sum(matrizSolucion, [])

            for i in range(tamanioKakuro * tamanioKakuro):

                if(vectorSolucion[i] != "#") & (vectorSolucion[i] != "X"):

                    interfazUsuario.canvas.create_text(
                                                casillasKakuro[i].getPosicionX(),
                                                casillasKakuro[i].getPosicionY(),
                                                fill=colorTexto,
                                                font="Times " + str(tamanioLetra) + " bold",
                                                text=vectorSolucion[i])

            SolucionadorK.Solucionador.matrizSolucion = []

    def GuardarKakuro(self):

        ftypes = [('.txt file', "*.txt")]
        archivo = filedialog.asksaveasfile(mode='w', filetypes=ftypes, defaultextension=".txt")

        if archivo is None:  # En caso de cerrar la ventana y no hacer nada
            return

        tamanioKakuro = tableroKakuro.getTamanio()

        contenido = self.ObtenerMatrices(tamanioKakuro, False)

        archivo.write(contenido)
        archivo.close()

    def ObtenerMatrizKakuro(self, matrizBase, tamanioKakuro, indice):
        """
        Como matrizBase tiene la matriz horizontal y vertical juntas, se necesita
        indice para que a nivel del eje x se pueda llegar hasta la matriz vertical.
        Por eso, en la llamada para obtener la matriz vertical se suma el tamaño del
        kakuro (lo que abarca la matriz horizontal) más 1 (saltar el espacio en blanco -> \n).
        """
        matriz = []
        for i in range(tamanioKakuro):
            matriz.append([])

            for j in range(tamanioKakuro):
                matriz[i].append(matrizBase[i + indice][j])

        return matriz


tk = Tk()

interfazUsuario = InterfazUsuario(tk)

kakuro = Kakuro()
tableroKakuro = Tablero.Tablero()


#archivoTmp = Archivo()
#archivoTmp.CrearArchivoTemp()
#archivoTmp.EscribirEnArchivoTemp("Mensaje")
#print(archivoTmp.LeerArchivoTemp())
#archivoTmp.CerrarArchivoTemp()
#print(archivoTmp.ObtenerDirectorio())


tk.mainloop()