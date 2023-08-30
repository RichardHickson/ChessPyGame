import pygame
from constants import *
from square import Square

class Board:
    def __init__(self):
        self.squares = [[0,0,0,0,0,0,0,0] for i in range(8)]
        self._squares_adder()

    def _squares_adder(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row,col)


board = Board()
