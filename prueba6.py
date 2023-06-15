import chess
import pygame

# Dimensiones del tablero y celdas. VARIABLES
pygame.init()
ANCHO, ALTO = 800, 640
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Ajedrez")
clock = pygame.time.Clock()

# Colores
BLANCO = (255, 255, 255)
CAFE = (170, 131, 79)

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
#tableroLoco.clear() #vaciar el tablero 2

# dimensiones y posición de cada cuadro del tablero
TAMAÑO_CUADRO = ALTO // 8

# Función para dibujar el tablero y las piezas
def draw_board(board, board2):
    # casilla para la pieza capturada
    #pygame.draw.rect(pantalla, (230, 230, 200), (8 * TAMAÑO_CUADRO, 4 * TAMAÑO_CUADRO, TAMAÑO_CUADRO, TAMAÑO_CUADRO))

    #Dibuja la matriz del juego
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
            else:
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

# función para graficar los posibles movimientos
def posibles_movimientos_grafica(posicion_seleccionada, movimientos):
    for movimiento in movimientos:
        if movimiento.from_square == posicion_seleccionada:
            destino = movimiento.to_square
            col = chess.square_file(destino)
            fil = 7 - chess.square_rank(destino)
            # dibujar todo el cuadro de opciones
            pygame.draw.rect(pantalla, (0, 255, 0, 128), (col * TAMAÑO_CUADRO , fil * TAMAÑO_CUADRO, TAMAÑO_CUADRO, TAMAÑO_CUADRO))

            # Calcular el centro de la casilla de destino
            centro_x = col * TAMAÑO_CUADRO + TAMAÑO_CUADRO // 2
            centro_y = fil * TAMAÑO_CUADRO + TAMAÑO_CUADRO // 2
            # Dibujar un punto en el centro de la casilla de destino
            radio = 10
            pygame.draw.circle(pantalla, (255, 0, 0),(centro_x, centro_y), radio)



# tablero del juego
pantalla.fill((255, 255, 255))  # Establecer el fondo en blanco
tablero = chess.Board()

# Variable para almacenar el turno actual
turno = chess.WHITE

# Variables para almacenar la posición seleccionada y el movimiento
posicion = None
posicion_mayor = False
pieza_seleccionada_borde = None
posicion_seleccionada = None
pieza_seleccionada = None
movimientos_seleccionados = []
posicion_original = None  # Variable para almacenar la posición original de la pieza
mouse_posicion = None  # Variable para almacenar la posición del cursor del mouse
pieza_capturada = None

#reinicar las variables del primer click
def reiniciarVariables():
    pieza_seleccionada_borde = None
    posicion_seleccionada = None
    pieza_seleccionada = None
    movimientos_seleccionados = []
    posicion_original = None 
    mouse_posicion = None  
    pieza_capturada = None   
    posicion = None
    posicion_mayor = False

#_______________________ LOGICA DEL JUEGO ________________________________________________
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        print(tablero.is_checkmate())
        if tablero.is_checkmate() is True:  # Verificar si el rey está en jaque mate
            #running = False
            # Dibujar la palabra "Jaque Mate" en el tablero
            font = pygame.font.Font(None, 70)
            text = font.render("Jaque Mate", True, (255, 0, 0))
            text_rect = text.get_rect(center=(ANCHO // 2, ALTO // 2))
            pantalla.blit(text, text_rect)

            

        # ... código para manejar el movimiento de las piezas ...    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Botón izquierdo del ratón     CLICK 1     
                mouse_x, mouse_y = pygame.mouse.get_pos()  # Obtener las coordenadas del clic
                fil = mouse_y // TAMAÑO_CUADRO  # Convertir las coordenadas del clic en la posición de la celda
                col = mouse_x // TAMAÑO_CUADRO

                """ #mover pieza capturada anterioremente
                if col >= 8:
                    posicion_seleccionada = chess.square(col-8, 7 - fil)
                    pieza_seleccionada = tableroLoco.piece_at(posicion_seleccionada)
                    pieza_seleccionada_borde = pygame.Rect((col) * TAMAÑO_CUADRO, fil * TAMAÑO_CUADRO, TAMAÑO_CUADRO, TAMAÑO_CUADRO)
                    posicion_mayor = True
                
                #SEGUNDO CLICK
                #else:
                    
                    #CASO 1 -> colocar una ficha que ha sido capturada """
                    if pieza_seleccionada is not None and pieza_seleccionada.color == turno and posicion_mayor is True:  # Pieza válida seleccionada  
                        posicion = posicion_seleccionada
                        
                        print("entro")
                    #elif :# Segundo clic: Mover la pieza a la nueva posición (si es válida)
                        destino = chess.square(col, 7 - fil)
                        if tablero.piece_at(destino) is None:
                            tablero.set_piece_at(destino, pieza_seleccionada)
                            posicion_mayor = False
                            #reiniciarVariables() #reiniciar las variables del pirmer click
                            turno = not turno
                            print(pieza_seleccionada, posicion)
                            

                    #CASO 2 -> movimiento de una pieza dentro del tablero
                    else:
                        posicion_seleccionada = chess.square(col, 7 - fil) # obtener la pieza que se encontraba en la posicion del click                
                        pieza_seleccionada = tablero.piece_at(posicion_seleccionada)

                        #dibujar el borde a la pieza selleccionada                    
                        pieza_seleccionada_borde = pygame.Rect(col * TAMAÑO_CUADRO, fil * TAMAÑO_CUADRO, TAMAÑO_CUADRO, TAMAÑO_CUADRO)                     
                    
                        movimientos_seleccionados = list(tablero.legal_moves) #lista de movimientos posibles
                        
                        if pieza_seleccionada is not None and pieza_seleccionada.color == turno:  # Pieza válida seleccionada es valida ysi es el turno del jugador actual              
                            posicion = posicion_seleccionada
                            
                        else:# Segundo clic: Mover la pieza a la nueva posición (si es válida)
                            destino = chess.square(col, 7 - fil)
                            movimiento = chess.Move(posicion, destino) #creo un movimiento
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
                                        reiniciarVariables()#Reiniciar las variables del primer clic

                                    else:
                                        # ya verifico que el rey no queda en jaque
                                        tablero.push(movimiento)
                                        turno = not turno  # cambio el turno
                                        print(pieza_seleccionada, posicion)
                                        reiniciarVariables()#Reiniciar las variables del primer clic                           

    #grafica los posibles moovimientos
    posibles_movimientos_grafica(posicion_seleccionada, movimientos_seleccionados)                                  
   
    # Llamado de funciones
    draw_board(tablero,tableroLoco)

    # Dibujar el borde rojo alrededor de la pieza seleccionada    
    if pieza_seleccionada_borde is not None:
        pygame.draw.rect(pantalla, (255, 0, 0), pieza_seleccionada_borde, 3)

    pygame.display.flip()
    clock.tick(3)

pygame.quit()
