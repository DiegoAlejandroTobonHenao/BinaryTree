import pygame, sys
import random
import time
import itertools
from tkinter import *
from pygame.locals import *

from Logic.Tree import Tree

pygame.init()
pygame.font.init()


class Gui:
    def __init__(self, tree):
        sys.setrecursionlimit(10000)
        width = 1200
        heigth = 700
        window = pygame.display.set_mode((width, heigth))
        pygame.display.set_caption("Proyect")
        # I define images
        background = pygame.image.load("..\Images\Fondo.jpg")
        if tree == None:
            print("None tree")
        else:
            window.fill((250, 250, 250))
            # I paint the white Window background
            # The following counter is used to continue to know the position of the list
            # of nodes to which to draw
            steepCounter = 0
            # object with the data to position and assign the matrix values ​​on the screen
            matrixPositioning = MatrixPositioning(10, 10, 20, 0, 20)

            keyboardListOfRectangles = []
            images = cargarImagenesCasa()
            imagesRectanglesList = drawHomeImages(window, images, [650, 500], 60, 60)
            delete = False
            edit = False
            name = False
            editX = False
            editY = False

            string = ""
            xNumber = ""
            yNumber = ""
            selectedItem = ""
            pictureMoving = False
            selectedImages = []
            selectedImages.append([])  # In position 0 go the images
            selectedImages.append([])  # In position 1 the labels go
            treeList = []
            treeList.append(tree)
            permutations = list(itertools.permutations(tree.listWidth))
            for i in permutations:
                newTree = Tree()
                newTree.createTree("reformatingTree", list(i))
                treeList.append(newTree)
            treeList[0].createTree("reformatingTree", permutations[0])
            treeCounter = 0  # Serves to know which tree should be displayed
            pointsList = []  # Are the points where you click with the mouse
            colorList = []
            for i in range(0, len(treeList)):
                colorList.append(generateRandomC())
            occupied = False  # If you are editing or deleting, you cannot modify any plane or tree counter
            findOptimum = False
            while True:
                window.fill((250, 250, 250))  # Fill the Window with a color
                window.blit(background, (0, 0))

                matrix = createMatrix()

                # I think the lines of the matrix
                createRectsInMatrix(treeList[treeCounter].listWidth, matrix, steepCounter)
                # change the 0 for a number greater than 2 different in each section, and depending on that number is the color of the section
                treeList[treeCounter].rectangleList = returnRectanglesInMatrix(
                    matrix)  # For each current tree the matrix is ​​modified for this tree, so the matrix always changes

                drawMatrix(window, matrix, matrixPositioning.x, matrixPositioning.y,
                           matrixPositioning.objectsSize, matrixPositioning.radio,
                           matrixPositioning.distanceObjects, colorList)
                # List of permutations of the list in width
                height = treeList[treeCounter].height()
                drawTree(window, treeList[treeCounter].root, [820, 40], treeList[treeCounter], height,
                         # tree counter = number of the current tree
                         0)

                drawKeyboard(window, keyboardListOfRectangles, 1045, 10)
                rectangleColors = drawRectangleColors(window, len(treeList[treeCounter].nodeList) + 5,
                                                      20, colorList, [750, 570])
                drawHomeImages(window, images, [650, 500], 60, 60)

                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    else:
                        if event.type == KEYDOWN:
                            if event.key == K_LEFT:
                                if steepCounter > 0:
                                    steepCounter -= 1
                            elif event.key == K_RIGHT:
                                if steepCounter < len(treeList[treeCounter].nodeList):
                                    steepCounter += 1
                            elif event.key == K_UP and not occupied:
                                if treeCounter < len(treeList) - 1:
                                    treeCounter += 1
                                    selectedImages[1].clear()
                                    selectedImages[0].clear()
                                    pointsList.clear()
                                    treeList[treeCounter].createTree("reformatingTree",
                                                                     treeList[treeCounter].nodeList)
                            elif event.key == K_DOWN:
                                if treeCounter > 0 and not occupied:
                                    treeCounter -= 1
                                    selectedImages[1].clear()
                                    selectedImages[0].clear()
                                    pointsList.clear()
                                    treeList[treeCounter].createTree("reformatingTree",
                                                                     treeList[treeCounter].nodeList)
                            elif event.key == K_SPACE:
                                occupied = False
                                findOptimum = False
                                treeCounter = 0
                                selectedImages[1].clear()
                                selectedImages[0].clear()
                                pointsList.clear()
                                treeList[treeCounter].createTree("reformatingTree",
                                                                 treeList[treeCounter].nodeList)

                                crearRectangulosMatriz = True
                            elif event.key == K_DELETE:
                                # =================================================SHow the best===========================================
                                if treeCounter == 0:
                                    # Genero la lista de matrices
                                    occupied = True
                                    for i in range(0, len(treeList)):
                                        treeList[i].createTree("reformatingTree",
                                                               treeList[i].nodeList)
                                        emptyMatrix = createMatrix()
                                        newMatrix = createRectsInMatrix(treeList[i].nodeList, emptyMatrix,
                                                                        len(treeList[i].nodeList))
                                        treeList[i].rectangleList = returnRectanglesInMatrix(newMatrix)
                                        treeList[i].minorArea()
                                        matrix = newMatrix  # the matrix with the new changes happened to the current matrix
                                    # buscarOptimo
                                    minorMayorArea = 0
                                    treeNumber = 0
                                    # ==============We find the largest area of ​​the minor, the optimal
                                    for i in range(len(treeList)):
                                        if treeList[i].areaMinor >= minorMayorArea:
                                            minorMayorArea = treeList[i].areaMinor
                                            treeNumber = i
                                    treeCounter = treeNumber
                                    matrix = newMatrix
                                    selectedImages[1].clear()
                                    selectedImages[0].clear()
                                    pointsList.clear()
                                    findOptimum = True
                                    print(treeList[treeCounter].areaMinor)
                                    treeList[treeCounter].createTree("reformatingTree",
                                                                     treeList[treeCounter].nodeList)
                            if delete:
                                string = string + chr(event.key)
                            if edit:
                                if name:
                                    string = string + chr(event.key)
                                if editX:
                                    xNumber = xNumber + chr(event.key)
                                if editY:
                                    yNumber = yNumber + chr(event.key)
                        elif event.type == MOUSEBUTTONUP:
                            mouse = event.pos
                            rectanguloMouse = Rectangle(mouse[0], mouse[1], 1, 1)
                            for i in keyboardListOfRectangles:
                                if interceptRectangle(i, rectanguloMouse):
                                    selectedItem = ""
                                    pictureMoving = False
                                    if i.identifier == "del":
                                        print('Por favor escriba el nombre del nodo a eliminar')
                                        delete = True
                                    if i.identifier == "ok":
                                        if delete:
                                            delete = False
                                            print(string)
                                            treeList[treeCounter].delete(string)
                                            string = ""
                                        if edit:
                                            edit = True
                                            if string != "" and xNumber != "" and yNumber != "":
                                                print(string + " " + xNumber + " " + yNumber)
                                                treeList[treeCounter].modify(string, int(xNumber),
                                                                             int(yNumber))
                                                string = ""
                                                xNumber = ""
                                                yNumber = ""
                                                edit = False
                                            if string != "" and xNumber == "" and yNumber == "":
                                                name = False
                                            if string != "" and xNumber != "" and yNumber == "":
                                                name = False
                                                editX = False
                                            if string != "" and xNumber != "" and yNumber != "":
                                                name = False
                                                editX = False
                                                editY = False
                                    if i.identifier == "edit":
                                        edit = True
                                    if i.identifier == "name":
                                        name = True
                                    if i.identifier == "x":
                                        editX = True
                                    if i.identifier == "y":
                                        editY = True
                            if pictureMoving:
                                if mouse[0] < (matrixPositioning.x + len(
                                        matrix) * matrixPositioning.distanceObjects + matrixPositioning.objectsSize):
                                    if mouse[0] > matrixPositioning.x:
                                        if mouse[1] < (matrixPositioning.y + len(
                                                matrix) * matrixPositioning.distanceObjects + matrixPositioning.objectsSize):
                                            if mouse[1] > matrixPositioning.y:
                                                selectedImages[1].append(selectedItem)
                                                selectedImages[0].append(
                                                    returnImage(images, selectedItem))
                                                pointsList.append(mouse)
                                                pictureMoving = False
                                                selectedItem = ""
                            for i in imagesRectanglesList:
                                if interceptRectangle(i, rectanguloMouse):
                                    print(rectanguloMouse.area)
                                    selectedItem = i.identifier
                                    pictureMoving = True
                            for i in range(len(rectangleColors)):
                                if interceptRectangle(rectangleColors[i], rectanguloMouse):
                                    colorList[i + 1] = generateRandomC()
                drawImages(window, selectedImages[0], pointsList)
                pygame.display.update()
                time.sleep(0.01)


