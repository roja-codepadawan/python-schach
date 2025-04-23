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

# === Koordinaten zeichnen ===
def zeichne_brett(screen):
    colors = [WHITE, BROWN]
    for r in range(8):
        for c in range(8):
            farbe = colors[(r + c) % 2]
            pygame.draw.rect(screen, farbe, pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

    # Koordinaten zeichnen
    font = pygame.font.SysFont("Arial", 14)
    for i in range(8):
        # Buchstaben (a–h) oben und unten
        buchstabe = font.render(chr(ord('a') + i), True, (0, 0, 0))
        screen.blit(buchstabe, (i * SQ_SIZE + 5, HEIGHT - 15))  # unten
      #   screen.blit(buchstabe, (i * SQ_SIZE + 5, 2))             # oben (optional)

        # Zahlen (1–8) links und rechts
        zahl = font.render(str(8 - i), True, (0, 0, 0))
        screen.blit(zahl, (2, i * SQ_SIZE + 5))                  # links
      #   screen.blit(zahl, (WIDTH - 15, i * SQ_SIZE + 5))         # rechts (optional)

# === Mögliche Züge ===
def markiere_zuege(screen, board, selected_square):
    if selected_square is None:
        return

    for zug in board.legal_moves:
        if zug.from_square == selected_square:
            to_square = zug.to_square
            col = chess.square_file(to_square)
            row = 7 - chess.square_rank(to_square)

            ziel_feld = pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)

            if board.piece_at(to_square):
                # 🔴 Schlagzug (gegnerische Figur steht da)
                pygame.draw.rect(screen, (255, 0, 0, 100), ziel_feld, 5)  # rot, Rahmen
            else:
                # 🟩 Normaler Zug
                center = (col * SQ_SIZE + SQ_SIZE // 2, row * SQ_SIZE + SQ_SIZE // 2)
                pygame.draw.circle(screen, (0, 255, 0), center, 10)  # grün


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
        markiere_zuege(screen, board, selected_square)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
