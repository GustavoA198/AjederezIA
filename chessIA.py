import chess

class Nodo:
    def __init__(self, tablero, tipoNodo,Profundidad, Padre, movimiento):
        self.tablero = tablero
        self.tipoNodo = tipoNodo
        self.profundidad = Profundidad
        self.padre = Padre
        self.Utilidad = self.CalcUtilidad()
        self.movimiento = movimiento

    def CalcUtilidad(self):
        return 1


def CrearHijos (Nodo):
    for fil in range(8):
        for col in range(8):
            
            pieza = tablero.piece_at(chess.square(col, 7 - fil))
