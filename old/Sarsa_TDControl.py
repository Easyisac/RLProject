import numpy as np

class SARSA_TDControl():
    def __init__(self,
                 space_size,
                 action_size,
                 gamma=1,
                 lr_v=0.01):
        """
        Calculates optimal policy using in-policy Temporal Difference control
        Evaluates Q-value for (S,A) pairs, using one-step updates.
        """
        # the discount factor
        self.gamma = gamma
        # size of system
        self.space_size = space_size # as tuple
        self.action_size = action_size

        # the learning rate
        self.lr_v = lr_v

        # where to save returns
        self.Qvalues = np.zeros( (*self.space_size, self.action_size) )

    # -------------------
    def single_step_update(self, s, a, r, new_s, new_a, done):
        """
        Uses a single step to update the values, using Temporal Difference for Q values.
        Employs the EXPERIENCED action in the new state  <- Q(S_new, A_new).
        """
        if done:


            # CODE HERE!
            # deltaQ = R - Q(s,a)

            deltaQ = (r + 0 - self.Qvalues[ (*s, a) ])
        else:

            # CODE HERE!
            # deltaQ = R + gamma*Q(new_s, new_a) - Q(s,a)

            deltaQ = (r +
                      self.gamma * self.Qvalues[ (*new_s, new_a) ]
                      - self.Qvalues[(*s, a)])

        self.Qvalues[(*s, a)] += self.lr_v * deltaQ

    # ---------------------
    def get_action_epsilon_greedy(self, s, eps):
        """
        Chooses action at random using an epsilon-greedy policy wrt the current Q(s,a).
        """
        ran = np.random.rand()

        # CODE HERE!

        if (ran < eps):
            # probability is uniform for all actions!
            prob_actions = np.ones(self.action_size) / self.action_size

        else:
            # I find the best Qvalue
            best_value = np.max(self.Qvalues[(*s,)])

            # There could be actions with equal value!
            best_actions = (self.Qvalues[(*s,)] == best_value)


            # best_actions is
            # *True* if the value is equal to the best (possibly ties)
            # *False* if the action is suboptimal
            prob_actions = best_actions / np.sum(best_actions)

        # take one action from the array of actions with the probabilities as defined above.
        a = np.random.choice(self.action_size, p=prob_actions)
        return a

    def greedy_policy(self):

        # CODE HERE!

        a = np.argmax(self.Qvalues, axis=2)
        return a