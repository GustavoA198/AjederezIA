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
while running:
    if tablero.turn == chess.BLACK:
        for event in pygame.event.get():   
            if event.type == pygame.QUIT:
                running = False

            # ... código para manejar el movimiento de las piezas ...    
            elif event.type == pygame.MOUSEBUTTONDOWN:                          
                if event.button == 1:  # Botón izquierdo -> CLICK 1   
                    mouse_x, mouse_y = pygame.mouse.get_pos()  # Obtener las coordenadas del clic
                    fil = mouse_y // TAMAÑO_CUADRO  # Convertir las coordenadas del clic en la posición de la celda
                    col = mouse_x // TAMAÑO_CUADRO  

                    movimientos_seleccionados = list(tablero.legal_moves) #lista de movimientos legales

                    if pieza_seleccionada is None:
                        if col >= 8: #selecciono pieza del tablero loco
                            posicion_seleccionada = chess.square(col-8, 7 - fil)
                            pieza_seleccionada = tableroLoco.piece_at(posicion_seleccionada)
                            pieza_seleccionada_borde = pygame.Rect(col* TAMAÑO_CUADRO, fil * TAMAÑO_CUADRO, TAMAÑO_CUADRO, TAMAÑO_CUADRO)
                            movimientos_seleccionados = [] #para que no se muestren movimientos del segundo tablero
                            posicion_mayor = True
                        else: #selecciono pieza del tablero normal
                            posicion_seleccionada = chess.square(col, 7 - fil) # obtener la pieza que se encontraba en la posicion del click                
                            pieza_seleccionada = tablero.piece_at(posicion_seleccionada)
                            pieza_seleccionada_borde = pygame.Rect(col * TAMAÑO_CUADRO, fil * TAMAÑO_CUADRO, TAMAÑO_CUADRO, TAMAÑO_CUADRO)    
                        
                    #SEGUNDO CLICK
                    else:
                        if col < 8:
                            print("turno", tablero.turn)
                            destino = chess.square(col, 7-fil)

                            #CASO 1 -> colocar una ficha que ha sido capturada 
                            if pieza_seleccionada is not None and pieza_seleccionada.color == tablero.turn and posicion_mayor is True:  # Pieza válida seleccionada   
                                if pieza_seleccionada.piece_type == chess.PAWN and not (chess.square_rank(destino) in [0, 7]) or pieza_seleccionada.piece_type != chess.PAWN:  #verifica que no se ponga un peon capturado en la ultima fila, chess.square_rank(destino) obtiene la fila                   
                                    if tablero.piece_at(destino) is None:
                                        tablero.turn = not tablero.turn
                                        tableroLoco.remove_piece_at(posicion_seleccionada) #eliminar la ficha usada del tablero loco
                                        tablero.set_piece_at(destino, pieza_seleccionada) #tablero.set_piece_at(casilla, pieza)
                                        posicion_mayor = False                          
                                        #print("mov alterado","pieza",pieza_seleccionada, "destino", destino)
                                
                                #seteo de variables
                                pieza_seleccionada_borde = None
                                posicion_seleccionada = None
                                pieza_seleccionada = None
                                posicion_mayor = False
                                destino = None                            

                            #CASO 2 -> movimiento de una pieza dentro del tablero

                            else:                                          
                                if pieza_seleccionada is not None and pieza_seleccionada.color == tablero.turn:  # Pieza válida seleccionada es valida ysi es el turno del jugador actual     
                                    #print("color de pieza select:", pieza_seleccionada.color)
                                    movimiento = chess.Move(posicion_seleccionada, destino) #creo un movimiento -> chess.Move(casilla_origen, casilla_destino)
                                    #print("origen", movimiento.from_square, "destino = ",movimiento.to_square)
                                    if any(movimiento.from_square == move.from_square and movimiento.to_square == move.to_square for move in movimientos_seleccionados):
                                    #if movimiento in movimientos_seleccionados:
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
                                                guardar_captura(pieza_capturada)                           

                                            # Detectar si un peón alcanza la última fila y merece promocion por una reina
                                            pieza = tablero.piece_type_at(movimiento.from_square) 
                                            if pieza == chess.PAWN and chess.square_rank(movimiento.to_square) in [0, 7]:
                                                print("promocion bb")
                                                # movimiento.promotion = chess.QUEEN
                                                movimiento_promocion = chess.Move(movimiento.from_square, movimiento.to_square, promotion=chess.QUEEN)
                                                tablero.push(movimiento_promocion)
                                                #turno = not turno

                                            else:                                        
                                                if isinstance(movimiento, chess.Move):
                                                    tablero.push(movimiento)

                                                else:
                                                    tablero.set_piece_at(movimiento[0], movimiento[1])
                                                    tablero.turn = not tablero.turn 
                                """  
                                tableroia = IA.Tablero(tablero,[],[])
                                print(IA.evaluar_tablero(tableroia) , "VALOR tableroo")
                                for i in IA.generar_movimientos(tableroia):
                                    IA.aplicar_movimiento(tableroia,i)   """
                                        #print("mov normal","pieza",pieza_seleccionada, "destino", destino)
                                            #reiniciarVariables()#Reiniciar las variables del primer clic 
                                          
                                                    
                        #reiniciarVariables
                        destino = None
                        pieza_seleccionada_borde = None
                        posicion_seleccionada = None
                        pieza_seleccionada = None
                        pieza_capturada = None  
                        posicion_mayor = False
    else:
        movimiento = IA.seleccionar_mejor_movimiento(tablero,piezas_capturadas_tupla())
        if isinstance(movimiento, chess.Move):
            pieza_capturada =tablero.piece_at(movimiento.to_square)
            if  pieza_capturada is not None:
                pieza_capturada = cambiar_color_pieza(pieza_capturada)
                guardar_captura(pieza_capturada)
            tablero.push(movimiento)
        else:
            eliminar_pieza(movimiento[1]) 
            tablero.set_piece_at(movimiento[0], movimiento[1])
            tablero.turn = not tablero.turn
        pieza_capturada = None 



        
    # Llamado de funciones
    draw_board(tablero,tableroLoco)

    #grafica los posibles moovimientos
    posibles_movimientos_grafica(posicion_seleccionada, movimientos_seleccionados) 
    #posibles_movimientos_completos(tablero)

    # Dibujar el borde rojo alrededor de la pieza seleccionada    
    if pieza_seleccionada_borde is not None:
        pygame.draw.rect(pantalla, (255, 0, 0), pieza_seleccionada_borde, 3)
    
    # Verificar si el rey está en jaque mate
    if tablero.is_checkmate() is True:  
            #running = False            
            font = pygame.font.Font(None, 70)
            text = font.render("Jaque Mate", True, (255, 0, 0))# Dibujar la palabra "Jaque Mate" en el tablero
            text_rect = text.get_rect(center=(ANCHO // 2, ALTO // 2))
            pantalla.blit(text, text_rect)
            pygame.time.delay(100000)

    
    pygame.display.flip()  
    clock.tick(60)

pygame.quit()
