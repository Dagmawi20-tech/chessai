# pgn.py
import os
from datetime import datetime

def export_pgn(move_log, result, difficulty, filename=None):
    """
    Exports the game to a .pgn file.
    result: '1-0' (white wins), '0-1' (black wins), '1/2-1/2' (draw)
    """
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename  = f"game_{timestamp}.pgn"

    date = datetime.now().strftime("%Y.%m.%d")

    # Build PGN header
    headers = (
        f'[Event "ChessAI Game"]\n'
        f'[Site "Terminal"]\n'
        f'[Date "{date}"]\n'
        f'[White "Player"]\n'
        f'[Black "ChessAI ({difficulty})"]\n'
        f'[Result "{result}"]\n\n'
    )

    # Build move text — pair white and black moves
    moves_text = []
    for i in range(0, len(move_log), 2):
        move_num   = i // 2 + 1
        white_move = move_log[i]
        black_move = move_log[i + 1] if i + 1 < len(move_log) else ""
        if black_move:
            moves_text.append(f"{move_num}. {white_move} {black_move}")
        else:
            moves_text.append(f"{move_num}. {white_move}")

    pgn_body = " ".join(moves_text) + f" {result}"

    # Save to file
    with open(filename, "w") as f:
        f.write(headers + pgn_body + "\n")

    return filename