import random
import pandas as pd
import numpy as np
import tensorflow as tf
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
        self.rotation = 0
        self.color = colors[figures.index(self.type)]

def string_to_positions(fig, slot):
    positions = []
    string = fig.type[fig.rotation % len(fig.type)]

    for i, line in enumerate(string):
        row = list(line)
        for _, num in enumerate(row):
            if num == '1':
                positions.append((slot, fig.y + i))

    while 0 not in [pos[1] for pos in positions]:
        positions = [(x,y-1) for x,y in iter(positions)]
    return positions

def plansza(fig, slot, shift, loops = []):
    matrix = [[(0,0,0) for _ in range(10)] for _ in range(20)]
    if loops == []:
        for i, line in enumerate(fig.type[fig.rotation % len(fig.type)],start=16):
            row = list(line)
            for j, num in enumerate(row):
                if num == '1':
                    loops.append((slot,i))
    else: pass

    while 16 not in [pos[1] for pos in loops]:
        loops = [(x,y-1) for x,y in iter(loops)]

    for i in range(16,20):
        for j in range(10):
            if (j,i) not in loops :
                matrix[i][j] = (128,128,128) #[czy wolne miejsce, czy aktualna figura]
            else:
                pass

    fig_pos = string_to_positions(fig,slot)
    # if slot == 0: shift = random.randint(0,1)
    # elif slot == 9: shift = random.randint(-1,0)
    # else: shift = random.randint(-1,1)
    fig_pos = [(pos[0] + shift,pos[1]) for pos in fig_pos]
    
    for i in range(20):
        for j in range(10):
            if (j,i) in fig_pos:
                matrix[i][j] = fig.color

    if fig_pos[0][0] > slot: answer = -1
    elif fig_pos[0][0] < slot: answer = 1
    else: answer = 0

    return matrix, fig_pos, answer

def data(n):
    # dane = {'matrix':[],'answer':[]}
    # for _ in range(n):
    #     matrix, figure_blocks, answer = plansza(block(4,0))
    #     matrix = [num for row in matrix for num in row]
    #     # figure_blocks = [num for pos in figure_blocks for num in pos]
    #     dane['matrix'].append(matrix)
    #     # dane['figure_blocks'].append(figure_blocks)
    #     dane['answer'].append(answer)
    # dane['matrix']=dane['matrix'][0]
    # dane = dane.copy()
    # labels = dane.pop('answer')
    # ds = tf.data.Dataset.from_tensor_slices((dict(dane),labels))
    # ds = ds.shuffle(buffer_size = len(dane))
    
    m = []
    # f = []
    a = []
    for _ in range(n):
        for slot in range(10):
            if slot == 0:
                for shift in [0,1]:
                    matrix, figure_blocks, answer = plansza(block(4,0),slot=slot,shift=shift)
                    m.append(matrix)
                    # f.append(figure_blocks)
                    a.append([answer])
            elif slot==9:
                for shift in [-1,0]:
                    matrix, figure_blocks, answer = plansza(block(4,0),slot=slot,shift=shift)
                    m.append(matrix)
                    # f.append(figure_blocks)
                    a.append([answer])
            else:
                for shift in [-1,0,1]:
                    matrix, figure_blocks, answer = plansza(block(4,0),slot=slot,shift=shift)
                    m.append(matrix)
                    # f.append(figure_blocks)
                    a.append([answer])

    m=np.asarray(m)
    a=np.asarray(a)
    m=m.astype('float32')
    a=a.astype('float32')
    return m,a

#m,a = data(1)
# for row in m[0]: print(row)
#print(m.shape)
