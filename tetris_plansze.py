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
        self.type = figures[6]
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

    while 0 not in [pos[1] for pos in positions]:
        positions = [(x,y-1) for x,y in iter(positions)]
    return positions

def create_matrix(fig, filled = {}):
    matrix = [[(0,0,0) for _ in range(10)] for _ in range(20)]

    for i in range(20):
        for j in range(10):
            if (j,i) in filled:
                block_color = filled[(j,i)]
                matrix[i][j] = block_color
    return plansza(fig,matrix)

def draw_game_interface(surf,mat):
    surf.fill((0,0,0))
    simple_env = [[int(bool(max(x))) for x in mat[i]] for i in range(20)]
    for row in simple_env: print(row)
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
    
    actual_position = string_to_positions(fig)

    for pos in actual_position:
        if pos not in free_positions:
            if pos[1] > -1:
                return False
    return True

def plansza(fig, matrix, loops = []):
    if loops == []:
        slot = random.randint(0,9)
        for i, line in enumerate(fig.type[fig.rotation % len(fig.type)],start=16):
            row = list(line)
            for j, num in enumerate(row):
                if num == '1':
                    loops.append((slot,i))

    while 16 not in [pos[1] for pos in loops]:
        loops = [(x,y-1) for x,y in iter(loops)]

    for i in range(16,20):
        for j in range(10):
            if (j,i) not in loops :
                matrix[i][j] = (255,255,255)
            else:
                pass
    return matrix

def game(actions = [-1,-1,-1,1,0,0,-1,1,1,1,1], render = False):
    fps = 3
    figure = block(4,0)
    filled = {}
    clock = pygame.time.Clock()
    running = True
    action_id = 0
    
    screen = pygame.display.set_mode((s_width,s_height))
    while running:
        matrix = create_matrix(figure, filled)
        figure.y += 5
        
        if not(free_position(figure,matrix)) and figure.y > 0:
            figure.y -= 1
            for pos in fig_pos:
                p = (pos[0],pos[1])
                filled[p] = figure.color

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running=False
            elif event.type == pygame.QUIT:
                running = False
        
        fig_pos = string_to_positions(figure)
        for i in range(len(fig_pos)):
            x,y = fig_pos[i]
            if y > -1:
                matrix[y][x] = figure.color
        
        if render: draw_game_interface(screen,matrix)
        
        try:
            print(actions[action_id])
            if actions[action_id] == -1:
                figure.x -= 1
                if not(free_position(figure,matrix)):
                    figure.x += 1
            elif actions[action_id] == 1:
                figure.x += 1
                if not(free_position(figure,matrix)):
                    figure.x -= 1
            action_id += 1
        except IndexError: pass

        pygame.display.update()
        clock.tick(fps)
        for pos in filled:
            if pos[1] < 16:
                font = pygame.font.Font(None, 200)
                lost = font.render('YOU DIED',1,(255,0,0))
                screen.blit(lost,(play_surface_x + play_width/2 - lost.get_width()/2, play_surface_y + play_height/2 - lost.get_height()/2))
                running = False
                pygame.display.update()
                pygame.time.delay(500)
                return (-1)
            else:
                font = pygame.font.Font(None, 200)
                lost = font.render('GOOD JOB',1,(0,255,0))
                screen.blit(lost,(play_surface_x + play_width/2 - lost.get_width()/2, play_surface_y + play_height/2 - lost.get_height()/2))
                running = False
                pygame.display.update()
                pygame.time.delay(500)
                return (1)
        
    pygame.display.quit()
game(render = True)