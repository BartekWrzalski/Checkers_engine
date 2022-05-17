import copy
import math
import time
import pygame
from .constants import *
from checkers.board import Board


class Game:
    def __init__(self, win, mode='pvp', depth=3, algorithm='min-max'):
        self.win = win
        self.mode = mode

    def start_game(self, heuristic=1, depth=3, algorithm='min-max'):
        self._init()
        self.heur_num = heuristic
        self.depth = depth
        self.algorithm = algorithm
        self.update()
        self._playmode()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = WHITE
        self.valid_moves = {}
        self.move_length = 0
        self.moves_to_draw = 15

    def _playmode(self):
        match self.mode:
            case 'pvp':
                return
            case 'ivi':
                self._ivi()
            case 'pvi':
                self._pvi()
    """
    def _pvp(self):
        self.board.minmax(self.turn,
                          self.move_length,
                          copy.deepcopy(self.board))
    """
    def _ivi(self):
        if self.winner():
            return

        match self.algorithm:
            case 'min-max':
                _, (self.selected, move, to_skip) = self.board.minmax(self.turn,
                                                                      self.board.get_longest_move(self.turn),
                                                                      self.depth,
                                                                      self.heur_num)
            case 'alfa-beta':
                _, (self.selected, move, to_skip) = self.board.alfa_beta(self.turn,
                                                                         self.board.get_longest_move(self.turn),
                                                                         self.depth,
                                                                         -math.inf,
                                                                         math.inf,
                                                                         self.heur_num)
        if move:
            self._moveAI(move[0], move[1], to_skip)

    def _pvi(self):
        if self.turn == WHITE:
            return
        else:
            self._ivi()

    def update(self):
        self.board.draw(self.win)
        self.draw_evaluated_moves()
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def draw_evaluated_moves(self):
        eval1_str = VALUATION_FONT.render('E1: ' + str(self.board.validate_one(self.turn)), True, BLACK)
        eval2_str = VALUATION_FONT.render('E2: ' + str(self.board.validate_two(self.turn)), True, BLACK)
        self.win.blit(eval1_str, (WIDTH + 10, WIDTH // 2 + 10))
        self.win.blit(eval2_str, (WIDTH + 10, 3 * WIDTH // 4 + 10))

    def winner(self):
        if self.moves_to_draw == 0:
            print(DRAW)
        winner = self.board.winner(self.turn)
        if winner:
            print(winner)
            return True
        return False

    def reset(self):
        self._init()

    def select(self, row, col):
        if col >= COLS:
            return False

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
            skipped = self.valid_moves[(row, col)]
            if skipped:
                com = 'x' * len(skipped)
                self.board.remove(skipped)
            if self.selected.king:
                self.moves_to_draw -= 1
            else:
                self.moves_to_draw = 15
            self.board.update_notation(f'{st} {com} {en}')
            self.change_turn()
            return True

        return False

    def _moveAI(self, row, col, skipped):
        st, en = self.board.move(self.selected, row, col)
        com = '-'
        if skipped:
            com = 'x' * len(skipped)
            self.board.remove(skipped)
        if self.selected.king:
            self.moves_to_draw -= 1
        else:
            self.moves_to_draw = 15
        self.board.update_notation(f'{st} {com} {en}')
        time.sleep(0.05)
        self.change_turn()

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE,
                               (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def change_turn(self):
        self.valid_moves = {}
        self.update()
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
