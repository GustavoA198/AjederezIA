import chess
import metodos

tablero = chess.Board
nodo1 = metodos.Tablero(tablero,[],[])
class Nodo:
    def __init__(self, tablero, mov):
        self.tablero = metodos.Tablero(tablero.table, tablero.piezasB,tablero.piezasN)                                       )
        self.tipoNodo = tablero.tablero.turn
        self.Utilidad = metodos.evaluar_tablero(tablero)
        self.Tableros  = metodos.generarTableros(tablero)

def crearArbol (nodo , profundidad):
    if profundidad ==0:
        return metodos.evaluar_tablero(nodo.tablero)
    else:
        return crearArbol()
        
              
   
   


   

