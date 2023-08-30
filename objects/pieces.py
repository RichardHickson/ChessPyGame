import pygame
from objects.constants import *
import os

class Piece:
    def __init__(self, name, color, value, texture = None, texture_rect = None):
        self.name = name
        self.color = color
        self.value = value
        self.texture = 'pieces1/{}_{}.png'.format(color, name)
        self.texture_rect = texture_rect
        self.moves = []
        self.blockable = []
    
    def set_texture(self, texture_rec):
        self.texture_rect = texture_rec
    
    def check_moves(self, game, c):
        checks = game.checks[c]
        valid = []
        if self.name != 'king':
            if len(checks) < 2:
                if checks[0] in self.moves:
                    valid.append(checks[0])
            for chk in checks:
                if chk.piece is not None:
                    for blok in chk.piece.blockable:
                        if blok in self.moves:
                            valid.append(blok)
        self.moves = valid
        if self.name == 'rook':
            print(self.blockable)
                
        
    
        

class Pawn(Piece):
    def __init__(self, color):
        super().__init__('pawn', color, 1.0)

    def update_moves(self, game):
        ret = []
        col, row =  int(self.texture_rect[0]/SQSIZE), int(self.texture_rect[1]/SQSIZE)
        last_sq = game.last_move
        last_piece = last_sq.piece
        if self.color == 'white':
            row_max = 0
            new_moves = []
            
            if row > row_max and game.board.squares[row-1][col].piece is None:
                new_moves.append(game.board.squares[row-1][col])
            if row == 6 and game.board.squares[row-2][col].piece is None:
                new_moves.append(game.board.squares[row-2][col])
            if col !=7:
                if game.board.squares[row-1][col+1].piece is not None:
                    new_moves.append(game.board.squares[row-1][col+1])
                else:
                    ret.append(game.board.squares[row-1][col+1])
            if col != 0:
                if game.board.squares[row-1][col-1].piece is not None:
                    new_moves.append(game.board.squares[row-1][col-1])
                else:
                    ret.append(game.board.squares[row-1][col-1])
            if last_piece.name == 'pawn':
                if row == 3 and last_sq.row == 3 and last_sq.col == col+1:
                    new_moves.append(game.board.squares[row-1][col+1])
                if row == 3 and last_sq.row == 3 and last_sq.col == col-1:
                    new_moves.append(game.board.squares[row-1][col-1])
            self.moves = new_moves
        if self.color == 'black':
            row_max = 7
            new_moves = []
            if row == row_max:
                game.board.squares[row][col].fresh_piece('queen')
                return 0
            if row < row_max and game.board.squares[row+1][col].piece is None:
                new_moves.append(game.board.squares[row+1][col])
            if row == 1 and game.board.squares[row+2][col].piece is None:
                new_moves.append(game.board.squares[row+2][col])
            if col != 7:
                if game.board.squares[row+1][col+1].piece is not None:
                    new_moves.append(game.board.squares[row+1][col+1])
                else:
                    ret.append(game.board.squares[row+1][col+1])
            if col != 0:
                if game.board.squares[row+1][col-1].piece is not None:
                    new_moves.append(game.board.squares[row+1][col-1])
                else:
                    ret.append(game.board.squares[row+1][col-1])
            if last_piece.name == 'pawn':
                if row == 4 and last_sq.row == 4 and last_sq.col == col+1:
                    new_moves.append(game.board.squares[row+1][col+1])
                if row == 4 and last_sq.row == 4 and last_sq.col == col-1:
                    new_moves.append(game.board.squares[row+1][col-1])
            self.moves = new_moves
        if self.color == 'white':
            c = 0
        if self.color == 'black':
            c = 1
        if len(game.checks[c]) > 0:
            self.check_moves(game,c)
            
        return ret

    def block(self, game, king_sq, cur_sq):
        pass

class Knight(Piece):
    def __init__(self, color):
        super().__init__('knight', color, 3.0)

    def update_moves(self, game):
        ret = []
        col, row =  int(self.texture_rect[0]/SQSIZE), int(self.texture_rect[1]/SQSIZE)
        new_moves = []
        possibles = [(row-2,col+1), (row-2,col-1), (row+2,col+1), (row+2,col-1), (row+1,col+2),
        (row+1,col-2), (row-1,col+2), (row-1,col-2)]
        for tup in possibles:
            if tup[0] <=7 and tup[0] >= 0 and tup[1] <= 7 and tup[1] >= 0:
                cur_squ = game.board.squares[tup[0]][tup[1]]
                if cur_squ.piece is None:
                    new_moves.append(cur_squ)
                elif cur_squ.piece.color != self.color:
                    new_moves.append(cur_squ)
                else:
                    ret.append(cur_squ)
        self.moves = new_moves
        if self.color == 'white':
            c = 0
        if self.color == 'black':
            c = 1
        if len(game.checks[c]) > 0:
            self.check_moves(game,c)
            
        return ret

    def block(self, game, king_sq, cur_sq):
        pass