# Matrix list is the list of nodes for the matrix
def createRectsInMatrix(matrixList, matrix, steepCounter):
    limite = 0
    counter = 0
    width = len(matrix) - 1
    for i in matrixList:
        if counter >= steepCounter:
            break
        counter += 1
        # assuming the matrix is ​​square
        if i.axis == 'x':
            if i.x < len(matrix) and i.y < len(matrix):
                matrix[width - i.y][i.x] = 2  # The number two is to indicate that there is a node
                for x in range(i.x + 1, len(matrix)):
                    if matrix[width - i.y][x] != 0:
                        break
                    matrix[width - i.y][x] = 1
                for x in reversed(range(0, i.x)):
                    if matrix[width - i.y][x] != 0:
                        break
                    matrix[width - i.y][x] = 1
        # en el eje y
        elif i.x < len(matrix) and i.y < len(matrix):
            matrix[width - i.y][i.x] = 2
            if i.y == len(matrix):
                limite = len(matrix)
            else:
                limite = i.y + 1
            for y in range(limite, len(matrix)):
                if matrix[width - y][i.x] != 0:
                    break
                matrix[width - y][i.x] = 1
            for y in reversed(range(0, i.y)):
                if matrix[width - y][i.x] != 0:
                    break
                matrix[width - y][i.x] = 1
    return matrix


