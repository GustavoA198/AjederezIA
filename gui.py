import pygame

# Dimensiones del tablero y celdas. VARIABLES
ANCHO, ALTO = 640, 640
FILAS, COLUMNAS = 8, 8
TAMAÑO_CUADRO = ANCHO // COLUMNAS
TAMAÑO_IMG = ANCHO / FILAS

# Colores
BLANCO = (255, 255, 255)
CAFE = (170, 131, 79)

# Cargar imágenes de las piezas
imagenes_piezas = {
    # piezas blancas
    "CABb": pygame.image.load("imagenes/caballo-b.png"),
    "TORb": pygame.image.load("imagenes/torre-b.png"),
    "ALFb": pygame.image.load("imagenes/alfil-b.png"),
    "REIb": pygame.image.load("imagenes/reina-b.png"),
    "REYb": pygame.image.load("imagenes/rey-b.png"),
    "PEOb": pygame.image.load("imagenes/peon-b.png"),
    # piezas negras
    "TORn": pygame.image.load("imagenes/torre-n.png"),
    "CABn": pygame.image.load("imagenes/caballo-n.png"),
    "ALFn": pygame.image.load("imagenes/alfil-n.png"),
    "REIn": pygame.image.load("imagenes/reina-n.png"),
    "REYn": pygame.image.load("imagenes/rey-n.png"),
    "PEOn": pygame.image.load("imagenes/peon-n.png")
}

# matriz de juego
tablero = [
    ["TORb", "CABb", "ALFb", "REIb", "REYb", "ALFb", "CABb", "TORb"],
    ["PEOb", "PEOb", "PEOb", "PEOb", "PEOb", "PEOb", "PEOb", "PEOb"],
    ["----", "----", "----", "----", "----", "----", "----", "----"],
    ["----", "----", "----", "----", "----", "----", "----", "----"],
    ["----", "----", "----", "----", "----", "----", "----", "----"],
    ["----", "----", "----", "----", "----", "----", "----", "----"],
    ["PEOn", "PEOn", "PEOn", "PEOn", "PEOn", "PEOn", "PEOn", "PEOn"],
    ["TORn", "CABn", "ALFn", "REIn", "REYn", "ALFn", "CABn", "TORn"]
]

# Inicializar Pygames sa
pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Tablero de Ajedrez")

# función que dibuja el tablero de juego 8X8
def dibujar_tablero():
    for fila in range(FILAS):
        for columna in range(COLUMNAS):
            color = BLANCO if (fila + columna) % 2 == 0 else CAFE
            pygame.draw.rect(pantalla, color, (columna * TAMAÑO_CUADRO,
                             fila * TAMAÑO_CUADRO, TAMAÑO_CUADRO, TAMAÑO_CUADRO))

# función que recorre la matriz de juego y dibuja las piezas
def dibujar_piezas(tablero):
    for fil in range(FILAS):
        for col in range(COLUMNAS):
            pieza = tablero[fil][col]
            if pieza == "----":
                pass
            else:
                imagen_pza = imagenes_piezas[pieza]
                # recta_pieza = imagen_pza.get_rect()
                recta_pieza = pygame.transform.scale(
                    imagen_pza, (TAMAÑO_CUADRO, TAMAÑO_CUADRO))
                # recta_pieza.topleft = (col * TAMAÑO_CUADRO, fil * TAMAÑO_CUADRO)
                # recibe una imagen y las coordenadas
                pantalla.blit(
                    recta_pieza, (col * TAMAÑO_CUADRO, fil * TAMAÑO_CUADRO))

#_______________________ LOGICA DEL JUEGO ________________________________________________

# Variables para el primer clic y lograr mover la pieza
pieza_seleccionada = None
fila_seleccionada = None
columna_seleccionada = None
pieza_seleccionada_borde = None

# Variable para almacenar el turno actual
turn = 'b' # el turno inicial siempre es para las blancas

# Ciclo principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Botón izquierdo del ratón     CLICK 1                
                mouse_x, mouse_y = pygame.mouse.get_pos()  # Obtener las coordenadas del clic
                print("f", mouse_x, "c", mouse_y)
                clicked_fil = mouse_y // TAMAÑO_CUADRO  # Convertir las coordenadas del clic en la posición de la celda
                clicked_col = mouse_x // TAMAÑO_CUADRO

                # Verificar si es el turno del jugador actual
                if (turn == 'b' and tablero[clicked_fil][clicked_col][-1]) or (turn == 'n' and tablero[clicked_fil][clicked_col][-1]):

                    if pieza_seleccionada is None:  # Primer clic: Seleccionar la pieza en la celda                    
                        pieza_seleccionada = tablero[clicked_fil][clicked_col]# Obtener el valor de la pieza en la posición de la celda
                        fila_seleccionada = clicked_fil
                        columna_seleccionada = clicked_col
                        pieza_seleccionada_borde = pygame.Rect(clicked_col * TAMAÑO_CUADRO, clicked_fil * TAMAÑO_CUADRO, TAMAÑO_CUADRO, TAMAÑO_CUADRO)

                    
                    else:# Segundo clic: Mover la pieza a la nueva posición (si es válida)
                        # if is_valid_move(selected_row, selected_col, clicked_row, clicked_col): funcion para verificar movimientos permitidos en el futuro
                                            
                        # Mover la pieza a una nueva posición (la del click 2 y vaciar la del click 1)
                        tablero[clicked_fil][clicked_col] = pieza_seleccionada
                        tablero[fila_seleccionada][columna_seleccionada] = "----"                        
                        turn = 'n' if turn == 'b' else 'b' # Cambiar al siguiente turno

                        # Reiniciar las variables del primer clic
                        pieza_seleccionada = None
                        fila_seleccionada = None
                        columna_seleccionada = None 
                        pieza_seleccionada_borde = None             

    # pantalla.fill(BLANCO)
    # Llamado de funciones
    dibujar_tablero()
    dibujar_piezas(tablero)

    # Dibujar el borde rojo alrededor de la pieza seleccionada
    if pieza_seleccionada_borde is not None:
        pygame.draw.rect(pantalla, (255, 0, 0), pieza_seleccionada_borde, 3)

    pygame.display.flip()

pygame.quit()
