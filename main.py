import chess

def bewertung(board):
    """Einfaches Bewertungssystem basierend auf Material."""
    werte = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0  # König bewerten wir nicht (ist eh nicht schlagbar)
    }

    score = 0
    for figurentyp in werte:
        score += len(board.pieces(figurentyp, chess.WHITE)) * werte[figurentyp]
        score -= len(board.pieces(figurentyp, chess.BLACK)) * werte[figurentyp]
    return score

def minimax(board, tiefe, alpha, beta, maximierend):
    if tiefe == 0 or board.is_game_over():
        return bewertung(board), None

    bester_zug = None

    if maximierend:
        max_eval = float('-inf')
        for zug in board.legal_moves:
            board.push(zug)
            eval, _ = minimax(board, tiefe - 1, alpha, beta, False)
            board.pop()
            if eval > max_eval:
                max_eval = eval
                bester_zug = zug
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, bester_zug
    else:
        min_eval = float('inf')
        for zug in board.legal_moves:
            board.push(zug)
            eval, _ = minimax(board, tiefe - 1, alpha, beta, True)
            board.pop()
            if eval < min_eval:
                min_eval = eval
                bester_zug = zug
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, bester_zug

def brett_anzeigen(board):
    """Zeigt das Schachbrett mit Koordinaten an."""
    brett_string = str(board)
    zeilen = brett_string.split("\n")
    print("  a b c d e f g h")
    for i, zeile in enumerate(zeilen):
        print(f"{8 - i} {zeile} {8 - i}")
    print("  a b c d e f g h")


def spiel_starten():
    board = chess.Board()
    print("Willkommen zu Schach! Du spielst Weiß.")
    brett_anzeigen(board)

    while not board.is_game_over():
        if board.turn == chess.WHITE:
            print("\nDein Zug (z. B. e2e4): ")
            eingabe = input("> ")
            try:
                move = chess.Move.from_uci(eingabe)
                if move in board.legal_moves:
                    board.push(move)
                    brett_anzeigen(board)
                else:
                    print("⚠️ Ungültiger Zug.")
            except:
                print("❌ Eingabefehler – Format: e2e4")
        else:
            print("\n🤖 KI denkt...")
            _, move = minimax(board, 2, float('-inf'), float('inf'), True)
            if move:
                print(f"🤖 KI spielt: {move.uci()}")
                board.push(move)
                brett_anzeigen(board)

    print("\n🎯 Spiel beendet!")
    print("Ergebnis:", board.result())

if __name__ == "__main__":
    spiel_starten()
# Hier wird das Schachspiel gestartet
# und die Hauptspiellogik ausgeführt.
