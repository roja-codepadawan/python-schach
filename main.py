import pygame
import chess
import os
from minimax import minimax, bewertung  # Externe Datei mit Minimax & Bewertungsfunktion

# === Einstellungen ===
WIDTH, HEIGHT = 480, 480
SQ_SIZE = WIDTH // 8
FPS = 15

# === Farben ===
WHITE = (240, 217, 181)
BROWN = (181, 136, 99)

# === Initialisierung ===
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Schach mit KI")
clock = pygame.time.Clock()

# === Figuren laden ===
IMAGES = {}
def lade_figuren():
    figuren = ['P', 'R', 'N', 'B', 'Q', 'K']
    for farbe in ['w', 'b']:
        for figur in figuren:
            name = farbe + figur
            path = os.path.join("assets", f"{name}.png")
            IMAGES[name] = pygame.transform.scale(pygame.image.load(path), (SQ_SIZE, SQ_SIZE))

# === Schachbrett zeichnen ===
def zeichne_brett(screen):
    colors = [WHITE, BROWN]
    for r in range(8):
        for c in range(8):
            farbe = colors[(r + c) % 2]
            pygame.draw.rect(screen, farbe, pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

# === Figuren zeichnen ===
def zeichne_figuren(screen, board):
    for r in range(8):
        for c in range(8):
            square = chess.square(c, 7 - r)
            piece = board.piece_at(square)
            if piece:
                bild = IMAGES[('w' if piece.color == chess.WHITE else 'b') + piece.symbol().upper()]
                screen.blit(bild, pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

# === Mausposition zu Brettkoordinate ===
def get_square_from_mouse(pos):
    x, y = pos
    col = x // SQ_SIZE
    row = 7 - (y // SQ_SIZE)
    return chess.square(col, row)

# === Hauptfunktion ===
def main():
    lade_figuren()
    board = chess.Board()
    selected_square = None
    running = True

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and board.turn == chess.WHITE:
                square = get_square_from_mouse(pygame.mouse.get_pos())
                if selected_square is None:
                    piece = board.piece_at(square)
                    if piece and piece.color == chess.WHITE:
                        selected_square = square
                else:
                    move = chess.Move(selected_square, square)
                    if move in board.legal_moves:
                        board.push(move)
                        selected_square = None
                    else:
                        selected_square = None

        if board.turn == chess.BLACK and not board.is_game_over():
            _, move = minimax(board, 2, float('-inf'), float('inf'), True)
            if move:
                board.push(move)

        zeichne_brett(screen)
        zeichne_figuren(screen, board)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
