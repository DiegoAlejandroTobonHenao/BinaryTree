import json
from Logic.Node import Nodo
##
# Lee un archivo y retorna una lista con cada uno de los nodos
##
class Reader:
    def __lector(self, deletedNodes):
        with open('../Files/arbol.json') as file:
            data = json.load(file)
            nodeList = []
            for node in data['arbol']:
                if not self.exists(deletedNodes, node["name"]):
                    n = Nodo(node['name'], node["x"], node["y"])
                    nodeList.append(n)
            return nodeList
    def exists(self, list, name):
        for i in list:
            if i.name == name:
                return True
        return False
    def getNodeList(self, deletedNodes):
        return self.__lector(deletedNodes)