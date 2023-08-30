import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

def draw_board():
    screen.fill((255,255,255))
    size_width, size_height = SCREEN_WIDTH/8,SCREEN_HEIGHT/8
    color = (0,255,0)
    for i in range(0,8,2):
        for j in range(1,9,2):
            pygame.draw.rect(screen,color,pygame.Rect(0+size_width*j,0+size_height*i,size_width,size_height))
    for i in range(1,9,2):
        for j in range(0,8,2):
            pygame.draw.rect(screen,color,pygame.Rect(0+size_width*j,0+size_height*i,size_width,size_height))

draw_board()


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
pygame.quit()
