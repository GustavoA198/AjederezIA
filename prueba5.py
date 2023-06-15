import chess
import pygame

pygame.init()
ANCHO, ALTO = 720, 640
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Ajedrez")
clock = pygame.time.Clock()

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

# dimensiones y posición de cada cuadro del tablero
TAMAÑO_CUADRO = ALTO // 8

# Función para dibujar el tablero y las piezas:


def draw_board(board):
    # casilla para la piezacapturada
    pygame.draw.rect(pantalla, (230, 230, 200), (8 * TAMAÑO_CUADRO, 4 * TAMAÑO_CUADRO, TAMAÑO_CUADRO, TAMAÑO_CUADRO))

    for fil in range(8):
        for col in range(8):
            square_color = (255, 255, 255) if (
                fil + col) % 2 == 0 else (170, 131, 79)
            pygame.draw.rect(pantalla, square_color, (col * TAMAÑO_CUADRO, fil * TAMAÑO_CUADRO, TAMAÑO_CUADRO, TAMAÑO_CUADRO))

            pieza = board.piece_at(chess.square(col, 7 - fil))
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


# funcion para graficar los poibles movimientos
def posibles_movimientos_grafica(posicion, movimientos):
    for movimiento in movimientos:
        if movimiento.from_square == posicion:
            destino = movimiento.to_square
            col = chess.square_file(destino)
            fil = 7 - chess.square_rank(destino)
            # dibujar todo el cuadro de opciones
            # pygame.draw.rect(pantalla, (0, 255, 0, 128), (col * TAMAÑO_CUADRO , fil * TAMAÑO_CUADRO, TAMAÑO_CUADRO, TAMAÑO_CUADRO))

            # Calcular el centro de la casilla de destino
            centro_x = col * TAMAÑO_CUADRO + TAMAÑO_CUADRO // 2
            centro_y = fil * TAMAÑO_CUADRO + TAMAÑO_CUADRO // 2
            # Dibujar un punto en el centro de la casilla de destino
            radio = 5
            pygame.draw.circle(pantalla, (255, 0, 0),
                               (centro_x, centro_y), radio)


# tablero del juego
pantalla.fill((255, 255, 255))  # Establecer el fondo en blanco
tablero = chess.Board()

# Variable para almacenar el turno actual
turno = chess.WHITE
turnoLoco = chess.BLACK

