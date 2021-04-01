from Graphics.Gui import Gui
from Logic.Tree import Tree
class Window:
    def __init__(self):
        self.arbol = Tree()
    def start(self):
        self.gui = Gui(self.arbol)
vent = Window()
vent.start()