import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import optim
import matplotlib.pyplot as plt


#hyper parameters
EPSILON = 0.99
GAMMA = 0.9
LR = 0.01
MEMORY_CAPACITY = 500
Q_NETWORK_ITERATION = 100
BATCH_SIZE = 32

EPISODES = 1000




class Net(nn.Module):
    def __init__(self, minv = -10, maxv = 10, n_states = 5, n_actions = 3):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(n_states, 30)
        self.fc1.weight.data.normal_(0, 0.1)
        self.fc2 = nn.Linear(30, n_actions)
        self.fc2.weight.data.normal_(0, 0.1)
        self.min_velocity, self.max_velocity = minv, maxv

    def forward(self, x):
        x = self.fc1(x)
        x = F.relu(x)
        return self.fc2(x)


class Dqn():
    def __init__(self, minv = -10, maxv = 10, n_states = 5):
        self.eval_net, self.target_net = Net(minv, maxv), Net(minv, maxv)
        self.NUM_STATES = n_states
        self.memory = np.zeros((MEMORY_CAPACITY, self.NUM_STATES *2 +2))
        # state, action ,reward and next state
        self.memory_counter = 0
        self.learn_counter = 0
        self.optimizer = optim.Adam(self.eval_net.parameters(), LR)
        self.loss = nn.MSELoss()
        self.fig, self.ax = plt.subplots()

    def store_trans(self, state, action, reward, next_state):
        if self.memory_counter % 500 ==0:
            # print(f"The experience pool collects {self.memory_counter} time experience")
            pass
        index = self.memory_counter % MEMORY_CAPACITY
        trans = np.hstack((state, action, [reward], next_state))
        self.memory[index,] = trans
        self.memory_counter += 1

    def choose_action(self, state, env):
        # notation that the function return the action's index nor the real action
        # EPSILON
        state = torch.unsqueeze(torch.FloatTensor(state) ,0)
        if np.random.randn() <= EPSILON:
            action_value = self.eval_net.forward(state)
            N = torch.max(action_value, 1)[1].data.numpy() # get action whose q is max

            discrete_action = N[0] #get the action index
            # print("1: ", discrete_action)
        else:
            discrete_action = env.action_space.sample()

            # print("2: ", discrete_action)
        return discrete_action 

    def plot(self, ax, x):
        ax.cla()
        ax.set_xlabel("episode")
        ax.set_ylabel("total reward")
        ax.plot(x, 'b-')
        plt.pause(0.000000000000001)

    def learn(self):
        # learn 100 times then the target network update
        if self.learn_counter % Q_NETWORK_ITERATION ==0:
            self.target_net.load_state_dict(self.eval_net.state_dict())
        self.learn_counter+=1

        sample_index = np.random.choice(MEMORY_CAPACITY, BATCH_SIZE)
        batch_memory = self.memory[sample_index, :]
        batch_state = torch.FloatTensor(batch_memory[:, :self.NUM_STATES])

        batch_action = torch.LongTensor(batch_memory[:, self.NUM_STATES:self.NUM_STATES+1])
        batch_reward = torch.FloatTensor(batch_memory[:, self.NUM_STATES+1: self.NUM_STATES+2])
        batch_next_state = torch.FloatTensor(batch_memory[:, -self.NUM_STATES:])
        
        q_eval = self.eval_net(batch_state)
        q_next = self.target_net(batch_next_state).detach()
        q_target = batch_reward + GAMMA*q_next

        self.optimizer.zero_grad()
        q_eval.requires_grad_()
        loss = self.loss(q_eval, q_target)
        loss.backward()
        self.optimizer.step()
        