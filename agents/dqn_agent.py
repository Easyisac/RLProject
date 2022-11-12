import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, Model
from collections import deque
import random
from exploration.epsilon_greedy import EpsilonGreedy


class DQNAgent:

    def __init__(self, starting_state, state_space, action_space, learning_rate=0.01, gamma=0.95, exploration_strategy=EpsilonGreedy()):
        self.state = starting_state
        self.state_space = state_space
        self.action_space = action_space
        self.action = None
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.exploration = exploration_strategy
        self.MIN_REPLAY_SIZE = 128
        self.acc_reward = 0

        self.model = self.network()
        self.target_model = self.network()
        self.target_model.set_weights(self.model.get_weights())

        self.replay_memory = deque(maxlen=10000)

    def get_lr_metric(self, optimizer):
        def lr(y_true, y_pred):
            return optimizer._decayed_lr(tf.float32)
        return lr


    def network(self):
        learning_rate = 0.00005
        # steps = 10000
        # rate = 0.96
        # staircase = True
        # schedule = tf.keras.optimizers.schedules.ExponentialDecay(
        #     learning_rate, steps, rate, staircase
        # )
        optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
        # lr_metric = self.get_lr_metric(optimizer)
        initializer = tf.keras.initializers.HeUniform()


        model = keras.Sequential()
        model.add(keras.layers.Dense(36, input_shape=self.state_space.shape, activation='relu', kernel_initializer=initializer))
        #model.add(keras.layers.Dense(24, activation='relu', kernel_initializer=initializer))
        #model.add(keras.layers.Dense(20, activation='relu', kernel_initializer=initializer))
        model.add(keras.layers.Dense(self.action_space.n, activation='linear', kernel_initializer=initializer))
        model.compile(loss=tf.keras.losses.Huber(), optimizer=optimizer, metrics=['accuracy'])
        return model

    def act(self):
        s = np.asarray(self.state).reshape(1, len(self.state))
        self.action = self.exploration.choose(self.model.predict(s), self.action_space)
        return self.action

    def learn(self):

        if len(self.replay_memory) < self.MIN_REPLAY_SIZE:
            return

        batch_size = 64 * 2
        mini_batch = random.sample(self.replay_memory, batch_size)
        current_states = np.array([transition[0] for transition in mini_batch])
        current_qs_list = self.model.predict(current_states)
        new_current_states = np.array([transition[3] for transition in mini_batch])
        future_qs_list = self.target_model.predict(new_current_states)

        X = []
        Y = []

        for index, (observation, action, reward, new_observation, done) in enumerate(mini_batch):
            if not done:
                max_future_q = reward + self.gamma * np.max(future_qs_list[index])
            else:
                max_future_q = reward

            current_qs = current_qs_list[index]
            current_qs[action] = (1 - self.learning_rate) * current_qs[action] + self.learning_rate * max_future_q

            X.append(observation)
            Y.append(current_qs)

        self.model.fit(np.array(X), np.array(Y), batch_size=batch_size, verbose=0, shuffle=True)

    def memorize(self, time_step):
        action, reward, new_state, done = time_step
        self.replay_memory.append([self.state, action, reward, new_state, done])