def returnImage(imageList, identifier):
    images = imageList[0]
    identifiers = imageList[1]
    for i in range(0, len(images)):
        if identifiers[i] == identifier:
            return images[i]
    print("no se encontró la imagen")


class Rectangle:
    def __init__(self, x, y, width, height, identifier=""):
        self.identifier = identifier
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.area = width * height


def imprimirValoresRecta(rect):
    print("x:", rect.x, "y:", rect.y, "x1:", rect.x1, "y1:",
          rect.y1, "eje:", rect.axis)


def createMatrix():
    numero_columnas = 31
    numero_filas = 31
    matriz = [[0] * numero_columnas for i in range(numero_filas)]
    return matriz


def printMatrix(matriz):
    for i in range(0, len(matriz)):
        print(matriz[i])


def drawMatrix(graphics, matrix, x, y, sizeObject, radius, distanceInObjects,
               colorList):
    xi = x
    yi = y
    for i in range(0, len(matrix)):
        for j in matrix[i]:
            pygame.draw.rect(graphics, colorList[j], (x, y, sizeObject, sizeObject))
            x += distanceInObjects
        x = xi
        y += distanceInObjects


def drawKeyboard(graphics, rectangleList, x, y):
    rectangleList.clear()
    numero = 0
    xi = x
    width = 50
    height = 50
    fuente = pygame.font.SysFont('Comic Sans MS', 15)

    pygame.draw.rect(graphics, (254, 254, 254), (x, y, width, height))
    text = fuente.render("Del", True, (200, 0, 0))
    graphics.blit(text, (x + 20, y + 13))
    rectangleList.append(Rectangle(x, y, width, height, "del"))

    pygame.draw.rect(graphics, (254, 254, 254), (x + width, y, width, height))
    text = fuente.render("Edit", True, (200, 0, 0))
    graphics.blit(text, (x + width + 20, y + 13))
    rectangleList.append(Rectangle(x + width, y, width, height, "edit"))

    pygame.draw.rect(graphics, (254, 254, 254), (x + width * 2, y, width, height))
    text = fuente.render("Ok", True, (200, 0, 0))
    graphics.blit(text, (x + width * 2 + 20, y + 13))
    rectangleList.append(Rectangle(x + width * 2, y, width, height, "ok"))

    pygame.draw.rect(graphics, (254, 254, 254), (x, y + height, width, height))
    text = fuente.render("Name", True, (200, 0, 0))
    graphics.blit(text, (x + 20, y + 13 + height))
    rectangleList.append(Rectangle(x, y + height, width, height, "name"))

    pygame.draw.rect(graphics, (254, 254, 254), (x + width, y + height, width, height))
    text = fuente.render("X", True, (200, 0, 0))
    graphics.blit(text, (x + width + 20, y + 13 + height))
    rectangleList.append(Rectangle(x + width, y + height, width, height, "x"))

    pygame.draw.rect(graphics, (254, 254, 254), (x + width * 2, y + height, width, height))
    text = fuente.render("Y", True, (200, 0, 0))
    graphics.blit(text, (x + width * 2 + 20, y + 13 + height))
    rectangleList.append(Rectangle(x + width * 2, y + height, width, height, "y"))

    text = fuente.render("PREV, ARROW <--------    NEXT, ARROW -------->", True, (200, 0, 0))
    graphics.blit(text, (90, 650))


