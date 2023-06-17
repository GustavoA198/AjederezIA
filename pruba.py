import chess
import pygame
import Ambiente as IA

# Dimensiones del tablero y celdas. VARIABLES
pygame.init()
ANCHO, ALTO = 800, 640
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Ajedrez")
clock = pygame.time.Clock()

# Colores
BLANCO = (255, 255, 255)
CAFE = (170, 131, 79)
#retorna una tupla con las piezas del tablero loco
def piezas_capturadas_tupla():
    tupla =[[],[]]    
    for fil in range(8):
        for col in range(2):
            cuadro = chess.square(col, fil)
            pieza = tableroLoco.piece_at(cuadro)
            if pieza is not None and col == 0:
                tupla[0].append(pieza)
            elif pieza is not None and col == 1:
                tupla[1].append(pieza)
    return tupla

# Cargar imágenes de las piezas en un diccionario
imagenes_piezas_blancas = {
    chess.PAWN: pygame.image.load("imagenes/peon-b.png"),
    chess.ROOK: pygame.image.load("imagenes/torre-b.png"),
    chess.KNIGHT: pygame.image.load("imagenes/caballo-b.png"),
    chess.BISHOP: pygame.image.load("imagenes/alfil-b.png"),
    chess.QUEEN: pygame.image.load("imagenes/reina-b.png"),
    chess.KING: pygame.image.load("imagenes/rey-b.png")
}
imagenes_piezas_negras = {
    chess.PAWN: pygame.image.load("imagenes/peon-n.png"),
    chess.ROOK: pygame.image.load("imagenes/torre-n.png"),
    chess.KNIGHT: pygame.image.load("imagenes/caballo-n.png"),
    chess.BISHOP: pygame.image.load("imagenes/alfil-n.png"),
    chess.QUEEN: pygame.image.load("imagenes/reina-n.png"),
    chess.KING: pygame.image.load("imagenes/rey-n.png")
}

# matriz de juego para las piezas capturadas
tableroLoco = chess.Board()
tableroLoco.clear() #vaciar el tablero 2

# dimensiones y posición de cada cuadro del tablero
TAMAÑO_CUADRO = ALTO // 8

# Función para dibujar el tablero y las piezas
def draw_board(board, board2):    
    for fil in range(8):
        for col in range(10):
            if fil < 8 and col < 8:
                color_cuadro = (255, 255, 255) if (fil + col) % 2 == 0 else (170, 131, 79)
                pygame.draw.rect(pantalla, color_cuadro, (col * TAMAÑO_CUADRO, fil * TAMAÑO_CUADRO, TAMAÑO_CUADRO, TAMAÑO_CUADRO))
                pieza = board.piece_at(chess.square(col, 7 - fil))
                if pieza is not None:
                    if pieza.color == chess.WHITE:
                        piece_image = imagenes_piezas_blancas[pieza.piece_type]
                    else:
                        piece_image = imagenes_piezas_negras[pieza.piece_type]
                    piece_image = pygame.transform.scale(piece_image, (TAMAÑO_CUADRO, TAMAÑO_CUADRO))
                    # piece_rect = piece_image.get_rect(center=cuadro_rect.center)
                    pantalla.blit(piece_image, (col * TAMAÑO_CUADRO, fil * TAMAÑO_CUADRO))
            else:#dibuja el tablero de las piezas que han sido capturadas -> tableroLoco
                color_cuadro =  (144, 238, 144) 
                pygame.draw.rect(pantalla, color_cuadro, (col * TAMAÑO_CUADRO, fil * TAMAÑO_CUADRO, TAMAÑO_CUADRO, TAMAÑO_CUADRO))
                pieza = board2.piece_at(chess.square(col - 8, 7-fil))
                if pieza is not None:
                    if pieza.color == chess.WHITE:
                        piece_image = imagenes_piezas_blancas[pieza.piece_type]
                    else:
                        piece_image = imagenes_piezas_negras[pieza.piece_type]
                    piece_image = pygame.transform.scale(piece_image, (TAMAÑO_CUADRO, TAMAÑO_CUADRO))
                    # piece_rect = piece_image.get_rect(center=cuadro_rect.center)
                    pantalla.blit(piece_image, (col * TAMAÑO_CUADRO, fil * TAMAÑO_CUADRO))

# funcion para cambiar el color de una pieza
def cambiar_color_pieza(pieza):
    if pieza.color == chess.WHITE:
        pieza_nueva = chess.Piece(piece_type=pieza.piece_type, color=chess.BLACK)
    else:
        pieza_nueva = chess.Piece(piece_type=pieza.piece_type, color=chess.WHITE)
    return pieza_nueva


def eliminar_pieza(pieza):
    # Iterar sobre todas las casillas del tablero
    for casilla in chess.SQUARES:
        if tableroLoco.piece_at(casilla) == pieza:
            tableroLoco.remove_piece_at(casilla) 

# función para graficar los posibles movimientos de una pieza seleccionada
def posibles_movimientos_grafica(posicion_seleccionada, movimientos):
    for movimiento in movimientos:
        if movimiento.from_square == posicion_seleccionada:
            destino = movimiento.to_square
            col = chess.square_file(destino)
            fil = 7 - chess.square_rank(destino)
            # Calcular el centro de la casilla de destino
            centro_x = col * TAMAÑO_CUADRO + TAMAÑO_CUADRO // 2
            centro_y = fil * TAMAÑO_CUADRO + TAMAÑO_CUADRO // 2
            # Dibujar un punto en el centro de la casilla de destino
            radio = 5
            pygame.draw.circle(pantalla, (255, 0, 0),(centro_x, centro_y), radio)

def posibles_movimientos_completos(tablero):
    for casilla in chess.SQUARES:
        pieza = tablero.piece_at(casilla)
        if pieza is not None:
            movimientos = tablero.legal_moves
            for movimiento in movimientos:
                if movimiento.from_square == casilla:
                    destino = movimiento.to_square
                    col = chess.square_file(destino)
                    fil = 7 - chess.square_rank(destino)
                    # Calcular el centro de la casilla de destino
                    centro_x = col * TAMAÑO_CUADRO + TAMAÑO_CUADRO // 2
                    centro_y = fil * TAMAÑO_CUADRO + TAMAÑO_CUADRO // 2
                    # Dibujar un punto en el centro de la casilla de destino
                    radio = 5
                    pygame.draw.circle(pantalla, (255, 0, 0),(centro_x, centro_y), radio)

#guardar la pieza capturada
def guardar_captura(pieza_capturada):
    col = 0 if pieza_capturada.color == chess.WHITE else 1
    for fil in range(8):
        cuadro = chess.square(col, fil)
        pieza= tableroLoco.piece_at(cuadro)
        if pieza is None:
            tableroLoco.set_piece_at(cuadro,pieza_capturada)
            return

# tablero del juego
pantalla.fill((255, 255, 255))  # Establecer el fondo en blanco
tablero = chess.Board()

# Variables para almacenar la posición seleccionada y el movimiento
destino = None
posicion_mayor = False
pieza_seleccionada_borde = None
posicion_seleccionada = None
pieza_seleccionada = None
movimientos_seleccionados = []
pieza_capturada = None    

#_______________________ LOGICA DEL JUEGO ________________________________________________
running = True
cont = 0
while running:
    if True:
        for event in pygame.event.get():   
            if event.type == pygame.QUIT:
                running = False
            draw_board(listaTablero[cont])
            cont += 1

    
    pygame.display.flip()  
    clock.tick(60)

pygame.quit()
