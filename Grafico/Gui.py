import pygame, sys
import random
import time
import itertools
from tkinter import *
from pygame.locals import *

from Logica.Arbol import Arbol

pygame.init()
pygame.font.init()


class Gui:
    def __init__(self, arbol):
        sys.setrecursionlimit(10000)
        ancho = 1200
        alto = 700
        anchoDeNodos = 12
        altoDeNodos = 12
        ventana = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("Proyecto Estructuras")
        fuente = pygame.font.SysFont('Comic Sans MS', 15)
        # Defino imagenes--------------------------------------------------------
        fondo = pygame.image.load("..\Imagenes\Fondo.jpg")

        # imprimirMatriz(matriz)

        # listaRectas = crearRectas(arbol.listaAnchura)
        # Lista de rectangulos de los nodos, se usa para verificar sobre qué nodo se dió click

        listaRectangulosNodos = []
        """for i in listaRectas:
            imprimirValoresRecta(i)"""
        if arbol == None:
            print("Arbol vacío, no se puede dibujar")
        else:
            ventana.fill((250, 250, 250))
            # El siguiente contador sirve para seguir saber la posicion de la lista
            # de nodos hasta la que se debe dibujar
            contadorDePasos = 0
            # objeto con los datos para posicionar y asignar los valores de la matriz en pantalla
            posicionamientoMatrizz = posicionamientoMatriz(10, 10, 20, 0, 20)

            listaRectangulosTeclado = []
            imagenes = cargarImagenesCasa()
            listaRectangulosImagenes = pintarImagenesCasa(ventana, imagenes, [650, 500], 60, 60)
            elim = False
            edit = False
            name = False
            editX = False
            editY = False

            cadena = ""
            numeroX = ""
            numeroY = ""
            elementoSeleccionado = ""
            puntoFinalImagenSeleccionada = []
            moviendoImagen = False
            imagenesSeleccionadas = []
            imagenesSeleccionadas.append([])
            imagenesSeleccionadas.append([])
            listaArboles = []
            listaArboles.append(arbol)
            permutaciones = list(itertools.permutations(arbol.listaAnchura))
            permutaciones[0] = arbol.listaAnchura
            for i in permutaciones:
                nuevoArbol = Arbol()
                nuevoArbol.crearArbol("reordenarArbol", list(i))
                listaArboles.append(nuevoArbol)
            listaArboles[0].crearArbol("reordenarArbol", permutaciones[0])
            contadorArbol = 0
            listaPuntos = []
            listaColores = []
            for i in range(0, len(arbol.listaNodos)+5):
                listaColores.append(generarColorAlAzar())
            listaColoresRectangulos = []
            crearRectangulosMatriz = False
            ocupado = False
            numeroDeArbol = 0
            encontroOptimo = False
            while True:
                ventana.fill((250, 250, 250))
                ventana.blit(fondo, (0, 0))
                listaRectangulosNodos.clear()

                matriz = crearMatriz()

                # dibujo el plano
                crearRectasEnMatriz(listaArboles[contadorArbol].listaAnchura, matriz, contadorDePasos)
                # cambia los 0 por un numero mayor a 2 diferente en cada seccion, y dependiendo de ese numero es el color de la seccion
                # crearRectangulosMatriz = False
                listaArboles[contadorArbol].listaRectangulos = devolverRectangulosMatriz(matriz)

                pintarMatriz(ventana, matriz, posicionamientoMatrizz.x, posicionamientoMatrizz.y,
                             posicionamientoMatrizz.tamanoObjetos, posicionamientoMatrizz.radio,
                             posicionamientoMatrizz.distanciaEntreObjetos, listaColores)
                # Lista de permutaciones de la lista en anchura
                # dibujo el arbol
                altura = listaArboles[contadorArbol].altura()

                # if not encontroOptimo:
                dibujarArbol(ventana, listaArboles[contadorArbol].raiz, [820, 40], listaArboles[contadorArbol], altura,
                             0)

                pintarTeclado(ventana, listaRectangulosTeclado, 1045, 10)
                rectangulosColores = pintarRectangulosColores(ventana, len(listaArboles[contadorArbol].listaNodos)+5, 20, listaColores, [750,570])
                pintarImagenesCasa(ventana, imagenes, [650, 500], 60, 60)


                for evento in pygame.event.get():
                    if evento.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    else:
                        if evento.type == KEYDOWN:
                            if evento.key == K_LEFT:
                                if contadorDePasos > 0:
                                    contadorDePasos -= 1
                            elif evento.key == K_RIGHT:
                                if contadorDePasos < len(listaArboles[contadorArbol].listaNodos):
                                    contadorDePasos += 1
                            elif evento.key == K_UP and not ocupado:
                                if contadorArbol < len(listaArboles) - 1:
                                    contadorArbol += 1
                                    imagenesSeleccionadas[1].clear()
                                    imagenesSeleccionadas[0].clear()
                                    listaPuntos.clear()
                                    listaArboles[contadorArbol].crearArbol("reordenarArbol",
                                                                            listaArboles[contadorArbol].listaNodos)
                            elif evento.key == K_DOWN:
                                if contadorArbol > 0 and not ocupado:
                                    contadorArbol -= 1
                                    imagenesSeleccionadas[1].clear()
                                    imagenesSeleccionadas[0].clear()
                                    listaPuntos.clear()
                                    listaArboles[contadorArbol].crearArbol("reordenarArbol",
                                                                            listaArboles[contadorArbol].listaNodos)
                            elif evento.key == K_SPACE:
                                ocupado = False
                                encontroOptimo = False
                                contadorArbol = 0
                                imagenesSeleccionadas[1].clear()
                                imagenesSeleccionadas[0].clear()
                                listaPuntos.clear()
                                listaArboles[contadorArbol].crearArbol("reordenarArbol",
                                                                       listaArboles[contadorArbol].listaNodos)


                                crearRectangulosMatriz = True
                            elif evento.key == K_DELETE:
                                if contadorArbol == 0:
                                    # Genero la lista de matrices
                                    ocupado = True
                                    for i in range(0, len(listaArboles)):
                                        listaArboles[i].crearArbol("reordenarArbol",
                                                                                listaArboles[i].listaNodos)
                                        matrizVacia = crearMatriz()
                                        matrizNueva = crearRectasEnMatriz(listaArboles[i].listaNodos, matrizVacia,
                                                                          len(listaArboles[i].listaNodos))
                                        # listaMatrices.append(matrizNueva)
                                        listaArboles[i].listaRectangulos = devolverRectangulosMatriz(matrizNueva)
                                        listaArboles[i].areaMenor()
                                        matriz = matrizNueva

                                    # buscarOptimo
                                    areaMayorMenor = 0
                                    numeroDeArbol = 0
                                    for i in range(len(listaArboles)):
                                        if listaArboles[i].menorArea >= areaMayorMenor:
                                            areaMayorMenor = listaArboles[i].menorArea
                                            numeroDeArbol = i
                                    contadorArbol = numeroDeArbol
                                    # print(listaArboles[contadorArbol].menorArea)
                                    # print(listaArboles[contadorArbol].menorArea)
                                    print("Numero de arbol y area:", contadorArbol, areaMayorMenor)
                                    matriz = matrizNueva
                                    imagenesSeleccionadas[1].clear()
                                    imagenesSeleccionadas[0].clear()
                                    listaPuntos.clear()
                                    encontroOptimo = True
                                    print(listaArboles[contadorArbol].menorArea)
                                    listaArboles[contadorArbol].crearArbol("reordenarArbol",
                                                                           listaArboles[contadorArbol].listaNodos)
                            if elim:
                                cadena = cadena + chr(evento.key)
                            if edit:
                                if name:
                                    cadena = cadena + chr(evento.key)
                                    print("nombre: " + cadena)
                                if editX:
                                    numeroX = numeroX + chr(evento.key)
                                    print("numero x: " + numeroX)
                                if editY:
                                    numeroY = numeroY + chr(evento.key)
                                    print("numero y: " + numeroY)
                        elif evento.type == MOUSEBUTTONUP:
                            mouse = evento.pos
                            rectanguloMouse = Rectangulo(mouse[0], mouse[1], 1, 1)
                            for i in listaRectangulosTeclado:
                                if interceptaRectangulo(i, rectanguloMouse):
                                    elementoSeleccionado = ""
                                    moviendoImagen = False
                                    # print(i.identificador)
                                    if i.identificador == "del":
                                        print('Por favor escriba el nombre del nodo a eliminar')
                                        elim = True
                                    if i.identificador == "ok":
                                        if elim:
                                            elim = False
                                            print(cadena)
                                            listaArboles[contadorArbol].eliminar(cadena)
                                            cadena = ""
                                        if edit:
                                            edit = True
                                            if cadena != "" and numeroX != "" and numeroY != "":
                                                print(cadena + " " + numeroX + " " + numeroY)
                                                listaArboles[contadorArbol].modificar(cadena, int(numeroX),
                                                                                      int(numeroY))
                                                cadena = ""
                                                numeroX = ""
                                                numeroY = ""
                                                edit = False
                                            if cadena != "" and numeroX == "" and numeroY == "":
                                                name = False
                                            if cadena != "" and numeroX != "" and numeroY == "":
                                                name = False
                                                editX = False
                                            if cadena != "" and numeroX != "" and numeroY != "":
                                                name = False
                                                editX = False
                                                editY = False

                                    if i.identificador == "edit":
                                        edit = True
                                    if i.identificador == "name":
                                        name = True
                                    if i.identificador == "x":
                                        editX = True
                                    if i.identificador == "y":
                                        editY = True
                            if moviendoImagen:
                                # pintarImagen(ventana, imagenes, rectanguloMouse, elementoSeleccionado)
                                if mouse[0] < (posicionamientoMatrizz.x + len(
                                        matriz) * posicionamientoMatrizz.distanciaEntreObjetos + posicionamientoMatrizz.tamanoObjetos):
                                    if mouse[0] > posicionamientoMatrizz.x:
                                        if mouse[1] < (posicionamientoMatrizz.y + len(
                                                matriz) * posicionamientoMatrizz.distanciaEntreObjetos + posicionamientoMatrizz.tamanoObjetos):
                                            if mouse[1] > posicionamientoMatrizz.y:
                                                imagenesSeleccionadas[1].append(elementoSeleccionado)
                                                imagenesSeleccionadas[0].append(
                                                    retornarImagen(imagenes, elementoSeleccionado))
                                                listaPuntos.append(mouse)
                                                moviendoImagen = False
                                                elementoSeleccionado = ""
                            for i in listaRectangulosImagenes:
                                if interceptaRectangulo(i, rectanguloMouse):
                                    print(rectanguloMouse.area)
                                    elementoSeleccionado = i.identificador
                                    moviendoImagen = True
                                    # print(i.identificador)
                            for i in range(len(rectangulosColores)):
                                if interceptaRectangulo(rectangulosColores[i], rectanguloMouse):
                                    listaColores[i+1] = generarColorAlAzar()

                pintarImagenes(ventana, imagenesSeleccionadas[0], listaPuntos)
                # -------------------------------------------
                # ingreso las imagenes a la pantalla
                # ventana.blit(controles, (ancho - 200, 0))
                # ventana.blit(eliminar, (r_eliminar.x, r_eliminar.y))
                # -------------------------------------------
                pygame.display.update()
                time.sleep(0.01)