# Variables para almacenar la posición seleccionada y el movimiento
posicion_seleccionada = None
movimientos_seleccionados = []
posicion_original = None  # Variable para almacenar la posición original de la pieza
mouse_posicion = None  # Variable para almacenar la posición del cursor del mouse
pieza_capturada = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # cerrar el juego
            running = False
        # Verificar si el rey está en jaque mate
        if tablero.is_checkmate():  # Verificar si el rey está en jaque mate
            # running = False
            # Dibujar la palabra "Jaque Mate" en el tablero
            font = pygame.font.Font(None, 70)
            text = font.render("Jaque Mate", True, (255, 0, 0))
            text_rect = text.get_rect(center=(ANCHO // 2, ALTO // 2))
            pantalla.blit(text, text_rect)

    # ... código para manejar el movimiento de las piezas ...
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:  # Obtener la posición del clic
                x, y = pygame.mouse.get_pos()
                col = x // TAMAÑO_CUADRO
                fil = y // TAMAÑO_CUADRO

                posicion = chess.square(col, 7 - fil)
                # obtener la pieza que se encontraba en la posicion del click
                pieza = tablero.piece_at(posicion)

                if pieza is not None and pieza.color == turno:  # Pieza válida seleccionada
                    posicion_seleccionada = posicion
                    # lista de mocimientos legales para el tablero en la jugada x
                    movimientos_seleccionados = list(tablero.legal_moves)
                    posicion_original = posicion  # por ahora no se usa

            elif event.type == pygame.MOUSEBUTTONUP and posicion_seleccionada is not None:  # movimiento del mouse
                # Obtener la posición del clic de soltar el botón del mouse
                x, y = pygame.mouse.get_pos()
                col = x // TAMAÑO_CUADRO
                fil = y // TAMAÑO_CUADRO

                destino = chess.square(col, 7 - fil)
                movimiento = chess.Move(posicion_seleccionada, destino)

                # any() para verificar si existe algún movimiento en movimientos_seleccionados con las mismas posiciones de origen y destino que nuestro movimiento actual.
                # Verificar si el movimiento es válido
                if any(movimiento.from_square == move.from_square and movimiento.to_square == move.to_square for move in movimientos_seleccionados):
                    # if movimiento in movimientos:
                    tablero_temporal = tablero.copy()
                    tablero_temporal.push(movimiento)

                    # Obtener el rey y su posicion, del jugador que realiza el movimiento para verificar que el movimiento no deje a su rey en jaque
                    if tablero.turn == chess.WHITE:
                        rey_posicion = tablero_temporal.king(chess.WHITE)
                        piezas_atacantes = chess.BLACK
                    else:
                        rey_posicion = tablero_temporal.king(chess.BLACK)
                        piezas_atacantes = chess.WHITE

                    # verificar que el rey del que realiza el movimiento no quede en jaque
                    if not tablero_temporal.is_attacked_by(piezas_atacantes, rey_posicion):

                        # Cambiar la pieza capturada de color
                        pieza_capturada = tablero.piece_at(destino)  # Guardar la pieza capturada
                        print("Pieza capturada:", pieza_capturada)
                        if pieza_capturada is not None:
                            pieza_capturada = cambiar_color_pieza(pieza_capturada)
                            print("Pieza capturada color:", pieza_capturada)
                        

                        # Detectar si un peón alcanza la última fila
                        pieza = tablero.piece_type_at(movimiento.from_square)
                        if pieza == chess.PAWN and chess.square_rank(movimiento.to_square) in [0, 7]:
                            print("promocion bb")
                            # movimiento.promotion = chess.QUEEN
                            movimiento_promocion = chess.Move(movimiento.from_square, movimiento.to_square, promotion=chess.QUEEN)
                            tablero.push(movimiento_promocion)
                            turno = not turno
                        else:
                            # ya verifico que el rey no queda en jaque
                            tablero.push(movimiento)
                            turno = not turno  # cambio el turno
                        #tablero.set_piece_at(posicion, pieza_capturada)
                        
                                      

                # Restablecer las variables de selección
                print("posicion", posicion_seleccionada)
                posicion_seleccionada = None
                movimientos_seleccionados = []
                mouse_posicion = None
                posicion_original = None
                #pieza_capturada = None

            elif event.type == pygame.MOUSEMOTION:  # Actualizar la posición del cursor del mouse
                x, y = pygame.mouse.get_pos()
                posicion_mause = (x, y)
            
        #parte grafica__________________________________________________________________________________________

            # Dibujar el tablero y las piezas
            draw_board(tablero)            

            #grafica los posibles moovimientos
            posibles_movimientos_grafica(posicion_seleccionada, movimientos_seleccionados)             

            # Dibujar la pieza seleccionada en la posición del mouse, si ésta está siendo arrastrada
            if posicion_seleccionada is not None:
                if posicion_mause is not None:
                    x, y = posicion_mause

                pieza = tablero.piece_at(posicion_seleccionada)               

                if pieza.color == chess.WHITE:
                    imagen_pieza = imagenes_piezas_blancas[pieza.piece_type]
                else:
                    imagen_pieza = imagenes_piezas_negras[pieza.piece_type]

                imagen_pieza = pygame.transform.scale(imagen_pieza, (TAMAÑO_CUADRO, TAMAÑO_CUADRO))
                piece_rect = imagen_pieza.get_rect()
                piece_rect.center = (x, y)
                pantalla.blit(imagen_pieza, piece_rect)

    """ # Dibujar la pieza capturada en la posición de captura, si existe
                if destino is not None:
                    # Obtener la pieza capturada del tablero """  
           
                            
    while pieza_capturada is not None:        
        for event in pygame.event.get():
            draw_board(tablero)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    xx, yy = pygame.mouse.get_pos()  # Obtener la posición del clic
                    column = xx // TAMAÑO_CUADRO
                    fila = yy // TAMAÑO_CUADRO
                    pos = chess.square(column, 7 - fila)
                    
                    if pos is not None:
                        # Agregar una pieza 'x' en la posición "posicion_Seleccionada"
                        tablero.set_piece_at(pos, pieza_capturada)
                        pieza_capturada = None
                        break

    # Actualizar la pantalla
    pygame.display.flip()

    # pantalla.fill((255, 255, 255))
    # draw_board(tablero)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
