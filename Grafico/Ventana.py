from Grafico.Gui import Gui
from Logica.Arbol import Arbol


class ventana:
    def __init__(self):
        self.arbol = Arbol()
    def inicializar(self):
        self.gui = Gui(self.arbol)
vent = ventana()
vent.inicializar()