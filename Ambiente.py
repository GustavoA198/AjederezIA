
import chess

tablero = chess.Board()
print(tablero)

def aplicar_movimientos(tablero, movimientos):
    for movimiento in movimientos:
        tablero_copia = tablero.copy()  # Crea una copia del tablero original
        tablero_copia.push(movimiento)  # Aplica el movimiento a la copia del tablero
        print(tablero_copia)

aplicar_movimientos(tablero, list(tablero.legal_moves))

