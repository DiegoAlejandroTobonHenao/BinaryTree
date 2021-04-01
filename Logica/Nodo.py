class Nodo:
  def __init__(self, nombre, x, y):
    self.nombre = nombre
    self.izq = None
    self.der = None
    self.padre = None
    self.x = x
    self.y = y
    self.eje = None
    self.nivel = 0