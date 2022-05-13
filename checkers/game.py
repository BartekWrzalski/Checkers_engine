import copy
import time
import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE, DRAW
from checkers.board import Board


class Game:
    def __init__(self, win, mode='pvp'):
        self._init()
        self.win = win
        self.mode = mode
        self._playmode()
        self.update()

    def _playmode(self):
        match self.mode:
            case 'pvp':
                self._pvp()
            case 'ivi':
                self._ivi()

    def _pvp(self):
        self.board.minmax(self.turn,
                          self.board.get_longest_move(self.turn),
                          copy.deepcopy(self.board))

    def _ivi(self):
        self.selected, self.move, self.to_skip = self.board.minmax(self.turn,
                                                                   self.board.get_longest_move(self.turn),
                                                                   copy.deepcopy(self.board))
        self._moveAI(self.move[0], self.move[1], self.to_skip)

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = WHITE
        self.valid_moves = {}
        self.move_length = 0
        self.moves_to_draw = 15

    def winner(self):
        if self.moves_to_draw == 0:
            return DRAW
        return self.board.winner(self.turn)

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece, self.move_length)
            return True

        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            st, en = self.board.move(self.selected, row, col)
            com = '-'
            end = '\n' if self.selected.color == RED else '\t\t\t'
            skipped = self.valid_moves[(row, col)]
            if skipped:
                com = 'x' * len(skipped)
                self.board.remove(skipped)
            if self.selected.king:
                self.moves_to_draw -= 1
            else:
                self.moves_to_draw = 15
            # print(st, com, en, end=end)
            self.change_turn()
            # self.validate_first()
            # self.validation_second()
            # print()
            return True

        return False

    def _moveAI(self, row, col, skipped):
        print(self.selected.get_pos(), row, col, skipped)
        self.board.move(self.selected, row, col)
        if skipped:
            self.board.remove(skipped)
        if self.selected.king:
            self.moves_to_draw -= 1
        else:
            self.moves_to_draw = 15
        time.sleep(0.5)
        self.update()
        self.change_turn()

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE,
                               (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
            self.move_length = self.board.get_longest_move(WHITE)
        else:
            self.turn = RED
            self.move_length = self.board.get_longest_move(RED)
        self._playmode()

    def validate_first(self):
        evaluation = self.board.validate_one(self.turn)
        print(evaluation)

    def validation_second(self):
        evaluation = self.board.validate_two(self.turn)
        print(evaluation)
