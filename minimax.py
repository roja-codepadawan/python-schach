import chess

def bewertung(board):
    werte = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0
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