def retornarImagen(listaImagenes, identificador):
    imagenes = listaImagenes[0]
    print("identificador buscado: " + identificador + "de la siguiente lista")
    identificadores = listaImagenes[1]
    for i in range(0, len(imagenes)):
        if identificadores[i] == identificador:
            return imagenes[i]
    print("no se encontró la imagen")


class puntosParaRecta:
    def __init__(self, x, y, x1, y1, eje, identificador=""):
        self.x = x
        self.y = y
        self.x1 = x1
        self.y1 = y1
        self.eje = eje
        self.id = identificador


class Rectangulo:
    def __init__(self, x, y, ancho, alto, identificador=""):
        self.identificador = identificador
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.area = ancho * alto


def imprimirValoresRecta(recta):
    print("x:", recta.x, "y:", recta.y, "x1:", recta.x1, "y1:",
          recta.y1, "eje:", recta.eje)


def crearRectasEnMatriz(listaMatriz, matriz, contadorDePasos):
    limite = 0
    contador = 0
    width = len(matriz) - 1
    for i in listaMatriz:
        if contador >= contadorDePasos:
            break
        contador += 1
        # suponiendo que la matriz es cuadrada
        if i.eje == 'x':
            if i.x < len(matriz) and i.y < len(matriz):
                matriz[width - i.y][i.x] = 2
                """if i.x == len(matriz):
                    limite = len(matriz)
                else:
                    limite = i.x + 1"""
                for x in range(i.x + 1, len(matriz)):
                    if matriz[width - i.y][x] != 0:
                        break
                    matriz[width - i.y][x] = 1
                for x in reversed(range(0, i.x)):
                    if matriz[width - i.y][x] != 0:
                        break
                    matriz[width - i.y][x] = 1
        # en el eje y
        elif i.x < len(matriz) and i.y < len(matriz):
            matriz[width - i.y][i.x] = 2
            if i.y == len(matriz):
                limite = len(matriz)
            else:
                limite = i.y + 1
            for y in range(limite, len(matriz)):
                if matriz[width - y][i.x] != 0:
                    break
                matriz[width - y][i.x] = 1
            for y in reversed(range(0, i.y)):
                if matriz[width - y][i.x] != 0:
                    break
                matriz[width - y][i.x] = 1
    return matriz


