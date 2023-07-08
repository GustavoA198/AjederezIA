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
        
valorDePieza = {
    chess.PAWN: [[10,10,10,10,10,10,10,10],
                [15,15,15,15,15,15,15,15],
                [11,11,12,13,13,12,11,11],
                [10.5,10.5,11,12.5,12.5,11,10.5,10.5],
                [10,11,11,13,13,11,11,10],
                [10.5,11,11,12,12,11,11,10.5],
                [10.5,8,8,8,8,8,8,10.5],
                [10,10,10,10,10,10,10,10],
                10],

    chess.ROOK: [[50,50,50,50,50,50,50,50],
                 [50.5,51,51,51,51,51,51,50.5],
                 [49.5,50,50,50,50,50,50,49.5],
                 [49.5,50,50,50,50,50,50,49.5],
                 [49.5,50,50,50,50,50,50,49.5],
                 [49.5,50,50,50,50,50,50,49.5],
                 [49.5,50,50,50,50,50,50,49.5],
                 [50,50,50,50.5,50.5,50,50,50],
                 50],

    chess.KNIGHT: [[25,26,27,27,27,27,26,25],
                   [26,28,30,30,30,30,28,26],
                   [27,30,31,31.5,31.5,31,30,27],
                   [27,30.5,31.5,32,32,31.5,30.5,27],
                   [27,30,31.5,32,32,31.5,30,27],
                   [27,30.5,31.5,32,32,31.5,30.5,27],
                   [26,28,30,30,30,30,28,26],
                   [25,26,27,27,27,27,26,25],
                   30
                   ],
    chess.BISHOP: [[28,29,29,29,29,29,29,28],
                   [29,30,30,30,30,30,30,29],
                   [29,30,30.5,31,31,30.5,30,29],
                   [29,30.5,30.5,31,31,30.5,30.5,29],
                   [29,30,31,31,31,31,30,29],
                   [29,31,31,31,31,31,31,29],
                   [29,30.5,30,30,30,30,30.5,29],
                   [28,29,29,29,29,29,29,28],
                    30
                   ],
    chess.QUEEN: [[88,89,89,89.5,89.5,89,89,88],
                  [89,90,90,90,90,90,90,89],
                  [89,90,90.5,90.5,90.5,90.5,90,89],
                  [89.5,90,90.5,90.5,90.5,90.5,90,89.5],
                  [90,90,90.5,90.5,90.5,90.5,90,89.5],
                  [89,90.5,90.5,90.5,90.5,90,89,89],
                  [89,90,90.5,90,90,90,90,89],
                  [88,89,89,89.5,89.5,89,89,88],
                  90
                  ],
    chess.KING: [[897,896,896,895,895,896,896,897],
                 [897,896,896,895,895,896,896,897],
                 [897,896,896,895,895,896,896,897],
                 [897,896,896,895,895,896,896,897],
                 [898,897,897,896,896,897,897,898],
                 [899,898,898,898,898,898,898,899],
                 [902,902,900,900,900,900,902,902],
                 [902,903,901,900,900,901,903,902],
                 900
                 ]
}

# Definición de la función para evaluar la posición en el tablero
def evaluar_tablero(tablero):
    Heuristica = 0
    for fil in range(8):
        for col in range(8):
            pieza = tablero.tablero.piece_at(chess.square(col,fil))
            if pieza is not None:
                if pieza.color == chess.WHITE:
                    Heuristica += valorDePieza[pieza.piece_type][fil][col]
                else:
                    Heuristica -= valorDePieza[pieza.piece_type][7-fil][7-col]

    for pieza in tablero.piezasB:
        Heuristica += valorDePieza[pieza.piece_type][8]

    for pieza in tablero.piezasN:
        Heuristica -= valorDePieza[pieza.piece_type][8]
    ##print(Heuristica , "hhh\n" , len(tablero.piezasB) , len(tablero.piezasN), tablero.tablero)  
     
    return Heuristica

# Definición de la función para generar los movimientos posibles
def generar_movimientos(tablero):
    movimientoAdd =list(tablero.tablero.legal_moves)
    for fil in range(8):
        for col in range(8):
            
            pieza = tablero.tablero.piece_at(chess.square(col, 7 - fil))
            if pieza is None:
                if tablero.tablero.turn == chess.WHITE:
                    for piezaAdd in tablero.piezasB:
                        destino = chess.square(col, 7-fil)#posicion de la libreria chess
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
    #pasamos pieza del verde a tablero normal
    else: #tablero verde
        #print("ENTROOOOOOOOO")
        if movimiento[1] in tablero.piezasN:
            piezasN_copia.remove(movimiento[1])#quitamos la pieza
        elif  movimiento[1] in tablero.piezasB:
            piezasB_copia.remove(movimiento[1])
        tablero_copia.set_piece_at(movimiento[0], movimiento[1]) #agregar pieza
        tablero_copia.turn = not tablero_copia.turn 
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
            valor = minimax(nuevo_tablero, profundidad - 1, alpha, beta, False) ##
            mejor_valor = max(mejor_valor, valor)
            alpha = max(alpha, mejor_valor)
            if beta <= alpha:
                break
        return mejor_valor
    else:
        mejor_valor = float("inf")
        movimientos = generar_movimientos(tablero)
        for movimiento in movimientos:
            nuevo_tablero = aplicar_movimiento(tablero, movimiento)
            valor = minimax(nuevo_tablero, profundidad - 1, alpha, beta, True) ##2
            mejor_valor = min(mejor_valor, valor)   
            beta = min(beta, mejor_valor) #10
            if beta <= alpha:#poda
                break
        return mejor_valor #

# Función para seleccionar el mejor movimiento usando el algoritmo minimax con poda alpha-beta


def seleccionar_mejor_movimiento(tableroAL,piezas):
    tablero = Tablero(tableroAL,piezas[0],piezas[1])
    mejor_movimiento = None
    mejor_valor = float("-inf")
    movimientos = generar_movimientos(tablero)
    alpha = float("-inf")
    for movimiento in movimientos:
        nuevo_tablero = aplicar_movimiento(tablero, movimiento)
        valor = minimax(nuevo_tablero, 2, alpha , float("inf"),False)
        if valor > mejor_valor:
            mejor_valor = valor #10
            mejor_movimiento = movimiento
            alpha = mejor_valor #10

    return mejor_movimiento

# Ejemplo de uso
""" tablero1 = chess.Board()  # Tablero inicial
piezaaaa=chess.Piece(chess.PAWN,chess.WHITE)
piezaaa=chess.Piece(chess.PAWN,chess.BLACK)
tablero = Tablero(tablero1,[piezaaaa,piezaaaa],[piezaaa])
mejor_movimiento = minimax(tablero, 0, float("-inf"), float("inf"), False)
print("El mejor movimiento es:", mejor_movimiento) """