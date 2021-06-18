from gym import Env
from gym.spaces import Discrete, Box
import numpy as np
import random
from keras.models import Sequential
from keras.layers import Flatten, Dense
from keras.optimizers import Adam
from rl.agents import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

class cenv(Env):
    def __init__(self):
        self.action_space = Discrete(3)
        self.observation_space = Box(low=np.array([0]),high = np.array([100]))
        self.state = 38+random.randint(-3,3)
        self.shower_length = 60

    def step(self,action):
        self.state += action -1
        self.shower_length -= 1

        if self.state >= 37 and self.state<= 39:
            reward = 1
        else:
            reward = -1

        if self.shower_length <= 0:
            done = True
        else:
            done = False
        
        self.state += random.randint(-1,1)

        info = {}

        return self.state, reward, done, info

    def render(self):
        pass
    def reset(self):
        self.state = 38 + random.randint(-3,3)
        self.shower_length = 60
        return self.state

def b_model(states,actions):
    model = Sequential()
    model.add(Dense(24,activation='relu',input_shape=states))
    model.add(Dense(24,activation='relu'))
    model.add(Dense(actions,activation='linear'))
    return model

def b_agent(model,actions):
    policy = BoltzmannQPolicy()
    memory = SequentialMemory(limit=50000, window_length = 1)
    dqn = DQNAgent(model=model,memory = memory, policy = policy, nb_actions= actions, nb_steps_warmup=100, target_model_update=1e-2)
    return dqn

env = cenv()
print(env.observation_space.sample())
episodes = 10
for episode in range(1,episodes+1):
    state= env.reset()
    done =False
    score = 0 
    while not done:
        action = env.action_space.sample()
        n_state, reward, done, info = env.step(action)
        score += reward
    print('Episode:{} Score:{}'.format(episode,score))

states = env.observation_space.shape
actions = env.action_space.n

model = b_model(states,actions)
print(model.summary())
dqn = b_agent(model,actions)
dqn.compile(Adam(lr=1e-3), metrics=['mae'])
dqn.fit(env,nb_steps=100000,visualize=False,verbose=1)