def crearMatriz():
    numero_columnas =31
    numero_filas = 31
    matriz = [[0] * numero_columnas for i in range(numero_filas)]
    return matriz


def imprimirMatriz(matriz):
    for i in range(0, len(matriz)):
        print(matriz[i])


def pintarMatriz(componenteDeVisualizacion, matriz, x, y, tamanoCirculo, radioCirculo, distanciaEntreCirculos,
                 listaColores):
    xi = x
    yi = y
    for i in range(0, len(matriz)):
        for j in matriz[i]:
            if j == 1:
                # pygame.draw.circle(componenteDeVisualizacion, (94, 207, 209), (x, y), tamanoCirculo, radioCirculo)
                pygame.draw.rect(componenteDeVisualizacion, listaColores[j], (x, y, tamanoCirculo, tamanoCirculo))
            elif j == 2:
                pygame.draw.rect(componenteDeVisualizacion, listaColores[j], (x, y, tamanoCirculo, tamanoCirculo))
                # pygame.draw.circle(componenteDeVisualizacion, (227, 45, 82), (x, y), tamanoCirculo, radioCirculo)
            else:
                # print(j)
                pygame.draw.rect(componenteDeVisualizacion, listaColores[j], (x, y, tamanoCirculo, tamanoCirculo))
                # pygame.draw.circle(componenteDeVisualizacion, (242, 187, 198), (x, y), tamanoCirculo, radioCirculo)
            x += distanciaEntreCirculos

        x = xi
        y += distanciaEntreCirculos


