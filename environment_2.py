import numpy as np


class FairEnv:

    def __init__(self, graph, demand_vectors, beta, gamma):
        self.G = graph
        self.demand_vectors = demand_vectors
        self.num_stations = len(list(self.G.nodes))
        self.hour = 0
        self.day = 0
        self.next_rebalancing_hour = 11
        self.beta = beta
        self.gamma = gamma
        self.csi = 0.3

    def get_state(self):
        state = np.zeros((self.num_stations, 2), dtype=np.int64)
        failures = [0] * self.num_stations

        time = 0 if self.next_rebalancing_hour == 11 else 1
        while self.hour <= self.next_rebalancing_hour:
            for i in range(self.num_stations):
                n_bikes = self.G.nodes[i]['bikes']

                demand_list = self.demand_vectors[self.day][i][self.hour]
                for demand_change in demand_list:
                    n_bikes += demand_change
                    if n_bikes < 0:
                        n_bikes = 0
                        failures[i] += 1

                if n_bikes > 100:
                    self.G.nodes[i]['bikes'] = 100
                else:
                    self.G.nodes[i]['bikes'] = n_bikes

                state[i] = [self.G.nodes[i]['bikes'], time]

            self.hour += 1

        self.next_rebalancing_hour = 23 if self.hour == 12 else 11
        if self.next_rebalancing_hour == 11:
            self.day += 1
            self.hour = 0
            if self.day == 1000:
                self.day = 0

        return state, failures

    def compute_reward(self, action, failures, mu):  # reward is a (num_stations, 1) vector
        rewards = np.zeros(self.num_stations)

        for i in range(self.num_stations):
            if action[i] != 0:
                rebalancing_penalty = 1
            else:
                rebalancing_penalty = 0
            rewards[i] -= failures[i]
            if self.G.nodes[i]['station'] == 0:
                rewards[i] -= self.beta * 1 * failures[i]
                rewards[i] -= self.gamma * 1 * rebalancing_penalty
                if self.next_rebalancing_hour == 23:
                    rewards[i] -= self.csi * abs(mu[i] - 22) - 0.4
                else:
                    rewards[i] -= self.csi * abs(mu[i] - 2) - 8

            elif self.G.nodes[i]['station'] == 4:
                rewards[i] -= self.beta * (-1) * failures[i]
                rewards[i] -= self.gamma * 0.1 * rebalancing_penalty
                if self.next_rebalancing_hour == 23:
                    rewards[i] -= self.csi * abs(mu[i]) - 61
                else:
                    rewards[i] -= self.csi * abs(mu[i] - 88) - 1

        return rewards

    def reset(self):
        self.hour = 0
        self.day = 0
        self.next_rebalancing_hour = 11

        state = np.zeros((self.num_stations, 2), dtype=np.int64)
        for i in range(self.num_stations):
            state[i] = [self.G.nodes[i]['bikes'], 0]

        return state

    def step(self, action):  # action is a (num_stations, 1) vector
        mu = np.zeros(self.num_stations, dtype=np.int64)
        for i in range(self.num_stations):
            self.G.nodes[i]['bikes'] += action[i]
            mu[i] = self.G.nodes[i]['bikes']

        state, failures = self.get_state()

        reward = self.compute_reward(action, failures, mu)

        return state, reward, failures
