# engine.py
import copy
import random

# How much each piece is worth
PIECE_VALUES = {
    'Pawn':   100,
    'Knight': 320,
    'Bishop': 330,
    'Rook':   500,
    'Queen':  900,
    'King':   20000,
}

# Bonus scores for good piece positions
PAWN_TABLE = [
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [ 5,  5, 10, 25, 25, 10,  5,  5],
    [ 0,  0,  0, 20, 20,  0,  0,  0],
    [ 5, -5,-10,  0,  0,-10, -5,  5],
    [ 5, 10, 10,-20,-20, 10, 10,  5],
    [ 0,  0,  0,  0,  0,  0,  0,  0],
]

KNIGHT_TABLE = [
    [-50,-40,-30,-30,-30,-30,-40,-50],
    [-40,-20,  0,  0,  0,  0,-20,-40],
    [-30,  0, 10, 15, 15, 10,  0,-30],
    [-30,  5, 15, 20, 20, 15,  5,-30],
    [-30,  0, 15, 20, 20, 15,  0,-30],
    [-30,  5, 10, 15, 15, 10,  5,-30],
    [-40,-20,  0,  5,  5,  0,-20,-40],
    [-50,-40,-30,-30,-30,-30,-40,-50],
]

def piece_value(piece, row, col):
    name = type(piece).__name__
    base = PIECE_VALUES.get(name, 0)
    # Position bonus for pawns and knights
    if name == 'Pawn':
        table_row = row if piece.color == 'black' else 7 - row
        base += PAWN_TABLE[table_row][col]
    elif name == 'Knight':
        table_row = row if piece.color == 'black' else 7 - row
        base += KNIGHT_TABLE[table_row][col]
    return base

def evaluate(board):
    score = 0
    for row in range(8):
        for col in range(8):
            p = board.grid[row][col]
            if p:
                val = piece_value(p, row, col)
                score += val if p.color == 'black' else -val
    return score

def minimax(board, depth, alpha, beta, maximizing):
    if depth == 0 or board.status:
        return evaluate(board)

    moves = board.legal_moves('black' if maximizing else 'white')

    if maximizing:
        max_eval = float('-inf')
        for fr, fc, tr, tc in moves:
            new_board = copy.deepcopy(board)
            new_board.move(fr, fc, tr, tc)
            score = minimax(new_board, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, score)
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for fr, fc, tr, tc in moves:
            new_board = copy.deepcopy(board)
            new_board.move(fr, fc, tr, tc)
            score = minimax(new_board, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, score)
            beta = min(beta, score)
            if beta <= alpha:
                break
        return min_eval

def best_move(board, depth=2, color='black'):
    moves = board.legal_moves(color)
    if not moves:
        return None

    best       = None
    best_score = float('-inf') if color == 'black' else float('inf')

    random.shuffle(moves)

    for fr, fc, tr, tc in moves:
        new_board = copy.deepcopy(board)
        new_board.move(fr, fc, tr, tc)
        score = minimax(new_board, depth - 1, float('-inf'), float('inf'), color != 'black')
        if color == 'black' and score > best_score:
            best_score = score
            best = (fr, fc, tr, tc)
        elif color == 'white' and score < best_score:
            best_score = score
            best = (fr, fc, tr, tc)

    return best