def pintarTeclado(componenteDeVisualizacion, listaRectangulos, x, y):
    listaRectangulos.clear()
    numero = 0
    xi = x
    ancho = 50
    alto = 50
    fuente = pygame.font.SysFont('Comic Sans MS', 15)

    """for i in range(0, 4):
        for j in range(0, 3):
            pygame.draw.rect(componenteDeVisualizacion, (254, 254, 254), (x, y, ancho, alto))
            texto = fuente.render(str(numero), True, (200, 0, 0))
            if numero <= 9:
                componenteDeVisualizacion.blit(texto, (x + 20, y + 13))
                listaRectangulos.append(Rectangulo(x, y, ancho, alto, numero))
            numero += 1
            x += ancho
        x = xi
        y += alto"""
    pygame.draw.rect(componenteDeVisualizacion, (254, 254, 254), (x, y, ancho, alto))
    texto = fuente.render("Del", True, (200, 0, 0))
    componenteDeVisualizacion.blit(texto, (x + 20, y + 13))
    listaRectangulos.append(Rectangulo(x, y, ancho, alto, "del"))

    pygame.draw.rect(componenteDeVisualizacion, (254, 254, 254), (x + ancho, y, ancho, alto))
    texto = fuente.render("Edit", True, (200, 0, 0))
    componenteDeVisualizacion.blit(texto, (x + ancho + 20, y + 13))
    listaRectangulos.append(Rectangulo(x + ancho, y, ancho, alto, "edit"))

    pygame.draw.rect(componenteDeVisualizacion, (254, 254, 254), (x + ancho * 2, y, ancho, alto))
    texto = fuente.render("Ok", True, (200, 0, 0))
    componenteDeVisualizacion.blit(texto, (x + ancho * 2 + 20, y + 13))
    listaRectangulos.append(Rectangulo(x + ancho * 2, y, ancho, alto, "ok"))

    pygame.draw.rect(componenteDeVisualizacion, (254, 254, 254), (x, y + alto, ancho, alto))
    texto = fuente.render("Name", True, (200, 0, 0))
    componenteDeVisualizacion.blit(texto, (x + 20, y + 13 + alto))
    listaRectangulos.append(Rectangulo(x, y + alto, ancho, alto, "name"))

    pygame.draw.rect(componenteDeVisualizacion, (254, 254, 254), (x + ancho, y + alto, ancho, alto))
    texto = fuente.render("X", True, (200, 0, 0))
    componenteDeVisualizacion.blit(texto, (x + ancho + 20, y + 13 + alto))
    listaRectangulos.append(Rectangulo(x + ancho, y + alto, ancho, alto, "x"))

    pygame.draw.rect(componenteDeVisualizacion, (254, 254, 254), (x + ancho * 2, y + alto, ancho, alto))
    texto = fuente.render("Y", True, (200, 0, 0))
    componenteDeVisualizacion.blit(texto, (x + ancho * 2 + 20, y + 13 + alto))
    listaRectangulos.append(Rectangulo(x + ancho * 2, y + alto, ancho, alto, "y"))

    # pygame.draw.rect(componenteDeVisualizacion, (254, 254, 254), (20, 600, 100, alto))
    texto = fuente.render("PREV, ARROW <--------    NEXT, ARROW -------->", True, (200, 0, 0))
    componenteDeVisualizacion.blit(texto, (90, 650))


