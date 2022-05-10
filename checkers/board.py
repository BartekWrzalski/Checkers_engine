import pygame
from .constants import *
from .piece import Piece


class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()
        self.can_move = True

    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, WHITE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self, piece, row, col):
        st = FIELD_NUMBERS[piece.row][piece.col]
        en = FIELD_NUMBERS[row][col]
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1
        return st, en

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, RED))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, WHITE))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1

    def winner(self, turn):
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED

        if not self.can_move:
            if turn == WHITE:
                return RED
            else:
                return WHITE

        return None

    def validate_one(self, turn):
        evaluation = 0.1 if turn == WHITE else -0.1

        for i, row in enumerate(self.board):
            for j, piece in enumerate(row):
                if piece != 0:
                    is_white = piece.color == WHITE
                    if not piece.king:
                        evaluation += PAWN_VALUES_ONE[i] if is_white else -PAWN_VALUES_ONE[-i - 1]
                    else:
                        evaluation += KING_VALUES[i][j] if is_white else -KING_VALUES[-i - 1][-j - 1]
        return round(evaluation, 2)

    def validate_two(self, turn):
        evaluation = 0.1 if turn == WHITE else -0.1

        for i, row in enumerate(self.board):
            for j, piece in enumerate(row):
                if piece != 0:
                    is_white = piece.color == WHITE
                    if not piece.king:
                        evaluation += PAWN_VALUES_TWO[i][j] if is_white else -PAWN_VALUES_TWO[-i - 1][-j - 1]
                    else:
                        evaluation += KING_VALUES[i][j] if is_white else -KING_VALUES[-i - 1][-j - 1]
        return round(evaluation, 2)

    def get_valid_moves(self, piece, length=None):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.king:
            moves.update(self._traverse_left_king(row - 1, -1, -1, piece.color, left))
            moves.update(self._traverse_left_king(row + 1, ROWS, 1, piece.color, left))
            moves.update(self._traverse_right_king(row - 1, -1, -1, piece.color, right))
            moves.update(self._traverse_right_king(row + 1, ROWS, 1, piece.color, right))
        else:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left,
                                             True if piece.color == WHITE else False))
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left,
                                             False if piece.color == WHITE else True))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right,
                                              True if piece.color == WHITE else False))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right,
                                              False if piece.color == WHITE else True))

        if length:
            correct_moves = {}
            for key, value in moves.items():
                if len(value) == length:
                    correct_moves[key] = value
            moves = correct_moves
        return moves

    def _traverse_left(self, start, stop, step, color, left, forward, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                elif forward:
                    moves[(r, left)] = last
                elif not forward and r != start:
                    moves[(r, left)] = last

                if last:
                    last += skipped
                    if step == -1:
                        row = max(r - 3, -1)
                        opposite = min(r + 3, ROWS)
                    else:
                        row = min(r + 3, ROWS)
                        opposite = max(r - 3, -1)
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, forward, skipped=last))
                    moves.update(self._traverse_left(r - step, opposite, -step, color, left - 1, not forward, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, forward, skipped=last))
                break
            elif current.color == color:
                break
            else:
                if current in skipped:
                    break
                last = [current]

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, forward, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                elif forward:
                    moves[(r, right)] = last
                elif not forward and r != start:
                    moves[(r, right)] = last

                if last:
                    last += skipped
                    if step == -1:
                        row = max(r - 3, -1)
                        opposite = min(r + 3, ROWS)
                    else:
                        row = min(r + 3, ROWS)
                        opposite = max(r - 3, -1)
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, forward, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, forward, skipped=last))
                    moves.update(self._traverse_right(r - step, opposite, -step, color, right + 1, not forward, skipped=last))
                break
            elif current.color == color:
                break
            else:
                if current in skipped:
                    break
                last = [current]

            right += 1

        return moves

    def _traverse_left_king(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    last += skipped
                    moves.update(self._traverse_left_king(r + step, stop, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_left_king(r - step, ROWS - stop - 1, -step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right_king(r + step, stop, step, color, left + 1, skipped=last))
            elif current.color == color or last:
                break
            else:
                if current in skipped:
                    break
                last = [current]

            left -= 1

        return moves

    def _traverse_right_king(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= ROWS:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    last += skipped
                    moves.update(self._traverse_left_king(r + step, stop, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right_king(r + step, stop, step, color, right + 1, skipped=last))
                    moves.update(
                        self._traverse_right_king(r - step, ROWS - stop - 1, -step, color, right + 1, skipped=last))
            elif current.color == color or last:
                break
            else:
                if current in skipped:
                    break
                last = [current]

            right += 1

        return moves

    def get_longest_move(self, color):
        longest = -1
        for row in self.board:
            for tile in row:
                if tile != 0:
                    if tile.color == color:
                        moves = self.get_valid_moves(tile)
                        if moves:
                            moves = dict(sorted(moves.items(), key=lambda k: len(k[1]), reverse=True))
                            longest_local = len(list(moves.values())[0])
                            if longest_local > longest:
                                longest = longest_local
        if longest == -1:
            self.can_move = False
        return longest
