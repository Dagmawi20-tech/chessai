# openings.py
import random

# Famous opening lines — format: list of (from, to) moves in order
# Each entry is one opening variation
OPENINGS = [
    # Italian Game
    ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4"],
    # Sicilian Defense
    ["e2e4", "c7c5", "g1f3", "d7d6", "d2d4"],
    # French Defense
    ["e2e4", "e7e6", "d2d4", "d7d5", "b1c3"],
    # Ruy Lopez
    ["e2e4", "e7e5", "g1f3", "b8c6", "f1b5"],
    # Queen's Gambit
    ["d2d4", "d7d5", "c2c4", "e7e6", "b1c3"],
    # King's Indian Defense
    ["d2d4", "g8f6", "c2c4", "g7g6", "b1c3"],
    # London System
    ["d2d4", "d7d5", "g1f3", "g8f6", "c1f4"],
    # Caro-Kann Defense
    ["e2e4", "c7c6", "d2d4", "d7d5", "b1c3"],
    # Pirc Defense
    ["e2e4", "d7d6", "d2d4", "g8f6", "b1c3"],
    # English Opening
    ["c2c4", "e7e5", "b1c3", "g8f6", "g1f3"],
]

class OpeningBook:
    def __init__(self):
        # Pick a random opening at the start of each game
        self.line    = random.choice(OPENINGS)
        self.move_num = 0  # tracks how far into the opening we are

    def get_move(self, color, move_count):
        """
        Returns the next book move for the given color if we're still in the opening.
        move_count = total half-moves played so far.
        Black plays on odd half-moves (1, 3, 5...)
        """
        # Only use book for black (computer)
        if color != 'black':
            return None

        # Black's book moves are at positions 1, 3, 5... in the line
        black_moves = [m for i, m in enumerate(self.line) if i % 2 == 1]

        idx = move_count // 2
        if idx < len(black_moves):
            return black_moves[idx]
        return None

    def parse_book_move(self, move_str):
        """Convert 'e2e4' string to (fr, fc, tr, tc) coords"""
        COLS = 'abcdefgh'
        fc = COLS.index(move_str[0])
        fr = 8 - int(move_str[1])
        tc = COLS.index(move_str[2])
        tr = 8 - int(move_str[3])
        return fr, fc, tr, tc