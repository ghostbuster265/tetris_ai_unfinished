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

global episode_n
episode_n = 1

class TetrisGame():
    def __init__(self,render=False):
        self.fps = 50
        self.figure = block(4,0)
        self.next_figure = block(4,0)
        self.get_new_figure = False
        self.filled = {}
        self.clock = pygame.time.Clock()
        self.done = False
        self.render = render
        self.reward = 0.0
        if self.render:
            self.screen = pygame.display.set_mode((s_width,s_height))
            pygame.display.set_caption('Tetris_RL')

    def string_to_positions(self,fig):
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

    def create_matrix(self,filled = {}):
        matrix = [[(0,0,0) for _ in range(10)] for _ in range(20)]

        for i in range(20):
            for j in range(10):
                if (j,i) in filled:
                    block_color = filled[(j,i)]
                    matrix[i][j] = block_color
        return matrix

    def draw_game_interface(self,surf,mat):
        surf.fill((0,0,0))

        for i in range(20):
            for j in range(10):
                pygame.draw.rect(surf, mat[i][j], (play_surface_x + j*block_size, play_surface_y + i*block_size, block_size,block_size),0)

        pygame.draw.rect(surf, (255,0,0), (play_surface_x, play_surface_y, play_width, play_height),5)
        for i in range(1,10):
                pygame.draw.line(surf,(128,128,128), (play_surface_x + i*block_size, play_surface_y), (play_surface_x + i*block_size, play_surface_y + play_height))
        for i in range(1,20):
            pygame.draw.line(surf,(128,128,128), (play_surface_x, play_surface_y + i*block_size), (play_surface_x + play_width, play_surface_y + i*block_size))

        font = pygame.font.Font(None, 40)
        episode = font.render('Episode: '+str(episode_n),1,(255,255,255))
        self.screen.blit(episode,(s_width/2 - episode.get_width()/2, 30))

    def free_position(self,fig,mat):
        free_positions = [[(j,i) for j in range(10) if mat[i][j] == (0,0,0)] for i in range(20)]
        free_positions = [pos for sub in free_positions for pos in sub]
        
        actual_position = self.string_to_positions(fig)

        for pos in actual_position:
            if pos not in free_positions:
                if pos[1] > -1:
                    return False
        return True

    def clear_rows(self,mat,filled):
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
            
            if cleared_rows==1:
                self.reward += 40
            elif cleared_rows==2:
                self.reward += 100
            elif cleared_rows==3:
                self.reward += 300
            else:
                self.reward += 1000

    def check_height(self,matrix):
        highest = 0
        for i in range(20):
            for j in range(10):
                if matrix[i][j] != (0,0,0):
                    highest = i
                    break
        if highest < 5:
            pass
        else:
            self.reward -= 10*highest

    def play(self,input):
        global episode_n
        self.reward = 0       
        matrix = self.create_matrix(self.filled)
                 
        if input[0] == 1:
            pass  
        elif input[1] == 1:
            self.figure.x -= 1
            if not (self.free_position(self.figure,matrix)):
                self.figure.x += 1
        elif input[2] == 1:
            self.figure.x += 1
            if not (self.free_position(self.figure,matrix)):
                self.figure.x -= 1
        elif input[3] == 1:
            self.figure.rotation += 1
            if not (self.free_position(self.figure,matrix)):
                self.figure.rotation -= 1

        self.figure.y += 1
        if not(self.free_position(self.figure,matrix)) and self.figure.y > 0:
            self.figure.y -= 1
            self.check_height(matrix)
            self.get_new_figure = True
        
        fig_pos = self.string_to_positions(self.figure)
        for i in range(len(fig_pos)):
            x,y = fig_pos[i]
            if y > -1:
                matrix[y][x] = self.figure.color

        if self.get_new_figure:
            for pos in fig_pos:
                p = (pos[0],pos[1])
                self.filled[p] = self.figure.color
            self.figure = self.next_figure
            self.next_figure = block(4,0)
            self.get_new_figure = False
            self.clear_rows(matrix,self.filled)

        if self.render:
            self.draw_game_interface(self.screen,matrix)
            pygame.display.update()
        
        self.clock.tick(self.fps)
        for pos in self.filled:
            if pos[1] < 0:
                self.reward -= 100
                if self.render:
                    font = pygame.font.Font(None, 200)
                    lost = font.render('YOU DIED',1,(255,0,0))
                    self.screen.blit(lost,(play_surface_x + play_width/2 - lost.get_width()/2, play_surface_y + play_height/2 - lost.get_height()/2))
                    self.done = True
                    pygame.display.update()
                    pygame.time.delay(800)
                    episode_n+=1
                    return matrix, self.reward, self.done
                else:
                    self.done = True
                    return matrix, self.reward, self.done
        if self.done == True and self.render == True:
            pygame.display.quit()
        return matrix, self.reward, self.done


# tetris = TetrisGame(render=True)
# tetris.play()