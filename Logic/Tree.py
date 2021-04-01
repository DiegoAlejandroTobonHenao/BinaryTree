from Files.Files import Reader
import sys


class Tree:
    def __init__(self):
        self.root = None
        self.deletedNodes = []
        self.listWidth = []
        self.rectangleList = None
        self.reader = Reader()
        self.nodeList = []
        self.areaMinor = sys.maxsize
        self.createTree()
    # Creation of the method that gives me the height of the tree
    def __height(self, actualNode):
        if actualNode == None:
            return 0
        return max(1 + self.__height(actualNode.left), 1 + self.__height(actualNode.right), -1)

    def height(self):
        return self.__height(self.root)

    def add(self, node):
        # In the first scenario the current node is the root
        if self.root == None:
            node.left = None
            node.right = None
            node.axis = 'y'
            node.level = 0
            self.root = node
            return
        else:
            #the last one of the parameter is the node level
            node.left = None
            node.right = None
            self.__agregar(node, self.root, 1, 1)

    def __agregar(self, node, actualNode, level, nodeLevel):
        if actualNode != None:
            if level == 0:
                if node.y < actualNode.y:
                    if actualNode.left == None:
                        node.axis = "y"
                        node.level = nodeLevel
                        actualNode.left = node
                    else:
                        self.__agregar(node, actualNode.left, 1, level + 1)
                if node.y >= actualNode.y:
                    if actualNode.right == None:
                        node.axis = "y"
                        node.level = nodeLevel
                        actualNode.right = node
                    else:
                        self.__agregar(node, actualNode.right, 1, level + 1)
            else:
                if node.x < actualNode.x:
                    if actualNode.left == None:
                        node.axis = "x"
                        node.level = nodeLevel
                        actualNode.left = node
                    else:
                        self.__agregar(node, actualNode.left, 0, level + 1)
                if node.x >= actualNode.x:
                    if actualNode.right == None:
                        node.axis = "x"
                        node.level = nodeLevel
                        actualNode.right = node
                    else:
                        self.__agregar(node, actualNode.right, 0, level + 1)
    def delete(self, nodeName):
        for i in range(0, len(self.nodeList)):
            if self.nodeList[i].name == nodeName:
                #Remove the node from the list
                self.deletedNodes.append(self.nodeList[i])
                print(type(self.nodeList))
                del self.nodeList[i]
                self.createTree()
                return

    # Current node = root in the first iteration
    def exists(self, nodeName):
        for i in self.listWidth:
            if i.name == nodeName:
                return True

        return False

    def modify(self, nodeName, x, y):
        print(str(type(x)))
        print(type(str(type(y))))
        if self.exists(nodeName) and str(type(x)) == "<class 'int'>" and str(
                type(y)) == "<class 'int'>" and x < 100 and y < 100:
            self.__modify(nodeName, x, y)
        else:
            print(
                "It could not be modified, this may be because the node does not exist or the values ​​of x or y are invalid")

    def __modify(self, nombreNodo, x, y):
        self.createTree("", [nombreNodo, x, y])

    def createTree(self, action ="", updatedNode=[]):
        if action == "":
            if len(updatedNode) == 0:
                self.nodeList = self.reader.getNodeList(self.deletedNodes)
                if self.root != None:
                    self.root = None
                # self.listaAnchura = []
                for i in self.nodeList:
                    self.add(i)
                self.listWidth = self.width()
            else:
                self.nodeList = self.reader.getNodeList(self.deletedNodes)
                if self.root != None:
                    self.root = None
                # self.listaAnchura = []
                for i in self.nodeList:
                    if i.name == updatedNode[0]:
                        i.x = updatedNode[1]
                        i.y = updatedNode[2]
                    self.add(i)
                self.listWidth = self.width()
        elif action == "reformatingTree" and len(updatedNode) != 0:
            listaNodos = updatedNode
            if self.root != None:
                self.root = None
            # self.listaAnchura = []
            for i in listaNodos:
                self.add(i)
            self.nodeList = updatedNode
            self.listWidth = self.width()

    def __anchura(self, nodo):
        travel = []
        nodeList = []
        if nodo != None:
            tmp = nodo
            travel.append(tmp)
            while len(travel) > 0:
                tmp = travel.pop(0)

                if tmp.left != None:
                    travel.append(tmp.left)
                if tmp.right != None:
                    travel.append(tmp.right)
                nodeList.append(tmp)
            self.nodeList = nodeList
        return nodeList
    def width(self):
        return self.__anchura(self.root)

    def minorArea(self):
        areaMinor1 = 900000
        if self.rectangleList != None and len(self.rectangleList) > 0:
            for i in self.rectangleList:
                if i.area < areaMinor1:
                    areaMinor1 = i.area
        self.areaMinor = areaMinor1
        return areaMinor1