def interceptRectangle(rectangle1, rectangle2):
    if rectangle2.x <= rectangle1.x + rectangle1.width:
        if rectangle2.x >= rectangle1.x:
            if rectangle2.y <= rectangle1.y + rectangle1.height:
                if rectangle2.y >= rectangle1.y:
                    return True
    return False


def generateRandomC():
    a = random.randint(0, 255)
    b = random.randint(0, 255)
    c = random.randint(0, 255)
    return (a, b, c)


def drawTree(graphics, root, rootPosition, tree, height, level):
    # variable to control the distance between nodes
    distance = 3
    # distance between the parent node and its children in terms of y
    dy = 70
    widthLine = 6
    if root != None and tree.root != None:
        # distance between the parent node and its children in terms of x
        dx = int(distance * (2 ** height - root.level))
        if root.left != None and root.right != None:
            # When he has two children
            drawCaseFirst(graphics, root, rootPosition, dx, dy, widthLine, tree, height,
                          level=level + 1)
        elif root.left == None and root.right != None:
            # when the node on the left is null and the right is not
            drawSecondCase(graphics, root, rootPosition, dx, dy, widthLine, tree, height,
                           level=level + 1)
        elif root.left != None and root.right == None:
            # When the left is null and the right is not
            drawThirdCase(graphics, root, rootPosition, dx, dy, widthLine, tree, height,
                          level=level + 1)
        elif root.left == None and root.right == None:
            # when you have no children, only the node and the node name are plotted
            drawFourthCase(graphics, root, rootPosition, level=level + 1)
    finalPoint = (rootPosition[0], rootPosition[1])
    return finalPoint


def drawCaseFirst(graphics, actualNode, rootPosition, dx, dy, widthLine, tree, height, level):
    # calculate the new positions
    leftPosition = (rootPosition[0] - dx, rootPosition[1] + dy)  # root position is the father's position
    rightPosition = (rootPosition[0] + dx, rootPosition[1] + dy)
    finalLeftPosition = drawTree(graphics, actualNode.left, leftPosition, tree, height,
                                 level=level + 1)
    pygame.draw.line(graphics, generateRandomC(), rootPosition,
                     (finalLeftPosition[0], finalLeftPosition[1]),
                     widthLine)
    pygame.draw.circle(graphics, generateRandomC(), rootPosition, 7, 1)
    finalRigthPosition = drawTree(graphics, actualNode.right, rightPosition, tree, height,
                                  level=level + 1)
    pygame.draw.line(graphics, generateRandomC(), rootPosition,
                     finalRigthPosition, widthLine)
    # I put the text of the node name
    drawInfoNode(graphics, actualNode, rootPosition)


def drawSecondCase(graphics, actualNode, rootPosition, dx, dy, whidtLine, tree, width, level):
    # I calculate the new positions
    newRigthPosition = (rootPosition[0] + dx, rootPosition[1] + dy)
    level = level + 1
    finalRigthPosition = drawTree(graphics, actualNode.right, newRigthPosition, tree, width,
                                  level=level + 1)
    pygame.draw.line(graphics, generateRandomC(), rootPosition,
                     finalRigthPosition, whidtLine)
    pygame.draw.circle(graphics, generateRandomC(), rootPosition, 7, 1)
    # I put the text of the node name
    drawInfoNode(graphics, actualNode, rootPosition)


def drawThirdCase(graphics, actualNode, rootPosition, dx, dy, widthLine, tree, height, level):
    # I calculate the new positions
    newLeftPosition = (rootPosition[0] - dx, rootPosition[1] + dy)
    finalLeftPosition = drawTree(graphics, actualNode.left, newLeftPosition, tree, height,
                                 level=level + 1)
    pygame.draw.line(graphics, generateRandomC(), rootPosition,
                     (finalLeftPosition[0], finalLeftPosition[1]), widthLine)
    pygame.draw.circle(graphics, generateRandomC(), rootPosition, 7, 1)
    # I put the text of the node name
    drawInfoNode(graphics, actualNode, rootPosition)


def drawFourthCase(graphics, actualNode, rootPosition, level):
    pygame.draw.circle(graphics, generateRandomC(), rootPosition, 7, 1)
    # I put the text of the node name
    drawInfoNode(graphics, actualNode, rootPosition)


