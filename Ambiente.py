import chess
import pygame


pygame.init()
ANCHO, ALTO = 440, 440
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
                #piece_rect = piece_image.get_rect(center=cuadro_rect.center)
                pantalla.blit(piece_image, (col * TAMAÑO_CUADRO, fil * TAMAÑO_CUADRO))
                
tablero = chess.Board()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #cerrar el juego
            running = False 
        
    draw_board(tablero)
    pygame.time.delay(100)
    Nf3 = chess.Move.from_uci("g1f3")

    pygame.display.flip()
    clock.tick(60)

pygame.quit()