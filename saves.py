# saves.py
import json
import os
from pieces import Pawn, Rook, Knight, Bishop, Queen, King

SAVE_FILE = "save.json"

PIECE_MAP = {
    'Pawn':   Pawn,
    'Rook':   Rook,
    'Knight': Knight,
    'Bishop': Bishop,
    'Queen':  Queen,
    'King':   King,
}

def piece_to_dict(piece):
    if piece is None:
        return None
    return {
        'type':  type(piece).__name__,
        'color': piece.color
    }

def dict_to_piece(d):
    if d is None:
        return None
    return PIECE_MAP[d['type']](d['color'])

def save_game(board, move_log, clock, captured_white, captured_black):
    data = {
        'grid': [[piece_to_dict(board.grid[r][c])
                  for c in range(8)] for r in range(8)],
        'turn':               board.turn,
        'moved':              list(board.moved),
        'en_passant_target':  board.en_passant_target,
        'move_log':           move_log,
        'clock':              clock,
        'captured_white':     [piece_to_dict(p) for p in captured_white],
        'captured_black':     [piece_to_dict(p) for p in captured_black],
    }
    with open(SAVE_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def load_game(board):
    if not os.path.exists(SAVE_FILE):
        return None
    with open(SAVE_FILE) as f:
        data = json.load(f)

    for r in range(8):
        for c in range(8):
            board.grid[r][c] = dict_to_piece(data['grid'][r][c])

    board.turn              = data['turn']
    board.moved             = set(tuple(m) for m in data['moved'])
    board.en_passant_target = tuple(data['en_passant_target']) \
                              if data['en_passant_target'] else None
    board.status            = None

    move_log       = data['move_log']
    clock          = data['clock']
    captured_white = [dict_to_piece(p) for p in data['captured_white']]
    captured_black = [dict_to_piece(p) for p in data['captured_black']]

    return move_log, clock, captured_white, captured_black