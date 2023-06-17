import random
import numpy as np
import chess

def cambiar_color_pieza(pieza):
    if pieza.color == chess.WHITE:
        pieza_nueva = chess.Piece(piece_type=pieza.piece_type, color=chess.BLACK)
    else:
        pieza_nueva = chess.Piece(piece_type=pieza.piece_type, color=chess.WHITE)
    return pieza_nueva

class Tablero:
    def __init__(self,tablero,piezasB, piezasN):
        self.tablero = tablero
        self.piezasB = piezasB
        self.piezasN = piezasN
        
global pieza
valorDePieza = {
    chess.PAWN: 10,
    chess.ROOK: 50,
    chess.KNIGHT: 30,
    chess.BISHOP: 30,
    chess.QUEEN: 90,
    chess.KING: 900
}


# Definición de la función para evaluar la posición en el tablero
def evaluar_tablero(tablero):
    Heuristica = 0
    for fil in range(8):
        for col in range(8):
            pieza = tablero.tablero.piece_at(chess.square(col,fil))
            if fil>2 and fil<5 and col>1 and col<6 and pieza is not None:
                if pieza.color == chess.WHITE:
                    Heuristica += valorDePieza[pieza.piece_type]*2
                else:
                    Heuristica -= valorDePieza[pieza.piece_type]*2
            elif pieza is not None:
                if pieza.color == chess.WHITE:
                    Heuristica += valorDePieza[pieza.piece_type]
                else:
                    Heuristica -= valorDePieza[pieza.piece_type]

    for pieza in tablero.piezasB:
        Heuristica += valorDePieza[pieza.piece_type]*0.9

    for pieza in tablero.piezasN:
        Heuristica -= valorDePieza[pieza.piece_type]*0.9
    ##print(Heuristica , "hhh\n" , len(tablero.piezasB) , len(tablero.piezasN), tablero.tablero)  
     
    return Heuristica

# Definición de la función para generar los movimientos posibles
def generar_movimientos(tablero):
    movimientoAdd =list( tablero.tablero.legal_moves)
    for fil in range(8):
        for col in range(8):
            
            pieza = tablero.tablero.piece_at(chess.square(col, 7 - fil))
            if pieza is None:
                if tablero.tablero.turn == chess.WHITE:
                    for piezaAdd in tablero.piezasB:
                        destino = chess.square(col, 7-fil)
                        if not(piezaAdd.piece_type == chess.PAWN and (chess.square_rank(destino) in [0, 7])):
                            movimientoAdd.append((destino,piezaAdd))
                else:
                    for piezaAdd in tablero.piezasN:
                        destino = chess.square(col, 7 - fil)
                        if not(piezaAdd.piece_type == chess.PAWN and (chess.square_rank(destino) in [0, 7])):
                            movimientoAdd.append((destino,piezaAdd))
# Aquí debes implementar la generación de todos los movimientos
    # legales a partir del estado actual del tablero y retornarlos
    return movimientoAdd

# Definición de la función para aplicar un 
# movimiento al tablero
def aplicar_movimiento(tablero, movimiento):
    tableroOBJ_copia = tablero
    tablero_copia = tableroOBJ_copia.tablero.copy()
    piezasB_copia = tableroOBJ_copia.piezasB.copy()
    piezasN_copia = tableroOBJ_copia.piezasN.copy()
    if isinstance(movimiento, chess.Move):
        #print(movimiento)
        Pieza_Capturada =tablero_copia.piece_at(movimiento.to_square)
        tablero_copia.push(movimiento)
        if  Pieza_Capturada is not None:
            ##print("ENTROOOOOOOOO892379847928479")
            Pieza_Capturada = cambiar_color_pieza(Pieza_Capturada) 
            if Pieza_Capturada.color == chess.WHITE:
                piezasB_copia.append(Pieza_Capturada)
            else:
                piezasN_copia.append(Pieza_Capturada)

    else:
        #print("ENTROOOOOOOOO")
        if movimiento[1] in tablero.piezasN:
            piezasN_copia.remove(movimiento[1])
        elif  movimiento[1] in tablero.piezasB:
            piezasB_copia.remove(movimiento[1])
        tablero_copia.set_piece_at(movimiento[0], movimiento[1])
        tablero_copia.turn = not tablero_copia.turn 
    # Aquí debes implementar la lógica para aplicar un movimiento
    # al tablero y retornar el nuevo tablero resultante
    #print(tablero_copia)
    return Tablero(tablero_copia, piezasB_copia,piezasN_copia)

# Definición de la función principal para la búsqueda con poda alpha-beta
def minimax(tablero, profundidad, alpha, beta, jugador_max):
    if profundidad == 0:
        return evaluar_tablero(tablero)

    if jugador_max:
        mejor_valor = float("-inf")
        movimientos = generar_movimientos(tablero)
        for movimiento in movimientos:
            nuevo_tablero = aplicar_movimiento(tablero, movimiento)
            valor = minimax(nuevo_tablero, profundidad - 1, alpha, beta, False)
            mejor_valor = max(mejor_valor, valor)
            alpha = max(alpha, mejor_valor)
            if beta <= alpha:
                a=0
                ##break
        return mejor_valor
    else:
        mejor_valor = float("inf")
        movimientos = generar_movimientos(tablero)
        for movimiento in movimientos:
            nuevo_tablero = aplicar_movimiento(tablero, movimiento)
            valor = minimax(nuevo_tablero, profundidad - 1, alpha, beta, True)
            mejor_valor = min(mejor_valor, valor)
            beta = min(beta, mejor_valor)
            if beta <= alpha:
                a=0
                ##break
        return mejor_valor

# Función para seleccionar el mejor movimiento usando el algoritmo minimax con poda alpha-beta
def seleccionar_mejor_movimiento(tableroAL,piezas):
    tablero = Tablero(tableroAL,piezas[0],piezas[1])
    mejor_movimiento = None
    mejor_valor = float("-inf")
    movimientos = generar_movimientos(tablero)
    for movimiento in movimientos:
        nuevo_tablero = aplicar_movimiento(tablero, movimiento)
        valor = minimax(nuevo_tablero, 2, float("-inf"), float("inf"), False)
        if valor > mejor_valor:
            mejor_valor = valor
            mejor_movimiento = movimiento

    return mejor_movimiento

# Ejemplo de uso
""" tablero1 = chess.Board()  # Tablero inicial
piezaaaa=chess.Piece(chess.PAWN,chess.WHITE)
piezaaa=chess.Piece(chess.PAWN,chess.BLACK)
tablero = Tablero(tablero1,[piezaaaa,piezaaaa],[piezaaa])
mejor_movimiento = minimax(tablero, 0, float("-inf"), float("inf"), False)
print("El mejor movimiento es:", mejor_movimiento) """