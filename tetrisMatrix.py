import pygame
import random

pygame.init()

s_width = 900
s_height = 800
play_width = 300
play_height = 600
block_size = 30

play_surface_x = (s_width - play_width)//2
play_surface_y = s_height - play_height - 50

figures = [
    #S
    [['011',
      '110',
      '000'],
     ['010',
      '011',
      '001'],
     ['000',
      '011',
      '110'],
     ['100',
      '110',
      '010']],
    #Z
    [['110',
      '011',
      '000'],
     ['001',
      '011',
      '010'],
     ['000',
      '110',
      '011'],
     ['010',
      '110',
      '100']],
    #L
    [['001',
      '111',
      '000'],
     ['010',
      '010',
      '011'],
     ['000',
      '111',
      '100'],
     ['110',
      '010',
      '010']],
    #J
    [['100',
      '111',
      '000'],
     ['011',
      '010',
      '010'],
     ['000',
      '111',
      '001'],
     ['010',
      '010',
      '110']],
    #O
    [['110',
      '110',
      '000']],
    #T
    [['010',
      '111',
      '000'],
     ['010',
      '011',
      '010'],
     ['000',
      '111',
      '010'],
     ['010',
      '110',
      '010']],
    #I
    [['0010',
      '0010',
      '0010',
      '0010'],
     ['0000',
      '0000',
      '1111',
      '0000'],
     ['0100',
      '0100',
      '0100',
      '0100'],
     ['0000',
      '1111',
      '0000',
      '0000']]]

colors = [(0,255,0),(255,0,0),(255,165,0),(0,0,255),(250,242,13),(255,0,255),(0,255,255)]

class block():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.type = random.choice(figures)
        self.color = colors[figures.index(self.type)]
        self.rotation = 0

def string_to_positions(fig):
    positions = []
    string = fig.type[fig.rotation % len(fig.type)]

    for i, line in enumerate(string):
        row = list(line)
        for j, num in enumerate(row):
            if num == '1':
                positions.append((fig.x + j, fig.y + i))
    for i,pos in enumerate(positions):
        positions[i] = (pos[0],pos[1]-2)
    return positions

def create_matrix(filled = {}):
    matrix = [[(0,0,0) for _ in range(10)] for _ in range(20)]

    for i in range(20):
        for j in range(10):
            if (j,i) in filled:
                block_color = filled[(j,i)]
                matrix[i][j] = block_color
    return matrix

def draw_game_interface(surf,mat):
    surf.fill((0,0,0))

    for i in range(20):
        for j in range(10):
            pygame.draw.rect(surf, mat[i][j], (play_surface_x + j*block_size, play_surface_y + i*block_size, block_size,block_size),0)

    pygame.draw.rect(surf, (255,0,0), (play_surface_x, play_surface_y, play_width, play_height),5)
    for i in range(1,10):
            pygame.draw.line(surf,(128,128,128), (play_surface_x + i*block_size, play_surface_y), (play_surface_x + i*block_size, play_surface_y + play_height))
    for i in range(1,20):
        pygame.draw.line(surf,(128,128,128), (play_surface_x, play_surface_y + i*block_size), (play_surface_x + play_width, play_surface_y + i*block_size))

def free_position(fig,mat):
    free_positions = [[(j,i) for j in range(10) if mat[i][j] == (0,0,0)] for i in range(20)]
    free_positions = [pos for sub in free_positions for pos in sub]
    
    actual_position = string_to_positions(figure)

    for pos in actual_position:
        if pos not in free_positions:
            if pos[1] > -1:
                return False
    return True

def clear_rows(mat,filled):
    cleared_rows = 0
    for i in range(19,-1,-1):
        row = mat[i]
        if (0,0,0) not in row:
            cleared_rows += 1
            shift_index = i
            for j in range(10):
                if (j,i) in filled:
                    del filled[(j,i)]
    
    if cleared_rows > 0:
        for key in sorted(list(filled), key=lambda x:x[1],reverse=True):
            x,y = key
            if y < shift_index:
                new_key = (x, y + cleared_rows)
                filled[new_key] = filled.pop(key)

fps = 5
figure = block(4,0)
next_figure = block(4,0)
get_new_figure = False
filled = {}
clock = pygame.time.Clock()
running = True
screen = pygame.display.set_mode((s_width,s_height))
while running:
    matrix = create_matrix(filled)
    
    figure.y += 1
    if not(free_position(figure,matrix)) and figure.y > 0:
        figure.y -= 1
        get_new_figure = True
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running=False
            elif event.key == pygame.K_UP:
                figure.rotation += 1
                if not (free_position(figure,matrix)):
                    figure.rotation -=1
            elif event.key == pygame.K_DOWN:
                figure.y += 1
                if not (free_position(figure,matrix)):
                    figure.y -= 1
            elif event.key == pygame.K_RIGHT:
                figure.x += 1
                if not (free_position(figure,matrix)):
                    figure.x -= 1
            elif event.key == pygame.K_LEFT:
                figure.x -= 1
                if not (free_position(figure,matrix)):
                    figure.x += 1
        elif event.type == pygame.QUIT:
            running = False
    
    fig_pos = string_to_positions(figure)
    for i in range(len(fig_pos)):
        x,y = fig_pos[i]
        if y > -1:
            matrix[y][x] = figure.color
    
    if get_new_figure:
        for pos in fig_pos:
            p = (pos[0],pos[1])
            filled[p] = figure.color
        figure = next_figure
        next_figure = block(4,0)
        get_new_figure = False
        clear_rows(matrix,filled)
    
    draw_game_interface(screen,matrix)
    
    pygame.display.update()
    clock.tick(fps)
    for pos in filled:
        if pos[1] < 0:
            font = pygame.font.Font(None, 200)
            lost = font.render('YOU DIED',1,(255,0,0))
            screen.blit(lost,(play_surface_x + play_width/2 - lost.get_width()/2, play_surface_y + play_height/2 - lost.get_height()/2))
            running = False
            pygame.display.update()
            pygame.time.delay(1500)
pygame.display.quit()