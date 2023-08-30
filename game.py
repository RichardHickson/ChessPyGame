import pygame

from constants import *
from board import Board
from pieces import *
from square import Square

class Game:
    def __init__(self):
        self.board = None
        self.checks = [[],[]]
        self.black_moves = []
        self.white_moves = []
        self.valid_white = [Square(0,0)]
        self.valid_black = [Square(0,0)]
        self.last_move = Square(0,0,Knight('white'))
        
        self.restart_game()

    def show_squares(self, scrn):
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col)%2 == 0:
                    color = (255,255,255)
                else:
                    color = (0,100,0)
                sq = pygame.draw.rect(scrn,color,pygame.Rect(SQSIZE*col,SQSIZE*row,SQSIZE,SQSIZE))
                self.board.squares[row][col].rect = sq

    def king_check(self):
        white_temp = []
        black_temp = []
        for row in range(ROWS):
            for col in range(COLS):
                sq = self.board.squares[row][col]
                if sq.piece is not None:
                    if sq.piece.name == 'king' and sq.piece.color == 'black':
                        black = sq
                    if sq.piece.name == 'king' and sq.piece.color == 'white':
                        white = sq
        for row in range(ROWS):
            for col in range(COLS):
                cur_sq = self.board.squares[row][col]
                cur_piece = cur_sq.piece
                if cur_piece is not None:
                    if cur_piece.color == 'white':
                        cur_piece.block(self, black, cur_sq)
                    if cur_piece.color == 'black':
                        cur_piece.block(self, white, cur_sq)
                    #cur_piece.update_moves(self)
                    for move in cur_piece.moves:
                        if move == black:
                            black_temp.append(cur_sq)
                        if move == white:
                            white_temp.append(cur_sq)
        self.checks = [white_temp,black_temp]
        

                        

    def get_positions(self):
        pos_arr = []
        white_temp = []
        black_temp = []
        whit_t1 = []
        black_t1 = []
        for row in range(ROWS):
            for col in range(COLS):
                cur_piece = self.board.squares[row][col].piece
                if cur_piece is not None:
                    ret = cur_piece.update_moves(self)
                    pos_arr.append((cur_piece.texture_rect, cur_piece, self.board.squares[row][col]))
                    if cur_piece.color == 'white':
                        white_temp+=cur_piece.moves
                        whit_t1 += cur_piece.moves
                        white_temp += ret
                    if cur_piece.color == 'black':
                        black_temp+=cur_piece.moves
                        black_t1 += cur_piece.moves
                        black_temp += ret
        self.white_moves = white_temp
        self.black_moves = black_temp
        self.valid_white = whit_t1
        self.valid_black = black_t1
        return pos_arr

    
    def show_pieces(self, scrn):
        for row in range(ROWS):
            for col in range(COLS):
                cur_piece = self.board.squares[row][col].piece
                if cur_piece is not None:
                    curImg = pygame.image.load(cur_piece.texture)
                    curImg = pygame.transform.smoothscale(curImg, (SQSIZE, SQSIZE))
                    curRect = curImg.get_rect(topleft = (col*SQSIZE,row*SQSIZE))
                    cur_piece.set_texture(curRect)
                    scrn.blit(curImg, curRect)

    def restart_game(self):
        self.board = Board()
        for row in range(ROWS):
            for col in range(COLS):
                cur_square = self.board.squares[row][col]
                if row == 1:
                    cur_square.add_piece(Pawn('black'))
                if row == 6:
                    cur_square.add_piece(Pawn('white'))
                if row == 0:
                    if col == 0 or col == 7:
                        cur_square.add_piece(Rook('black'))
                    if col == 1 or col == 6:
                        cur_square.add_piece(Knight('black'))
                    if col == 2 or col == 5:
                        cur_square.add_piece(Bishop('black'))
                    if col == 3:
                        cur_square.add_piece(Queen('black'))
                    if col == 4:
                        cur_square.add_piece(King('black'))
                if row == 7:
                    if col == 0 or col == 7:
                        cur_square.add_piece(Rook('white'))
                    if col == 1 or col == 6:
                        cur_square.add_piece(Knight('white'))
                    if col == 2 or col == 5:
                        cur_square.add_piece(Bishop('white'))
                    if col == 3:
                        cur_square.add_piece(Queen('white'))
                    if col == 4:
                        cur_square.add_piece(King('white'))
                



