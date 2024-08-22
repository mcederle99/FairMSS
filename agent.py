import random
import numpy as np


np.random.seed(0)


def get_state_bin(state):
    bins = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    for threshold in bins:
        if state[0] in (threshold - 2, threshold - 1, threshold, threshold + 1, threshold + 2):
            return (threshold, state[1], state[2])
    return (bins[-1], state[1], state[2])


class RebalancingAgent:
    def __init__(self, epsilon=1, epsilon_decay=0.99985, min_epsilon=0):
        self.learning_rate = 0.1
        self.discount_factor = 0.9  # 0.01
        self.q_table = {}
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon

    def set_epsilon(self, value):
        self.epsilon = value

    def get_q_value(self, state, action):
        binned_state = get_state_bin(state)
        key = (binned_state, action)
        return self.q_table.get(key, 0)

    def update_q_table(self, state, action, reward, next_state):
        binned_state = get_state_bin(state)
        binned_next_state = get_state_bin(next_state)
        actions = [-30, -20, -10, 0, 5, 10, 20]

        max_q_next = max(self.get_q_value(binned_next_state, a) for a in actions)
        q_current = self.get_q_value(binned_state, action)

        q_new = np.round(q_current + self.learning_rate * (reward + self.discount_factor * max_q_next - q_current), 1)
        self.q_table[(binned_state, action)] = q_new

    def print_q_table(self):
        for key, value in self.q_table.items():
            v = key[1]
            print(f"State-Action: {key[0]} {v}, Q-Value: {value}")

    def decide_action(self, state):
        binned_state = get_state_bin(state)
        if binned_state[0] > 30:
            actions = [-30, -20, -10, 0, 5, 10, 20]
        elif binned_state[0] > 20:
            actions = [-20, -10, 0, 5, 10, 20]
        elif binned_state[0] > 10:
            actions = [-10, 0, 5, 10, 20]
        else:
            actions = [0, 5, 10, 20]

        if random.random() < self.epsilon:
            return random.choice(actions)
        else:
            q_values = [self.get_q_value(binned_state, action) for action in actions]
            action = actions[np.argmax(q_values)]

        return action

    def update_epsilon(self):
        if self.epsilon > self.min_epsilon:
            self.epsilon *= self.epsilon_decay
