import pygame
from objects.constants import *
from objects.pieces import *

class Square:
    def __init__(self, row, col, piece = None, rect = None):
        self.row = row
        self.col = col
        self.piece = piece
        self.rect = rect

    def add_piece(self, new_piece):
        self.piece = new_piece

    def fresh_piece(self, new_piece, color):
        if new_piece == 'pawn':
            self.piece = Pawn(color)
        elif new_piece == 'knight':
            self.piece = Knight(color)
        elif new_piece == 'rook':
            self.piece = Rook(color)
        elif new_piece == 'bishop':
            self.piece = Bishop(color)
        elif new_piece == 'queen':
            self.piece = Queen(color)
        elif new_piece == 'king':
            self.piece = King(color)
    
    def show_square(self, scrn):
        pygame.draw.circle(scrn, (200, 100, 0),[self.col*SQSIZE+SQSIZE/2, self.row*SQSIZE+SQSIZE/2], SQSIZE//4, 0)