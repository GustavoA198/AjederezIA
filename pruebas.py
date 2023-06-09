import chess
import pygame

pygame.init()
ANCHO, ALTO = 640, 640
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

#dimensiones y posición de cada cuadro del tablero
TAMAÑO_CUADRO = ANCHO // 8

#Función para dibujar el tablero y las piezas:
def draw_board(board):
    for fil in range(8):
        for col in range(8):
            square_color = (255, 255, 255) if (fil + col) % 2 == 0 else (170, 131, 79)
            pygame.draw.rect(pantalla, square_color, (col * TAMAÑO_CUADRO , fil * TAMAÑO_CUADRO, TAMAÑO_CUADRO, TAMAÑO_CUADRO))

            pieza = board.piece_at(chess.square(col, 7 - fil))
            if pieza is not None:
                if pieza.color == chess.WHITE:
                    piece_image = imagenes_piezas_blancas[pieza.piece_type]
                else:
                    piece_image = imagenes_piezas_negras[pieza.piece_type]
                piece_image = pygame.transform.scale(piece_image, (TAMAÑO_CUADRO, TAMAÑO_CUADRO))
                pantalla.blit(piece_image, (col * TAMAÑO_CUADRO, fil * TAMAÑO_CUADRO))


#bucle principal del juego
tablero = chess.Board()

# Variable para almacenar el turno actual
turno = chess.WHITE

# Variables para almacenar la posición seleccionada y el movimiento
posicion_seleccionada = None
movimientos_seleccionados = []
posicion_original = None # Variable para almacenar la posición original de la pieza
mouse_posicion = None # Variable para almacenar la posición del cursor del mouse

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #cerrar el juego
            running = False 
        # Verificar si el rey está en jaque mate
        if tablero.is_checkmate():# Verificar si el rey está en jaque mate
            #running = False
            # Dibujar la palabra "Jaque Mate" en el tablero
            font = pygame.font.Font(None, 70)
            text = font.render("Jaque Mate", True, (255, 0, 0))
            text_rect = text.get_rect(center=(ANCHO // 2, ALTO // 2))
            pantalla.blit(text, text_rect)

    # ... código para manejar el movimiento de las piezas ...
        else:
            if event.type == pygame.MOUSEBUTTONDOWN: # Obtener la posición del clic
                x, y = pygame.mouse.get_pos()
                col = x // TAMAÑO_CUADRO
                fil = y // TAMAÑO_CUADRO

                posicion = chess.square(col, 7 - fil)
                pieza = tablero.piece_at(posicion)

                if pieza is not None and pieza.color == turno:  # Pieza válida seleccionada                
                    posicion_seleccionada = posicion
                    movimientos_seleccionados = list(tablero.legal_moves)
                    posicion_original = posicion
            
            elif event.type == pygame.MOUSEBUTTONUP and posicion_seleccionada is not None:
                x, y = pygame.mouse.get_pos() # Obtener la posición del clic de soltar el botón del mouse
                col = x // TAMAÑO_CUADRO
                fil = y // TAMAÑO_CUADRO

                destino = chess.square(col, 7 - fil)
                movimiento = chess.Move(posicion_seleccionada, destino)

                if movimiento in movimientos_seleccionados and not tablero.is_check():# Verificar si el movimiento es válido y el rey no está en jaque
                    tablero.push(movimiento)                
                    turno = not turno # Cambiar el turno
                    print("entra 1")

                    """ # Detectar si un peón alcanza la última fila
                    move = chess.Move(posicion_seleccionada, destino)
                    if move.piece_type == chess.PAWN and (move.to_square in chess.SquareSet(chess.RANK_7) or move.to_square in chess.SquareSet(chess.RANK_0)):
                        nueva_pieza = chess.QUEEN
                        tablero.set_piece_at(move.to_square, chess.Piece(nueva_pieza, tablero.turn)) # Actualizar el tablero reemplazando el peón por la nueva pieza """

                else:
                    tablero_temporal = tablero.copy() # Copiar el tablero actual en una copia temporal
                    tablero_temporal.push(movimiento)
                    print("entra 2")
                    print(movimiento)
                    print(tablero_temporal)
                    if tablero_temporal.is_check():
                        print("entra 3")
                        tablero.push(movimiento)                
                        turno = not turno # Cambiar el turno

               


                # Restablecer las variables de selección
                posicion_seleccionada = None
                movimientos_seleccionados = []
                mouse_posicion = None
                posicion_original = None

            elif event.type == pygame.MOUSEMOTION: # Actualizar la posición del cursor del mouse            
                x, y= pygame.mouse.get_pos()
                posicion_mause = (x, y)

            # Dibujar el tablero y las piezas
            draw_board(tablero)

            # Dibujar la pieza seleccionada en la posición del mouse, si ésta está siendo arrastrada
            if posicion_seleccionada is not None and posicion_mause is not None:            
                pieza = tablero.piece_at(posicion_seleccionada)
                
                if pieza.color == chess.WHITE:# Verificar el color de la pieza seleccionada y obtener la imagen adecuada
                    imagen_pieza = imagenes_piezas_blancas[pieza.piece_type]
                else:
                    imagen_pieza = imagenes_piezas_negras[pieza.piece_type]

                imagen_pieza = pygame.transform.scale(imagen_pieza, (TAMAÑO_CUADRO, TAMAÑO_CUADRO))
                piece_rect = imagen_pieza.get_rect()
                piece_rect.center = (x, y)
                pantalla.blit(imagen_pieza, piece_rect)

                """ # Borrar la pieza original antes de dibujar la nueva posición
                original_file = chess.square_file(posicion_seleccionada)
                original_rank = chess.square_rank(posicion_seleccionada)
                original_x = original_file * TAMAÑO_CUADRO
                original_y = (7 - original_rank) * TAMAÑO_CUADRO
                pantalla.fill(original_x, original_y, TAMAÑO_CUADRO, TAMAÑO_CUADRO)

                # Dibujar la nueva posición de la pieza
                pantalla.blit(imagen_pieza, piece_rect) """

    # Actualizar la pantalla
    pygame.display.flip()

    #pantalla.fill((255, 255, 255))
    #draw_board(tablero)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

