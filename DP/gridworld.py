import gym
import numpy as np
from gym import spaces

# custom 2d grid world enviroment which extends gym.Env
class GridWorld(gym.Env):
    """
        A grid world env follows the book Example 4.1
    """
    metadata = {'render.modes': ['console']}
    
    # actions available 
    UP   = 0
    LEFT = 1
    DOWN = 2
    RIGHT= 3
    
    def __init__(self, size):
        super(GridWorld, self).__init__()
        
        self.size = size # size of the grid world
        self.end_state = [[0,0],[size-1,size-1]] # top left and bottom right
        
        # randomly assign the inital location of agent
        self.agent_position = [np.random.randint(0,self.size),np.random.randint(0,self.size)]
        
        # respective actions of agents : up, down, left and right
        self.action_space = spaces.Discrete(4)
        
        # set the observation space to (1,) to represent agent position in the grid world 
        # staring from [0,size*size)
        self.observation_space = spaces.Box(low=0, high=4, shape=(2,), dtype=np.uint8)
        
        self.states = [[i,j] for i in range(size) for j in range(size)]
    
    def bound_position(self):
        self.agent_position[0] = 0 if self.agent_position[0]<0 else self.agent_position[0]
        self.agent_position[0] = self.size-1 if self.agent_position[0]>self.size-1 else self.agent_position[0]
        self.agent_position[1] = 0 if self.agent_position[1]<0 else self.agent_position[1]
        self.agent_position[1] = self.size-1 if self.agent_position[1]>self.size-1 else self.agent_position[1]
        
    def step(self,action):
        info = {} # additional information
        
        if self.agent_position in self.end_state:
            return self.agent_position, 0, True, info
        
        
        if action == self.UP:
            self.agent_position[0] -=1

        elif action == self.LEFT:
            self.agent_position[1] -=1

        elif action == self.DOWN:
            self.agent_position[0] +=1

        elif action == self.RIGHT:
            self.agent_position[1] +=1

        else:
            raise ValueError("Received invalid action={} which is not part of the action space".format(action))
        
        self.bound_position()
        done = bool(self.agent_position in self.end_state)
        
        # reward agent when it is in the terminal cell, else reward = 0
        reward = 0 if done else -1
        
        return self.agent_position, reward, done, info
    
    def render(self, mode='console'):
        '''
            render the state
        '''
        if mode != 'console':
          raise NotImplementedError()
        
        row  = self.agent_position[0]
        col  = self.agent_position[1]
        
        for r in range(self.size):
            for c in range(self.size):
                if r == row and c == col:
                    print("X",end='')
                else:
                    print('.',end='')
            print('')

    def reset(self,position):
        
        self.agent_position = position
    
    def close(self):
        pass