def cargarImagenesCasa():
    # load the images of the house and return a list of lists, with images in index 0 and labels in index 1
    bathroom = pygame.image.load("..\Images\pequeñas\Baño.png")
    kitchen = pygame.image.load("..\Images\pequeñas\Cocina.png")
    dinningRoom = pygame.image.load("..\Images\pequeñas\Comedor.png")
    room = pygame.image.load("..\Images\pequeñas\Habitacion.png")
    office = pygame.image.load("..\Images\pequeñas\Oficina.png")
    hall = pygame.image.load("..\Images\pequeñas\Pasillo.png")
    room1 = pygame.image.load("..\Images\pequeñas\Sala.png")

    imagesList = [bathroom, kitchen, dinningRoom, room, office, hall, room1]
    tagList = ["bath", "kitchen", "dinningRoom", "room", "office", "hall", "room1"]
    list = [imagesList, tagList]
    return list


def drawInfoNode(graphics, node, rootPosition):
    x = str(node.x)
    y = str(node.y)
    dy = 10  # distance in and from the point of the node, is used to graph the information of the node (points)
    dx = 10  # distance in x from the point of the node, is used to graph the information of the node (points)
    font = pygame.font.SysFont('Comic Sans MS', 10, True)
    text = font.render(node.name, True, (250, 100, 0))
    text1 = font.render(x + ",", True, (200, 0, 0))  # the value x of the node is plotted
    text2 = font.render(y, True, (200, 0, 0))  # the value of the node is plotted
    graphics.blit(text, (rootPosition[0] + dx, rootPosition[1] - 15 + dy))
    graphics.blit(text1, (rootPosition[0] + dx, rootPosition[1] + dy))
    graphics.blit(text2, (rootPosition[0] + dx + 15, rootPosition[1] + dy))


def deleteRectFromList(identifier, list):
    for i in range(0, len(list)):
        if list[i].id == identifier:
            del list[i]
            return True


class MatrixPositioning:
    def __init__(self, x, y, sizeObjects, radio, distanceObjects):
        self.x = x
        self.y = y
        self.objectsSize = sizeObjects
        self.radio = radio
        self.distanceObjects = distanceObjects


def drawRectangleColors(graphics, rectangleNumbers, size, colorList, position=[0, 0]):
    xi = position[0]
    yi = position[1]
    x = xi
    y = yi
    rectangleList = []
    for i in range(1, rectangleNumbers):
        pygame.draw.rect(graphics, colorList[i], (x, y, size, size))
        recangulo = Rectangle(x, y, size, size, i)
        rectangleList.append(recangulo)
        x = x + size

    return rectangleList


# he paints the images of the house and returns his rectangles
def drawHomeImages(graphics, list, position, distance, sizeRectangle):
    x = position[0]
    y = position[1]
    pictures = list[0]
    tags = list[1]
    rectangleList = []
    for i in range(0, len(pictures)):
        graphics.blit(pictures[i], (x, y))  # Put the image on the screen
        rectangleList.append(Rectangle(x, y, sizeRectangle, sizeRectangle, tags[i]))
        x += distance
    return rectangleList


# paint an image from a list
def drawImages(graphics, imageList, positionList):
    for i in range(0, len(imageList)):
        if imageList[i] != None:
            graphics.blit(imageList[i], positionList[i])


def returnRectanglesInMatrix(matrix):
    # This method looks for the zeros and when finding them executes a method to put four, fives, etc.
    rectangleList = []
    counter = 3
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            if matrix[y][x] == 0:
                rectangle = fillMatrix(matrix, (x, y), counter)
                rectangleList.append(rectangle)
                counter += 1
    return rectangleList


def fillMatrix(matrix, index, counter):
    # Fill in a division with numbers equal to the counter
    xi = index[0]  # Where zero was found
    yi = index[1]  # Where zero was found
    yf = 0
    xf = 0
    # x = 0
    for y in range(yi, len(matrix)):
        for x in range(xi, len(matrix[y])):
            if matrix[y][x] == 0:
                matrix[y][x] = counter
            else:
                xf = x - 1
                break
            xf = x
        if y + 1 < len(matrix):
            if matrix[y + 1][x - 1] != 0:
                yf = y
                break

    # matrix [yi] [xi] = 49 # 49 is a color from a list of colors, I use it to paint the starting point
    # matrix [y] [xf] = 40 # the same but for the end point
    # I put a +1 in the width and height because the matrix starts from 0 and to find the area is counted from 1
    return Rectangle(xi, yi, (xf - xi) + 1, (y - yi) + 1, counter)
