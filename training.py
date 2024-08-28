from environment import FairEnv
from agent import RebalancingAgent
from network import generate_network, generate_bike_distribution
from demand import generate_global_demand
import numpy as np
import random
import pickle
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--beta", default=0, type=float)
parser.add_argument("--categories", default=0, type=int)
parser.add_argument("--seed", default=0, type=int)
args = parser.parse_args()

beta = args.beta / 10
gamma = 10

num_days = 1000
time_slots = [(0, 4), (4, 7), (7, 10), (10, 11), (11, 13), (13, 14), (14, 17), (17, 20), (20, 24)]

demand_params_0 = [(1, 1), (1, 1), (1, 2), (1, 2), (1, 1), (1, 2), (2, 1), (2, 1), (1, 1)]
demand_params_1 = [(1, 1), (1, 1), (1, 3), (1, 3), (1, 1), (1, 1), (3, 1), (3, 1), (1, 1)]
demand_params_2 = [(1, 1), (1, 1), (1, 7), (1, 5), (1, 1), (1, 1), (5, 1), (5, 1), (1, 1)]
demand_params_3 = [(2, 2), (2, 2), (8, 1), (5, 1), (2, 2), (1, 4), (1, 7), (1, 5), (2, 2)]
demand_params_4 = [(2, 2), (2, 2), (13, 1), (7, 1), (2, 2), (1, 6), (1, 10), (1, 7), (2, 2)]

if args.categories == 2:
    demand_params = [demand_params_0, demand_params_4]
    node_list = [60, 10]
    total_bikes = 700
elif args.categories == 3:
    demand_params = [demand_params_0, demand_params_2, demand_params_4]
    node_list = [60, 30, 10]
    total_bikes = 1000
elif args.categories == 4:
    demand_params = [demand_params_0, demand_params_1, demand_params_3, demand_params_4]
    node_list = [60, 45, 20, 10]
    total_bikes = 1400
elif args.categories == 5:
    demand_params = [demand_params_0, demand_params_1, demand_params_2, demand_params_3, demand_params_4]
    node_list = [60, 45, 30, 20, 10]
    total_bikes = 1700
else:
    raise ValueError("Wrong number of categories. Select among [2, 3, 4, 5]")

G = generate_network(node_list)
all_days_demand_vectors, transformed_demand_vectors = generate_global_demand(node_list, num_days,
                                                                             demand_params, time_slots)
agent = RebalancingAgent()

num_stations = np.sum(node_list)
daily_returns = []
daily_failures = []
generate_bike_distribution(G, total_bikes, args.categories, 'wg')
np.random.seed(args.seed)
random.seed(args.seed)

env = FairEnv(G, transformed_demand_vectors, beta, gamma)
state = env.reset()

for repeat in range(10):
    for day in range(num_days):
        ret = 0
        fails = 0
        for time in (0, 1):
            actions = np.zeros(num_stations, dtype=np.int64)
            for i in range(num_stations):
                actions[i] = agent.decide_action(state[i])

            next_state, reward, failures = env.step(actions)
            ret += np.sum(reward)
            fails += np.sum(failures)

            for i in range(num_stations):
                agent.update_q_table(state[i], actions[i], reward[i], next_state[i])

            agent.update_epsilon()
            state = next_state

        daily_returns.append(ret)
        daily_failures.append(fails)

# plt.plot(daily_returns)
# plt.savefig(f"learning_curves/daily_returns_{args.beta / 10}_{args.categories}.png")
# plt.close()
# plt.plot(daily_failures)
# plt.savefig(f"learning_curves/daily_failures_{args.beta / 10}_{args.categories}.png")
# plt.close()

with open(f"q_tables/q_table_{args.beta / 10}_{args.categories}_{args.seed}.pkl", "wb") as file:
    pickle.dump(agent.q_table, file)

print(f'Finished simulation with seed: {args.seed}, categories: {args.categories} and beta: {args.beta / 10}')
