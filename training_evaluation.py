from environment import FairEnv
from agent import RebalancingAgent
from network import generate_network, generate_bike_distribution
from demand import generate_global_demand
import numpy as np
import random
from tqdm import tqdm


# TRAINING PHASE
temperature = 0

num_central = 10
num_peripheral = 30
num_remote = 60
num_days = 1000
time_slots = [(0, 4), (4, 7), (7, 10), (10, 11), (11, 13), (13, 14), (14, 17), (17, 20), (20, 24)]
central_params = [(2, 2), (2, 2), (13, 1), (7, 1), (2, 2), (1, 6), (1, 10), (1, 7), (2, 2)]
peripheral_params = [(1, 1), (1, 1), (1, 7), (1, 5), (1, 1), (1, 1), (5, 1), (5, 1), (1, 1)]
remote_params = [(1, 1), (1, 1), (1, 2), (1, 2), (1, 1), (1, 2), (2, 1), (2, 1), (1, 1)]

G = generate_network(num_central, num_peripheral, num_remote)
all_days_demand_vectors, transformed_demand_vectors = generate_global_demand(num_central, num_peripheral,
                                                                             num_remote, num_days, central_params,
                                                                             peripheral_params, remote_params,
                                                                             time_slots)

agent = RebalancingAgent()

num_stations = 100
daily_returns = []
daily_failures = []
generate_bike_distribution(G, 1000, 'wg')
np.random.seed(0)
random.seed(0)

env = FairEnv(G, transformed_demand_vectors, temperature)
state = env.reset()

for repeat in range(10):
    for day in tqdm(range(num_days)):
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

# EVALUATION PHASE
daily_central_failures = []
daily_per_failures = []
daily_rem_failures = []
daily_global_failures = []

daily_central_rebalancing = []
daily_per_rebalancing = []
daily_rem_rebalancing = []
daily_global_rebalancing = []

agent.set_epsilon(0.0)

generate_bike_distribution(G, 1000, 'wg')
eval_env = FairEnv(G, transformed_demand_vectors, temperature)
state = eval_env.reset()
initial_bikes = 0
for i in range(100):
    initial_bikes += G.nodes[i]['bikes']

for day in range(100):
    ret = 0

    central_fails = 0
    per_fails = 0
    rem_fails = 0
    global_fails = 0

    central_rebalancing = 0
    per_rebalancing = 0
    rem_rebalancing = 0
    global_rebalancing = 0

    for time in (0, 1):
        actions = np.zeros(num_stations, dtype=np.int64)
        for i in range(num_stations):
            actions[i] = agent.decide_action(state[i])

        next_state, reward, failures = eval_env.step(actions)

        ret += np.sum(reward)

        central_fails += np.sum(failures[:10])
        per_fails += np.sum(failures[10:40])
        rem_fails += np.sum(failures[40:])
        global_fails += np.sum(failures)

        for a in range(len(actions)):
            if actions[a] != 0:
                global_rebalancing += 1
                if a < 10:
                    central_rebalancing += 1
                elif a < 40:
                    per_rebalancing += 1
                else:
                    rem_rebalancing += 1

        state = next_state

    daily_central_failures.append(central_fails/10)
    daily_per_failures.append(per_fails/30)
    daily_rem_failures.append(rem_fails/60)
    daily_global_failures.append(global_fails)

    daily_central_rebalancing.append(central_rebalancing/10)
    daily_per_rebalancing.append(per_rebalancing/30)
    daily_rem_rebalancing.append(rem_rebalancing/60)
    daily_global_rebalancing.append(global_rebalancing)

# PERFORMANCE METRICS
print('Recall that the maximum number of daily rebalancing operations for a generic station is 2')
print(f'Average number of daily rebalancing operations in the whole network: {np.mean(daily_global_rebalancing):.2f}')
print(f'Average number of daily rebalancing operations in a central station: {np.mean(daily_central_rebalancing):.2f}')
print(f'Average number of daily rebalancing operations in a peripheral station: {np.mean(daily_per_rebalancing):.2f}')
print(f'Average number of daily rebalancing operations in a remote station: {np.mean(daily_rem_rebalancing):.2f}')
print('')

central_requests = 0
per_requests = 0
rem_requests = 0
global_requests = 0

for day in range(100):
    for i in range(24):
        for j in range(100):
            if j < 10:
                if all_days_demand_vectors[day][j][i] < 0:
                    central_requests += abs(all_days_demand_vectors[day][j][i])
                    global_requests += abs(all_days_demand_vectors[day][j][i])
            elif j < 40:
                if all_days_demand_vectors[day][j][i] < 0:
                    per_requests += abs(all_days_demand_vectors[day][j][i])
                    global_requests += abs(all_days_demand_vectors[day][j][i])
            else:
                if all_days_demand_vectors[day][j][i] < 0:
                    rem_requests += abs(all_days_demand_vectors[day][j][i])
                    global_requests += abs(all_days_demand_vectors[day][j][i])

central_requests = central_requests / 100 / 10
per_requests = per_requests / 100 / 30
rem_requests = rem_requests / 100 / 60
global_requests = global_requests / 100

failure_rate_central = np.mean(daily_central_failures) / central_requests * 100
failure_rate_per = np.mean(daily_per_failures) / per_requests * 100
failure_rate_rem = np.mean(daily_rem_failures) / rem_requests * 100
failure_rate_global = np.mean(daily_global_failures) / global_requests * 100

print(f'Average daily failure rate in the network: {failure_rate_global:.2f} %')
print(f'Average daily failure rate in a central station: {failure_rate_central:.2f} %')
print(f'Average daily failure rate in a peripheral station: {failure_rate_per:.2f} %')
print(f'Average daily failure rate in a remote station: {failure_rate_rem:.2f} %')
print('')

b = 0
for i in range(100):
    b += G.nodes[i]['bikes']

bike_increment = (b - initial_bikes) / initial_bikes * 100

print(f'Percentage increase on the total number of bikes: {bike_increment:.2f} %')
