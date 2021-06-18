import gym
from gym import spaces, logger
from gym.utils import seeding
import numpy as np
import tetrisMatrix_RL

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, Input, Conv2D, MaxPooling2D

from rl.agents.cem import CEMAgent
from rl.memory import EpisodeParameterMemory

class TetrisEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self,render=False):
        super(TetrisEnv, self).__init__()
        self.render_ = render
        self.game_state = tetrisMatrix_RL.TetrisGame(render=render)
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=0,high=255,shape=(20,10,3))

    def step(self, action):
        self.action_set = np.zeros([4])
        self.action_set[action] = 1
        reward = 0.0
        state, reward, done = self.game_state.play(input=self.action_set)

        return state, reward, done,{}

    def reset(self):
        self.game_state = tetrisMatrix_RL.TetrisGame(render=self.render_)
        hold = np.zeros([4])
        hold[0] = 1
        self.observation_space = spaces.Box(low=0,high=255,shape=(20,10,3))
        state, _, _ = self.game_state.play(hold)

        return state

    def close(self):
        pass

env = TetrisEnv(render=True)

model = Sequential()
model.add(Flatten(input_shape=(1,) + (20,10,3)))
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dense(32))
model.add(Activation('relu')) 
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(8))
model.add(Activation('relu'))
model.add(Dense(4))
model.add(Activation('softmax'))
print(model.summary())
# model = Sequential()
# model.add(Input(shape=(1,) + (20,10,3)))
# model.add(Conv2D(32,kernel_size=(3,3),activation='relu',))
# model.add(MaxPooling2D(pool_size=(2,2)))
# model.add(Conv2D(64,kernel_size=(3,3),activation='relu'))
# model.add(MaxPooling2D(pool_size=(2,2)))
# model.add(Flatten(input_shape=(1,) + (20,10,3)))
# model.add(Dense(512))
# model.add(Activation('relu'))
# model.add(Dense(256))
# model.add(Activation('relu'))
# model.add(Dense(16))
# model.add(Activation('relu'))
# model.add(Dense(8))
# model.add(Activation('relu'))
# # model.add(Dropout(0.5))
# # model.add(Activation('relu'))
# model.add(Dense(4))
# model.add(Activation('softmax'))

memory = EpisodeParameterMemory(limit=1000, window_length=1)

cem = CEMAgent(model=model, nb_actions=4, memory=memory,
               batch_size=50, nb_steps_warmup=2000, train_interval=50, elite_frac=0.05)
cem.compile()
cem.fit(env, nb_steps=100000, visualize=False, verbose=2)

cem.save_weights('cem_TetrisEnv_params.h5f', overwrite=True)

cem.test(env, nb_episodes=10)