def interceptaRectangulo(rectangulo1, rectangulo2):
    if rectangulo2.x <= rectangulo1.x + rectangulo1.ancho:
        if rectangulo2.x >= rectangulo1.x:
            if rectangulo2.y <= rectangulo1.y + rectangulo1.alto:
                if rectangulo2.y >= rectangulo1.y:
                    return True
    return False


def generarColorAlAzar():
    a = random.randint(0, 255)
    b = random.randint(0, 255)
    c = random.randint(0, 255)
    return (a, b, c)


def dibujarArbol(componenteDeVisualizacion, nodoActual, posicionRaiz, arbol, altura, nivel):
    # variable para controlar la distancia entre nodos
    distancia = 3
    # distancia entre el nodo padre y sus hijos en terminos de y
    dy = 70

    # si hay 3 niveles, la distancia entre cada nodo debe ser de n*2*2.
    # la distancia entre cada nodo aumenta dependiendo del tamaño del arbol, por ejemplo si hay 3 niveles,
    # la distancia debe ser x*2 n, siendo x un valor pequeño y n el nivel, la distancia se cuenta desde el nivel de la
    # hoja mas lejana, pero para obtener la distancia de los nodos del padre se le resta la altura al nivel del nodo actual

    anchoDeLinea = 6
    if nodoActual != None and arbol.raiz != None:
        # distancia entre el nodo padre y sus hijos en terminos de x
        dx = int(distancia * (2 ** altura - nodoActual.nivel))
        # dx = int(distancia * (2 ** altura - nivel))
        if nodoActual.izq != None and nodoActual.der != None:
            # Cuando tiene dos hijos
            dibujarCaso1(componenteDeVisualizacion, nodoActual, posicionRaiz, dx, dy, anchoDeLinea, arbol, altura,
                         nivel=nivel + 1)
        elif nodoActual.izq == None and nodoActual.der != None:
            # cuando el nodo de la izquierda es nulo y el derecho no lo es
            dibujarCaso2(componenteDeVisualizacion, nodoActual, posicionRaiz, dx, dy, anchoDeLinea, arbol, altura,
                         nivel=nivel + 1)
        elif nodoActual.izq != None and nodoActual.der == None:
            # Cuando el izquierdo es nulo y el derecho no lo es
            dibujarCaso3(componenteDeVisualizacion, nodoActual, posicionRaiz, dx, dy, anchoDeLinea, arbol, altura,
                         nivel=nivel + 1)
        elif nodoActual.izq == None and nodoActual.der == None:
            # cuando no tiene hijos, solo se grafica el nodo y el nombre del nodo
            dibujarCaso4(componenteDeVisualizacion, nodoActual, posicionRaiz, nivel=nivel + 1)

    pFinal = (posicionRaiz[0], posicionRaiz[1])
    return pFinal


