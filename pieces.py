# pieces.py

class Piece:
    def __init__(self, color):
        self.color = color  # 'white' or 'black'

    def opponent(self):
        return 'black' if self.color == 'white' else 'white'

    def __str__(self):
        return self.symbol()


class Pawn(Piece):
    def symbol(self):
        return '♙' if self.color == 'white' else '♟'

    def moves(self, row, col, board, en_passant_target=None):
        moves = []
        direction = -1 if self.color == 'white' else 1
        start_row  =  6 if self.color == 'white' else 1

        # Move forward one
        nr = row + direction
        if 0 <= nr <= 7 and board[nr][col] is None:
            moves.append((nr, col))
            # Move forward two from start
            if row == start_row and board[nr + direction][col] is None:
                moves.append((nr + direction, col))

        # Normal captures
        for dc in (-1, 1):
            nc = col + dc
            if 0 <= nr <= 7 and 0 <= nc <= 7:
                if board[nr][nc] and board[nr][nc].color == self.opponent():
                    moves.append((nr, nc))
                # En passant capture
                elif en_passant_target and (nr, nc) == en_passant_target:
                    moves.append((nr, nc))

        return moves


class Rook(Piece):
    def symbol(self):
        return '♖' if self.color == 'white' else '♜'

    def moves(self, row, col, board):
        return sliding_moves(self, row, col, board, [(1,0),(-1,0),(0,1),(0,-1)])


class Knight(Piece):
    def symbol(self):
        return '♘' if self.color == 'white' else '♞'

    def moves(self, row, col, board):
        moves = []
        for dr, dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr <= 7 and 0 <= nc <= 7:
                if board[nr][nc] is None or board[nr][nc].color == self.opponent():
                    moves.append((nr, nc))
        return moves


class Bishop(Piece):
    def symbol(self):
        return '♗' if self.color == 'white' else '♝'

    def moves(self, row, col, board):
        return sliding_moves(self, row, col, board, [(1,1),(1,-1),(-1,1),(-1,-1)])


class Queen(Piece):
    def symbol(self):
        return '♕' if self.color == 'white' else '♛'

    def moves(self, row, col, board):
        return sliding_moves(self, row, col, board,
                             [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)])


class King(Piece):
    def symbol(self):
        return '♔' if self.color == 'white' else '♚'

    def moves(self, row, col, board):
        moves = []
        for dr, dc in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr <= 7 and 0 <= nc <= 7:
                if board[nr][nc] is None or board[nr][nc].color == self.opponent():
                    moves.append((nr, nc))
        return moves


def sliding_moves(piece, row, col, board, directions):
    moves = []
    for dr, dc in directions:
        nr, nc = row + dr, col + dc
        while 0 <= nr <= 7 and 0 <= nc <= 7:
            if board[nr][nc] is None:
                moves.append((nr, nc))
            elif board[nr][nc].color == piece.opponent():
                moves.append((nr, nc))
                break
            else:
                break
            nr += dr
            nc += dc
    return moves