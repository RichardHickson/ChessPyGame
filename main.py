import pygame

from constants import *
from game import Game
from pieces import *

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = Game()
    
    def loop(self):
        self.game.show_squares(self.screen)
        self.game.show_pieces(self.screen)
        pieceActive = False
        cur_turn = 'white'
        while True:
            #self.game.show_pieces(self.screen)
            #self.game.board
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos_arr = self.game.get_positions()
                    if pieceActive == True:
                        for sq in cur_piece.moves:
                            if sq.rect.collidepoint(event.pos):
                                if cur_piece.name == 'pawn' and sq.piece == None and sq.col != cur_sq.col:
                                    self.game.last_move.piece = None
                                if cur_piece.name == 'pawn' and (sq.row == 7 or sq.row == 0):
                                    sq.fresh_piece('queen',cur_piece.color)
                                else:
                                    sq.fresh_piece(cur_piece.name,cur_piece.color)
                                cur_sq.piece = None
                                if cur_turn == 'white':
                                    cur_turn = 'black'
                                else:
                                    cur_turn = 'white'
                                self.game.last_move = sq
                        self.game.show_pieces(self.screen)
                        pieceActive = False
                        pieceFound = False
                    elif pieceActive == False:
                        #pos_arr = self.game.get_positions()
                        #if event.button == 1:
                        pieceFound = False
                        for posi in pos_arr:
                            if posi[0].collidepoint(event.pos) and len(posi[1].moves) != 0:
                                cur_piece = posi[1]
                                if cur_piece.color == cur_turn:
                                    cur_sq = posi[2]
                                    pieceFound = True
                                    pieceActive = True
                                    #cur_piece.update_moves(self.game)
                                    for sq in cur_piece.moves:
                                        sq.show_square(self.screen)                      
                    if pieceFound == False:
                        self.game.show_squares(self.screen)
                        self.game.show_pieces(self.screen)
                        pieceActive = False
                    pos_arr = self.game.get_positions()
                    self.game.king_check()
                    if len(self.game.valid_white) == 0:
                        if cur_turn == 'black':
                            print('stalemate!')
                        else:
                            print('black wins')
                    if len(self.game.valid_black) == 0:
                        if cur_turn == 'white':
                            print('stalemate!')
                        else:
                            print('black wins')
                        

            pygame.display.update()

main = Main()
main.loop()