def dibujarCaso1(componenteDeVisualizacion, nodoActual, posicionRaiz, dx, dy, anchoDeLinea, arbol, altura, nivel):
    # calculo las nuevas posiciones
    nuevaPosicionIzq = (posicionRaiz[0] - dx, posicionRaiz[1] + dy)
    nuevaPosicionDer = (posicionRaiz[0] + dx, posicionRaiz[1] + dy)

    posicionFinalIzq = dibujarArbol(componenteDeVisualizacion, nodoActual.izq, nuevaPosicionIzq, arbol, altura,
                                    nivel=nivel + 1)

    pygame.draw.line(componenteDeVisualizacion, generarColorAlAzar(), posicionRaiz,
                     (posicionFinalIzq[0], posicionFinalIzq[1]), anchoDeLinea)
    pygame.draw.circle(componenteDeVisualizacion, generarColorAlAzar(), posicionRaiz, 7, 1)

    posicionFinalDer = dibujarArbol(componenteDeVisualizacion, nodoActual.der, nuevaPosicionDer, arbol, altura,
                                    nivel=nivel + 1)
    pygame.draw.line(componenteDeVisualizacion, generarColorAlAzar(), posicionRaiz,
                     posicionFinalDer, anchoDeLinea)
    # Pongo el texto del nombre del nodo
    dibujarInfoNodo(componenteDeVisualizacion, nodoActual, posicionRaiz)


def dibujarCaso2(componenteDeVisualizacion, nodoActual, posicionRaiz, dx, dy, anchoDeLinea, arbol, altura, nivel):
    # calculo las nuevas posiciones
    nuevaPosicionDer = (posicionRaiz[0] + dx, posicionRaiz[1] + dy)
    nivel = nivel + 1
    posicionFinalDer = dibujarArbol(componenteDeVisualizacion, nodoActual.der, nuevaPosicionDer, arbol, altura,
                                    nivel=nivel + 1)
    pygame.draw.line(componenteDeVisualizacion, generarColorAlAzar(), posicionRaiz,
                     posicionFinalDer, anchoDeLinea)
    pygame.draw.circle(componenteDeVisualizacion, generarColorAlAzar(), posicionRaiz, 7, 1)
    # Pongo el texto del nombre del nodo
    dibujarInfoNodo(componenteDeVisualizacion, nodoActual, posicionRaiz)


def dibujarCaso3(componenteDeVisualizacion, nodoActual, posicionRaiz, dx, dy, anchoDeLinea, arbol, altura, nivel):
    # calculo las nuevas posiciones
    nuevaPosicionIzq = (posicionRaiz[0] - dx, posicionRaiz[1] + dy)

    posicionFinalIzq = dibujarArbol(componenteDeVisualizacion, nodoActual.izq, nuevaPosicionIzq, arbol, altura,
                                    nivel=nivel + 1)

    pygame.draw.line(componenteDeVisualizacion, generarColorAlAzar(), posicionRaiz,
                     (posicionFinalIzq[0], posicionFinalIzq[1]), anchoDeLinea)
    pygame.draw.circle(componenteDeVisualizacion, generarColorAlAzar(), posicionRaiz, 7, 1)
    # Pongo el texto del nombre del nodo
    dibujarInfoNodo(componenteDeVisualizacion, nodoActual, posicionRaiz)


def dibujarCaso4(componenteDeVisualizacion, nodoActual, posicionRaiz, nivel):
    pygame.draw.circle(componenteDeVisualizacion, generarColorAlAzar(), posicionRaiz, 7, 1)
    # Pongo el texto del nombre del nodo
    dibujarInfoNodo(componenteDeVisualizacion, nodoActual, posicionRaiz)


def dibujarInfoNodo(componenteDeVisualizacion, nodo, posicionRaiz):
    x = str(nodo.x)
    y = str(nodo.y)
    dy = 10  # distancia en y desde el punto del nodo, se usa para graficar la informacion del nodo (puntos)
    dx = 10  # distancia en x desde el punto del nodo, se usa para graficar la informacion del nodo (puntos)
    fuente = pygame.font.SysFont('Comic Sans MS', 10, True)
    texto = fuente.render(nodo.nombre, True, (250, 100, 0))
    texto1 = fuente.render(x + ",", True, (200, 0, 0))  # se grafica el valor x del nodo
    texto2 = fuente.render(y, True, (200, 0, 0))  # se grafica el valor y del nodo
    componenteDeVisualizacion.blit(texto, (posicionRaiz[0] + dx, posicionRaiz[1] - 15 + dy))
    componenteDeVisualizacion.blit(texto1, (posicionRaiz[0] + dx, posicionRaiz[1] + dy))
    componenteDeVisualizacion.blit(texto2, (posicionRaiz[0] + dx + 15, posicionRaiz[1] + dy))


def eliminarRectaDeLista(identificador, lista):
    for i in range(0, len(lista)):
        if lista[i].id == identificador:
            del lista[i]
            return True


