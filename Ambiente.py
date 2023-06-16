import random
import numpy as np
import chess


# Definición de la función para evaluar la posición en el tablero
def evaluar_tablero(tablero):
    # Aquí puedes implementar tu propia función de evaluación
    # que asigne un valor a la posición actual del tablero
    return random.randint(25, 35)

# Definición de la función para generar los movimientos posibles
def generar_movimientos(tablero, piezas):
    movimientos = tablero.legal_moves
    for fil in range(8):
        for col in range(8):
            
            pieza = tablero.piece_at(chess.square(col, 7 - fil))
            if pieza is None:
                for piezaAdd in piezas:
                    destino = chess.square(col-8, 7 - fil)
                    if not(piezaAdd.piece_type == chess.PAWN and (chess.square_rank(destino) in [0, 7])):
                        movimientos.add((destino,piezaAdd))
# Aquí debes implementar la generación de todos los movimientos
    # legales a partir del estado actual del tablero y retornarlos
    return movimientos

# Definición de la función para aplicar un 
# movimiento al tablero
def aplicar_movimiento(tablero, movimiento):
    tablero_copia = tablero.copy()
    if isinstance(movimiento, chess.Move):
        tablero_copia.push(movimiento)
    else:
        tablero_copia.set_piece_at(movimiento[0], movimiento[1])
        tablero_copia.turn = not tablero_copia.turn 
    # Aquí debes implementar la lógica para aplicar un movimiento
    # al tablero y retornar el nuevo tablero resultante
    return tablero_copia

# Definición de la función principal para la búsqueda con poda alpha-beta
def minimax(tablero, profundidad, alpha, beta, jugador_max):
    if profundidad == 0:
        return evaluar_tablero(tablero)

    if jugador_max:
        mejor_valor = float("-inf")
        movimientos = generar_movimientos(tablero,[])
        for movimiento in movimientos:
            nuevo_tablero = aplicar_movimiento(tablero, movimiento)
            valor = minimax(nuevo_tablero, profundidad - 1, alpha, beta, False)
            mejor_valor = max(mejor_valor, valor)
            alpha = max(alpha, mejor_valor)
            if beta <= alpha:
                break
        return mejor_valor
    else:
        mejor_valor = float("inf")
        movimientos = generar_movimientos(tablero,[])
        for movimiento in movimientos:
            nuevo_tablero = aplicar_movimiento(tablero, movimiento)
            valor = minimax(nuevo_tablero, profundidad - 1, alpha, beta, True)
            mejor_valor = min(mejor_valor, valor)
            beta = min(beta, mejor_valor)
            if beta <= alpha:
                break
        return mejor_valor

# Función para seleccionar el mejor movimiento usando el algoritmo minimax con poda alpha-beta
def seleccionar_mejor_movimiento(tablero,piezasA):
    mejor_movimiento = None
    mejor_valor = float("-inf")
    movimientos = generar_movimientos(tablero, piezasA)
    for movimiento in movimientos:
        nuevo_tablero = aplicar_movimiento(tablero, movimiento)
        valor = minimax(nuevo_tablero, 3, float("-inf"), float("inf"), False)
        if valor > mejor_valor:
            mejor_valor = valor
            mejor_movimiento = movimiento
    return mejor_movimiento

# Ejemplo de uso
""" tablero = chess.Board()  # Tablero inicial
mejor_movimiento = seleccionar_mejor_movimiento(tablero,[])
print("El mejor movimiento es:", mejor_movimiento) """