class Bishop(Piece):
    def __init__(self, color):
        super().__init__('bishop', color, 3.0)

    def update_moves(self, game):
        ret = []
        col, row =  int(self.texture_rect[0]/SQSIZE), int(self.texture_rect[1]/SQSIZE)
        col_temp = col
        row_temp = row
        new_moves = []
        iters = [(1,1), (1,-1), (-1,-1), (-1,1)]
        for i in iters:
            col_temp = col
            row_temp = row
            unblocked = True
            while unblocked:
                row_temp += i[0]
                col_temp += i[1]
                if row_temp > 7 or row_temp < 0 or col_temp < 0 or col_temp > 7:
                    unblocked = False
                else:
                    cur_squ = game.board.squares[row_temp][col_temp]
                    if cur_squ.piece is None:
                        new_moves.append(cur_squ)
                    elif cur_squ.piece.color != self.color:
                        new_moves.append(cur_squ)
                        unblocked = False
                    else:
                        ret.append(cur_squ)
                        unblocked = False
        self.moves = new_moves
        if self.color == 'white':
            c = 0
        if self.color == 'black':
            c = 1
        if len(game.checks[c]) > 0:
            self.check_moves(game,c)
            
        return ret

    def block(self, game, king_sq, cur_sq):
        blocks = []
        if king_sq in self.moves:
            row, col = cur_sq.row, cur_sq.col
            krow, kcol = king_sq.row, king_sq.col
            i = [0,0]
            if row > krow:
                i[0]-=1
            else:
                i[0]+=1
            if col > kcol:
                i[1]-=1
            else:
                i[1]+=1
            while True:
                row += i[0]
                col += i[1]
                cur_sq = game.board.squares[row][col]
                if cur_sq == king_sq:
                    break
                else:
                    blocks.append(cur_sq)
        self.blockable = blocks


class Rook(Piece):
    def __init__(self, color):
        super().__init__('rook', color, 5.0)

    def update_moves(self, game):
        ret = []
        col, row =  int(self.texture_rect[0]/SQSIZE), int(self.texture_rect[1]/SQSIZE)
        col_temp = col
        row_temp = row
        new_moves = []
        iters = [(1,0), (-1,0), (0,-1), (0,1)]
        for i in iters:
            col_temp = col
            row_temp = row
            unblocked = True
            while unblocked:
                row_temp += i[0]
                col_temp += i[1]
                if row_temp > 7 or row_temp < 0 or col_temp < 0 or col_temp > 7:
                    unblocked = False
                else:
                    cur_squ = game.board.squares[row_temp][col_temp]
                    if cur_squ.piece is None:
                        new_moves.append(cur_squ)
                    elif cur_squ.piece.color != self.color:
                        new_moves.append(cur_squ)
                        unblocked = False
                    else:
                        ret.append(cur_squ)
                        unblocked = False
        self.moves = new_moves
        if self.color == 'white':
            c = 0
        if self.color == 'black':
            c = 1
        if len(game.checks[c]) > 0:
            self.check_moves(game,c)
            
        return ret

    def block(self, game, king_sq, cur_sq):
        blocks = []
        if king_sq in self.moves:
            col, row = cur_sq.row, cur_sq.col
            krow, kcol = king_sq.row, king_sq.col
            if row == krow:
                if col < kcol:
                    temp = kcol
                    while temp > col:
                        temp -= 1
                        blocks.append(game.board.squares[row][temp])
                if col > kcol:
                    temp = kcol
                    while temp < col:
                        temp += 1
                        blocks.append(game.board.squares[row][temp])
            if col == kcol:
                if row < krow:
                    temp = krow
                    while temp > row:
                        temp -=1
                        blocks.append(game.board.squares[row][temp])
                if row > krow:
                    temp = krow
                    while temp < row:
                        temp +=1
                        blocks.append(game.board.squares[row][temp])
        self.blockable = blocks