class posicionamientoMatriz:
    def __init__(self, x, y, tamanoObjetos, radio, distanciaEntreObjetos):
        self.x = x
        self.y = y
        self.tamanoObjetos = tamanoObjetos
        self.radio = radio
        self.distanciaEntreObjetos = distanciaEntreObjetos


def cargarImagenesCasa():
    bano = pygame.image.load("..\Imagenes\pequeñas\Baño.png")
    cocina = pygame.image.load("..\Imagenes\pequeñas\Cocina.png")
    comedor = pygame.image.load("..\Imagenes\pequeñas\Comedor.png")
    habitacion = pygame.image.load("..\Imagenes\pequeñas\Habitacion.png")
    oficina = pygame.image.load("..\Imagenes\pequeñas\Oficina.png")
    pasillo = pygame.image.load("..\Imagenes\pequeñas\Pasillo.png")
    sala = pygame.image.load("..\Imagenes\pequeñas\Sala.png")

    listaImagenes = [bano, cocina, comedor, habitacion, oficina, pasillo, sala]
    listaEtiquetas = ["baño", "cocina", "comedor", "habitacion", "oficina", "pasillo", "sala"]
    lista = [listaImagenes, listaEtiquetas]
    return lista


def pintarImagenesCasa(componenteDeVisualizacion, lista, posicion, distancia, tamanoRectangulo):
    x = posicion[0]
    y = posicion[1]
    imagenes = lista[0]
    etiquetas = lista[1]
    listaRectangulos = []
    for i in range(0, len(imagenes)):
        componenteDeVisualizacion.blit(imagenes[i], (x, y))
        listaRectangulos.append(Rectangulo(x, y, tamanoRectangulo, tamanoRectangulo, etiquetas[i]))
        x += distancia
    return listaRectangulos


def pintarImagen(componenteDevisualizacion, listaImagenes, identificador, posicion):
    imagenes = listaImagenes[0]
    identificadores = listaImagenes[1]
    for i in range(0, len(identificadores)):
        if i == identificador:
            componenteDevisualizacion.blit(imagenes[i], posicion.x, posicion.y)
        return


def pintarImagenes(componenteDeVisualizacion, listaImagenes, listaPosiciones):
    for i in range(0, len(listaImagenes)):
        # print(type(listaImagenes[i]))
        if listaImagenes[i] != None:
            componenteDeVisualizacion.blit(listaImagenes[i], listaPosiciones[i])


def devolverRectangulosMatriz(matriz):
    listaRectangulos = []
    contador = 3
    for y in range(len(matriz)):
        for x in range(len(matriz[y])):
            if matriz[y][x] == 0:
                punto = rellenarMatriz(matriz, (x, y), contador)
                listaRectangulos.append(punto)
                contador += 1
        # if len(matriz[y]) == 0:
        #     print("la matriz en y =", y, "es nula")
    # print(len(listaRectangulos))
    return listaRectangulos


def rellenarMatriz(matriz, indice, contador):
    xi = indice[0]
    yi = indice[1]
    yf = 0
    xf = 0
    # x = 0
    for y in range(yi, len(matriz)):
        for x in range(xi, len(matriz[y])):
            if matriz[y][x] == 0:
                matriz[y][x] = contador
                # if x == 0:
                #
            else:
                xf = x - 1
                break
            xf = x
        if y + 1 < len(matriz):
            if matriz[y + 1][x - 1] != 0:
                yf = y
                break

    #matriz[yi][xi] = 49 # el 49 es un color de una lista de colores, lo uso para pintar el punto inicial
    #matriz[y][xf] = 40 #lo mismo pero para el punto final
    # pongo un +1 en el ancho y el alto porque la matriz empieza desde 0 y para hallar el area se cuenta desde 1
    return Rectangulo(xi, yi, (xf - xi) +1, (y - yi) + 1, contador)


def pintarRectangulosColores(componendeDeVisualizacion, numeroRectangulos, tamano, listaColores, posicion=[0, 0]):
    xi = posicion[0]
    yi = posicion[1]
    x = xi
    y = yi
    listaRectangulos = []
    for i in range(1, numeroRectangulos):
        pygame.draw.rect(componendeDeVisualizacion, listaColores[i], (x, y, tamano, tamano))
        recangulo = Rectangulo(x, y, tamano, tamano, i)
        listaRectangulos.append(recangulo)
        x = x + tamano

    return listaRectangulos