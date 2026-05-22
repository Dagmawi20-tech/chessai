# board.py
import copy
from pieces import Pawn, Rook, Knight, Bishop, Queen, King

class Board:
    def __init__(self):
        self.grid = [[None] * 8 for _ in range(8)]
        self.turn = 'white'
        self.status = None
        self.moved = set()  # tracks which pieces have moved
        self.en_passant_target = None  # square where en passant capture is possible
        self.setup()

    def setup(self):
        order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for col, PieceClass in enumerate(order):
            self.grid[0][col] = PieceClass('black')
        for col in range(8):
            self.grid[1][col] = Pawn('black')
        for col, PieceClass in enumerate(order):
            self.grid[7][col] = PieceClass('white')
        for col in range(8):
            self.grid[6][col] = Pawn('white')

    def get_piece(self, row, col):
        return self.grid[row][col]

    def can_castle_kingside(self, color):
        row = 7 if color == 'white' else 0
        king  = self.grid[row][4]
        rook  = self.grid[row][7]
        if not isinstance(king, King) or not isinstance(rook, Rook):
            return False
        if (row, 4) in self.moved or (row, 7) in self.moved:
            return False
        if self.grid[row][5] or self.grid[row][6]:
            return False
        if self.is_in_check(color):
            return False
        # King must not pass through check
        for col in (5, 6):
            test = copy.deepcopy(self)
            test.grid[row][col] = test.grid[row][4]
            test.grid[row][4]   = None
            if test.is_in_check(color):
                return False
        return True

    def can_castle_queenside(self, color):
        row = 7 if color == 'white' else 0
        king  = self.grid[row][4]
        rook  = self.grid[row][0]
        if not isinstance(king, King) or not isinstance(rook, Rook):
            return False
        if (row, 4) in self.moved or (row, 0) in self.moved:
            return False
        if self.grid[row][1] or self.grid[row][2] or self.grid[row][3]:
            return False
        if self.is_in_check(color):
            return False
        # King must not pass through check
        for col in (3, 2):
            test = copy.deepcopy(self)
            test.grid[row][col] = test.grid[row][4]
            test.grid[row][4]   = None
            if test.is_in_check(color):
                return False
        return True

    def move(self, from_row, from_col, to_row, to_col):
        piece = self.grid[from_row][from_col]
        self.en_passant_target = None

        # En passant capture
        if isinstance(piece, Pawn) and (to_row, to_col) == self.en_passant_target:
            captured_row = from_row  # the captured pawn is on the same row as attacker
            self.grid[captured_row][to_col] = None

        self.grid[to_row][to_col] = piece
        self.grid[from_row][from_col] = None
        self.moved.add((to_row, to_col))

        # Set en passant target if pawn moved two squares
        if isinstance(piece, Pawn) and abs(to_row - from_row) == 2:
            self.en_passant_target = ((from_row + to_row) // 2, to_col)

        # Pawn promotion
        if isinstance(piece, Pawn):
            if (piece.color == 'white' and to_row == 0) or \
               (piece.color == 'black' and to_row == 7):
                self.grid[to_row][to_col] = Queen(piece.color)

        self.turn = 'black' if self.turn == 'white' else 'white'
        self.update_status()

    def castle_kingside(self, color):
        row = 7 if color == 'white' else 0
        self.grid[row][6] = self.grid[row][4]
        self.grid[row][5] = self.grid[row][7]
        self.grid[row][4] = None
        self.grid[row][7] = None
        self.moved.add((row, 6))
        self.moved.add((row, 5))
        self.turn = 'black' if self.turn == 'white' else 'white'
        self.update_status()

    def castle_queenside(self, color):
        row = 7 if color == 'white' else 0
        self.grid[row][2] = self.grid[row][4]
        self.grid[row][3] = self.grid[row][0]
        self.grid[row][4] = None
        self.grid[row][0] = None
        self.moved.add((row, 2))
        self.moved.add((row, 3))
        self.turn = 'black' if self.turn == 'white' else 'white'
        self.update_status()

    def find_king(self, color):
        for row in range(8):
            for col in range(8):
                p = self.grid[row][col]
                if isinstance(p, King) and p.color == color:
                    return row, col
        return None

    def is_in_check(self, color):
        king_pos = self.find_king(color)
        if not king_pos:
            return False
        opponent = 'black' if color == 'white' else 'white'
        for row in range(8):
            for col in range(8):
                p = self.grid[row][col]
                if p and p.color == opponent:
                    if king_pos in p.moves(row, col, self.grid):
                        return True
        return False

    def legal_moves(self, color):
        moves = []
        for row in range(8):
            for col in range(8):
                p = self.grid[row][col]
                if p and p.color == color:
                    if isinstance(p, Pawn):
                        raw = p.moves(row, col, self.grid, self.en_passant_target)
                    else:
                        raw = p.moves(row, col, self.grid)
                    for to_row, to_col in raw:
                        test = copy.deepcopy(self)
                        test.grid[to_row][to_col] = test.grid[row][col]
                        test.grid[row][col] = None
                        # Remove en passant captured pawn
                        if isinstance(p, Pawn) and self.en_passant_target == (to_row, to_col):
                            test.grid[row][to_col] = None
                        if not test.is_in_check(color):
                            moves.append((row, col, to_row, to_col))
        return moves

    def update_status(self):
        moves = self.legal_moves(self.turn)
        if not moves:
            if self.is_in_check(self.turn):
                self.status = 'checkmate'
            else:
                self.status = 'stalemate'