class Queen(Piece):
    def __init__(self, color):
        super().__init__('queen', color, 9.0)

    def update_moves(self, game):
        ret = []
        col, row =  int(self.texture_rect[0]/SQSIZE), int(self.texture_rect[1]/SQSIZE)
        col_temp = col
        row_temp = row
        new_moves = []
        iters = [(1,1), (1,-1), (-1,-1), (-1,1), (1,0), (-1,0), (0,-1), (0,1)]
        for i in iters:
            col_temp = col
            row_temp = row
            unblocked = True
            while unblocked:
                row_temp += i[0]
                col_temp += i[1]
                if row_temp > 7 or row_temp < 0 or col_temp < 0 or col_temp > 7:
                    unblocked = False
                else:
                    cur_squ = game.board.squares[row_temp][col_temp]
                    if cur_squ.piece is None:
                        new_moves.append(cur_squ)
                    elif cur_squ.piece.color != self.color:
                        new_moves.append(cur_squ)
                        unblocked = False
                    else:
                        ret.append(cur_squ)
                        unblocked = False
        self.moves = new_moves
        if self.color == 'white':
            c = 0
        if self.color == 'black':
            c = 1
        if len(game.checks[c]) > 0:
            self.check_moves(game,c)
            
        return ret

    def block(self, game, king_sq, cur_sq):
        blocks = []
        if king_sq in self.moves:
            row, col = cur_sq.row, cur_sq.col
            krow, kcol = king_sq.row, king_sq.col
            if row == krow:
                if col < kcol:
                    temp = kcol
                    while temp > col:
                        temp -= 1
                        blocks.append(game.board.squares[row][temp])
                if col > kcol:
                    temp = kcol
                    while temp < col:
                        temp += 1
                        blocks.append(game.board.squares[row][temp])
            if col == kcol:
                if row < krow:
                    temp = krow
                    while temp > row:
                        temp -=1
                        blocks.append(game.board.squares[row][temp])
                if row > krow:
                    temp = krow
                    while temp < row:
                        temp +=1
                        blocks.append(game.board.squares[row][temp])
            if len(blocks)==0:
                row, col = cur_sq.row, cur_sq.col
                krow, kcol = king_sq.row, king_sq.col
                i = [0,0]
                if row > krow:
                    i[0]-=1
                else:
                    i[0]+=1
                if col > kcol:
                    i[1]-=1
                else:
                    i[1]+=1
                while True:
                    row += i[0]
                    col += i[1]
                    
                    cur_sq = game.board.squares[row][col]
                    if cur_sq == king_sq:
                        break
                    else:
                        blocks.append(cur_sq)
        self.blockable = blocks
        


class King(Piece):
    def __init__(self, color):
        super().__init__('king', color, 1.0)

    def update_moves(self, game):
        ret = []
        col, row =  int(self.texture_rect[0]/SQSIZE), int(self.texture_rect[1]/SQSIZE)
        col_temp = col
        row_temp = row
        new_moves = []
        iters = [(1,1), (1,-1), (-1,-1), (-1,1), (1,0), (-1,0), (0,-1), (0,1)]
        if self.color == 'white':
            for i in iters:
                col_temp = col
                row_temp = row
                unblocked = True
                while unblocked:
                    row_temp += i[0]
                    col_temp += i[1]
                    if row_temp > 7 or row_temp < 0 or col_temp < 0 or col_temp > 7:
                        unblocked = False
                    elif row_temp > row + 1 or col_temp > col + 1 or row_temp < row - 1 or col_temp < col - 1:
                        unblocked = False
                    else:
                        cur_squ = game.board.squares[row_temp][col_temp]
                        if cur_squ.piece is None:
                            '''for i in game.black_moves:
                                if i.row != 0:
                                    if game.board.squares[i.row-1][i.col] == 'pawn' and game.black_moves.count(i) == 1:
                                        new_moves.append(cur_squ)'''
                            if cur_squ not in game.black_moves:
                                new_moves.append(cur_squ)
                        elif cur_squ.piece.color != self.color and cur_squ not in game.black_moves:
                            new_moves.append(cur_squ)
                            unblocked = False
                        else:
                            ret.append(cur_squ)
                            unblocked = False
        if self.color == 'black':
            for i in iters:
                col_temp = col
                row_temp = row
                unblocked = True
                while unblocked:
                    row_temp += i[0]
                    col_temp += i[1]
                    if row_temp > 7 or row_temp < 0 or col_temp < 0 or col_temp > 7:
                        unblocked = False
                    elif row_temp > row + 1 or col_temp > col + 1 or row_temp < row - 1 or col_temp < col - 1:
                        unblocked = False
                    else:
                        cur_squ = game.board.squares[row_temp][col_temp]
                        if cur_squ.piece is None:
                            '''for j in game.white_moves:
                                if j.row != 7:
                                    if game.board.squares[j.row+1][j.col] == 'pawn' and game.white_moves.count(j) == 1:
                                        new_moves.append(cur_squ)'''
                            if cur_squ not in game.white_moves:
                                new_moves.append(cur_squ)
                        elif cur_squ.piece.color != self.color and cur_squ not in game.white_moves:
                            new_moves.append(cur_squ)
                            unblocked = False
                        else:
                            ret.append(cur_squ)
                            unblocked = False
        self.moves = new_moves
        return ret

    def block(self, game, k, cur_sq):
        pass
        