import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense
import tensorflow as tf

from exploration.epsilon_greedy import EpsilonGreedy

class SarsaANNagent:
    def __init__(self, starting_state, state_space, action_space, gamma=0.95, learning_rate=0.01, exploration_strategy=EpsilonGreedy()):
        self.state = starting_state
        self.state_space = state_space
        self.action_space = action_space
        self.action = None
        self.gamma = gamma
        self.learning_rate = learning_rate
        self.exploration = exploration_strategy
        self.new_state = None
        self.new_action = None
        self.acc_reward = 0
        SGD = tf.keras.optimizers.SGD(learning_rate=learning_rate)

        s = np.asarray(self.state).reshape(1, len(self.state))
        self.Q_NN = []

        for a in range(self.action_space.n):
            NN = Sequential()
            NN.add(Dense(20, activation='relu'))
            NN.add(Dense(20, activation='relu'))
            NN.add(Dense(1, activation='linear'))
            # "Construct" the NN with all the internal structure needed for calculations and updates..
            NN.compile(loss='MSE', optimizer=SGD)
            self.Q_NN.append(NN)

    def first_act(self):
        s = np.asarray(self.state).reshape(1, len(self.state))
        Qvalue_approx = np.array([self.Q_NN[a](s) for a in range(self.action_space.n)]).flatten()
        self.action = self.exploration.choose(Qvalue_approx, self.action_space)
        return self.action

    def act(self):
        s = np.asarray(self.state).reshape(1, len(self.state))
        Qvalue_approx = np.array([self.Q_NN[a](s) for a in range(self.action_space.n)]).flatten()
        self.new_action = self.exploration.choose(Qvalue_approx, self.action_space)
        return self.new_action

    def learn(self, new_state, reward, done=False):

        self.new_state = new_state

        s = np.asarray(self.state).reshape(1, len(self.state))
        new_s = np.asarray(self.new_state).reshape(1, len(self.new_state))
        new_Q_approx = self.Q_NN[self.new_action](new_s)

        if done:

            target = reward

        else:

            target = reward + self.gamma * new_Q_approx

        target = np.array(target).reshape(1,1)

        self.Q_NN[self.action].fit(s, target, verbose=0)

        self.state = self.new_state
        self.action = self.new_action