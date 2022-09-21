import numpy as np

from exploration.epsilon_greedy import EpsilonGreedy

class SARSAagent:
    def __init__(self, starting_state, state_space, action_space, gamma=0.95, learning_rate=0.01, exploration_strategy=EpsilonGreedy()):
        self.state = starting_state
        self.state_space = state_space
        self.action_space = action_space
        self.action = None
        self.gamma = gamma
        self.learning_rate = learning_rate
        self.q_table = {self.state: [0 for _ in range(action_space.n)]}
        self.exploration = exploration_strategy
        self.new_state = None
        self.new_action = None
        self.acc_reward = 0

    def first_act(self):
        self.action = self.exploration.choose(self.q_table[self.state], self.action_space)
        return self.action

    def act(self):
        self.new_action = self.exploration.choose(self.q_table[self.state], self.action_space)
        return self.new_action

    def learn(self, new_state, reward, done=False):

        self.new_state = new_state

        if self.new_state not in self.q_table:
            self.q_table[self.new_state] = [0 for _ in range(self.action_space.n)]

        if done:

            deltaQ = (reward + 0 - self.q_table[self.state][self.action])

        else:

            deltaQ = (reward + self.gamma * self.q_table[self.new_state][self.new_action] - self.q_table[self.state][self.action])

        self.q_table[self.state][self.action] += self.learning_rate * deltaQ

        self.state = self.new_state
        self.action = self.new_action