from Archivos.Archivos import Lector
import sys


class Arbol:
    def __init__(self):
        self.raiz = None
        self.eliminados = []
        self.listaAnchura = []
        self.listaRectangulos = None
        self.lector = Lector()
        self.listaNodos = []
        self.menorArea = sys.maxsize
        self.crearArbol()

    ##Cambios en el orden de comparar en la condicion de salida del metodo __nivel, se invirtió el orden para comparar
    def __nivel(self, nombre, nodoActual):
        if nodoActual == None or nodoActual.nombre == nombre:
            return 0
        return max(1 + self.__nivel(nombre, nodoActual.izq), 1 + self.__nivel(nombre, nodoActual.der), -100)

    def nivel(self, nombre):
        return self.__nivel(nombre, self.raiz)

    # Creacion del metodo que me da la altura del arbol
    def __altura(self, nodoActual):
        if nodoActual == None:
            return 0
        return max(1 + self.__altura(nodoActual.izq), 1 + self.__altura(nodoActual.der), -1)

    def altura(self):
        return self.__altura(self.raiz)

    def agregar(self, nodo):
        # En el primer escenario el nodo actual es la raiz
        if self.raiz == None:
            nodo.izq = None
            nodo.der = None
            nodo.eje = 'y'
            nodo.nivel = 0
            self.raiz = nodo
            return
        else:
            #el ultimo uno del parametro es el nivel del nodo
            nodo.izq = None
            nodo.der = None
            self.__agregar(nodo, self.raiz, 1, 1)

    def __agregar(self, nodo, nodoActual, nivel, nivelNodo):
        if nodoActual != None:
            if nivel == 0:
                if nodo.y < nodoActual.y:
                    if nodoActual.izq == None:
                        nodo.eje = "y"
                        nodo.nivel = nivelNodo
                        nodoActual.izq = nodo
                    else:
                        self.__agregar(nodo, nodoActual.izq, 1, nivel+1)
                if nodo.y >= nodoActual.y:
                    if nodoActual.der == None:
                        nodo.eje = "y"
                        nodo.nivel = nivelNodo
                        nodoActual.der = nodo
                    else:
                        self.__agregar(nodo, nodoActual.der, 1, nivel+1)
            else:
                if nodo.x < nodoActual.x:
                    if nodoActual.izq == None:
                        nodo.eje = "x"
                        nodo.nivel = nivelNodo
                        nodoActual.izq = nodo
                    else:
                        self.__agregar(nodo, nodoActual.izq, 0, nivel+1)
                if nodo.x >= nodoActual.x:
                    if nodoActual.der == None:
                        nodo.eje = "x"
                        nodo.nivel = nivelNodo
                        nodoActual.der = nodo
                    else:
                        self.__agregar(nodo, nodoActual.der, 0, nivel+1)
    def eliminar(self, nombreNodo):
        for i in range(0, len(self.listaNodos)):
            if self.listaNodos[i].nombre == nombreNodo:
                # Elimina el nodo de la lista
                self.eliminados.append(self.listaNodos[i])
                print(type(self.listaNodos))
                del self.listaNodos[i]
                self.crearArbol()
                return



    # Nodo actual = raiz en la primera iteracion
    def existe(self, nombreNodo):
        for i in self.listaAnchura:
            if i.nombre == nombreNodo:
                return True

        return False

    def modificar(self, nombreNodo, x, y):
        print(str(type(x)))
        print(type(str(type(y))))
        if self.existe(nombreNodo) and str(type(x)) == "<class 'int'>" and str(
                type(y)) == "<class 'int'>" and x < 100 and y < 100:
            self.__modificar(nombreNodo, x, y)
        else:
            print(
                "No se ha podido modificar, esto puede ser porque el nodo no existe o los valores de x o y son invalidos")

    def __modificar(self, nombreNodo, x, y):
        self.crearArbol("", [nombreNodo, x, y])

    def crearArbol(self, accion = "", nodoActualizado=[]):
        if accion == "":
            if len(nodoActualizado) == 0:
                self.listaNodos = self.lector.getListaDeNodos(self.eliminados)
                if self.raiz != None:
                    self.raiz = None
                # self.listaAnchura = []
                for i in self.listaNodos:
                    self.agregar(i)
                self.listaAnchura = self.anchura()
            else:
                self.listaNodos = self.lector.getListaDeNodos(self.eliminados)
                if self.raiz != None:
                    self.raiz = None
                # self.listaAnchura = []
                for i in self.listaNodos:
                    if i.nombre == nodoActualizado[0]:
                        i.x = nodoActualizado[1]
                        i.y = nodoActualizado[2]
                    self.agregar(i)
                self.listaAnchura = self.anchura()
        elif accion == "reordenarArbol" and len(nodoActualizado) != 0:
            listaNodos = nodoActualizado
            if self.raiz != None:
                self.raiz = None
            # self.listaAnchura = []
            for i in listaNodos:
                self.agregar(i)
            self.listaNodos = nodoActualizado
            self.listaAnchura = self.anchura()

    def __anchura(self, nodo):
        recorrido = []
        listaN = []
        if nodo != None:
            tmp = nodo
            recorrido.append(tmp)
            while len(recorrido) > 0:
                tmp = recorrido.pop(0)

                if tmp.izq != None:
                    recorrido.append(tmp.izq)
                if tmp.der != None:
                    recorrido.append(tmp.der)
                # print(tmp.nombre, "as")
                listaN.append(tmp)
            self.listaNodos = listaN
        return listaN
    def anchura(self):
        return self.__anchura(self.raiz)

    def areaMenor(self):
        areaMenor = 900000
        if self.listaRectangulos != None and len(self.listaRectangulos) > 0:
            for i in self.listaRectangulos:
                if i.area < areaMenor:
                    areaMenor = i.area
        self.menorArea = areaMenor
        return areaMenor

    def devolverNumeroAreaMatriz(self, matriz, puntoMouse, posicionMatriz, tamanoRectangulosMatriz, distanciaEntreRectangulos):
        x = puntoMouse[0]
        y = puntoMouse[1]
        #posicionX = x+
