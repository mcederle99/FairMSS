import numpy as np


np.random.seed(0)


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

    def get_state(self):
        state = np.zeros((self.num_stations, 3), dtype=np.int64)
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

                if self.G.nodes[i]['station'] == 0 and n_bikes > 75:
                    self.G.nodes[i]['bikes'] = 75
                elif self.G.nodes[i]['station'] == 1 and n_bikes > 20:
                    self.G.nodes[i]['bikes'] = 20
                elif self.G.nodes[i]['station'] == 2 and n_bikes > 15:
                    self.G.nodes[i]['bikes'] = 15
                else:
                    self.G.nodes[i]['bikes'] = n_bikes

                state[i] = [self.G.nodes[i]['bikes'], self.G.nodes[i]['station'], time]

            self.hour += 1

        self.next_rebalancing_hour = 23 if self.hour == 12 else 11
        if self.next_rebalancing_hour == 11:
            self.day += 1
            self.hour = 0
            if self.day == 1000:
                self.day = 0

        return state, failures

    def compute_reward(self, action, failures):  # reward is a (num_stations, 1) vector
        rewards = np.zeros(self.num_stations)

        for i in range(self.num_stations):
            if action[i] != 0:
                rebalancing_penalty = 1
            else:
                rebalancing_penalty = 0
            rewards[i] -= failures[i]
            if self.G.nodes[i]['station'] == 0:
                rewards[i] -= self.beta * (-1) * failures[i]
                rewards[i] -= self.gamma * (1 - 0.6 - 0.3) * rebalancing_penalty
            elif self.G.nodes[i]['station'] == 1:
                rewards[i] -= self.beta * 0 * failures[i]
                rewards[i] -= self.gamma * (1 - 0.6) * rebalancing_penalty
            else:
                rewards[i] -= self.beta * 1 * failures[i]
                rewards[i] -= self.gamma * 1 * rebalancing_penalty

        return rewards

    def reset(self):
        self.hour = 0
        self.day = 0
        self.next_rebalancing_hour = 11

        state = np.zeros((self.num_stations, 3), dtype=np.int64)
        for i in range(self.num_stations):
            state[i] = [self.G.nodes[i]['bikes'], self.G.nodes[i]['station'], 0]

        return state

    def step(self, action):  # action is a (num_stations, 1) vector
        for i in range(self.num_stations):
            self.G.nodes[i]['bikes'] += action[i]

        state, failures = self.get_state()

        reward = self.compute_reward(action, failures)

        return state, reward, failures
