import json
from Logica.Nodo import Nodo
##
# Lee un archivo y retorna una lista con cada uno de los nodos
##
class Lector:
    def __lector(self, listaEliminados):
        with open('../Archivos/arbol.json') as file:
            data = json.load(file)
            listaNodos = []
            #print('leyendo archivo...')
            for nodo in data['arbol']:
                if not self.existe(listaEliminados, nodo["nombre"]):
                    n = Nodo(nodo['nombre'], nodo["x"], nodo["y"])
                    listaNodos.append(n)
            #print('archivo leido.')
            return listaNodos
    def existe(self, lista, nombre):
        for i in lista:
            if i.nombre == nombre:
                return True
        return False
    def getListaDeNodos(self, listaEliminados):
        return self.__lector(listaEliminados)