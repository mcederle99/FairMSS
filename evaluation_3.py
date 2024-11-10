from environment_3 import FairEnv
from agent import RebalancingAgent
from network import generate_network
from demand import generate_global_demand
import numpy as np
import random
import pickle
import inequalipy as ineq

gini_values_tot = [[], [], [], [], [], [], [], [], [], [], []]
costs_tot = [[], [], [], [], [], [], [], [], [], [], []]

for beta in (0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0):
    index = int(beta * 10)
    for seed in range(100, 110):
        np.random.seed(seed)
        random.seed(seed)

        n_bikes = np.load(f'results/bikes_3_cat_{beta}_{seed}.npy')

        gamma = 20

        num_central = 10
        num_peripheral = 30
        num_remote = 60
        num_days = 101

        time_slots = \
            [(0, 12), (12, 24)]
        remote_params = \
            [(0.3, 2), (1.5, 0.3)]
        peripheral_params = \
            [(3.3, 1.5), (1.5, 3.3)]
        central_params = \
            [(13.8, 9), (12, 13.8)]

        G = generate_network([num_remote, num_peripheral, num_central])
        all_days_demand_vectors, transformed_demand_vectors = (
            generate_global_demand([num_remote, num_peripheral, num_central], num_days,
                                   [remote_params, peripheral_params, central_params], time_slots))

        agent_0 = RebalancingAgent(0)
        agent_2 = RebalancingAgent(2)
        agent_4 = RebalancingAgent(4)

        with open(f"q_tables/q_table_{beta}_3_{seed}_cat0.pkl", "rb") as file:
            agent_0.q_table = pickle.load(file)
        with open(f"q_tables/q_table_{beta}_3_{seed}_cat2.pkl", "rb") as file:
            agent_2.q_table = pickle.load(file)
        with open(f"q_tables/q_table_{beta}_3_{seed}_cat4.pkl", "rb") as file:
            agent_4.q_table = pickle.load(file)

        num_stations = 100

        daily_central_failures = []
        daily_per_failures = []
        daily_rem_failures = []
        daily_global_failures = []

        daily_central_rebalancing = []
        daily_per_rebalancing = []
        daily_rem_rebalancing = []
        daily_global_rebalancing = []

        daily_global_costs = []

        agent_0.set_epsilon(0.0)
        agent_2.set_epsilon(0.0)
        agent_4.set_epsilon(0.0)

        eval_env = FairEnv(G, transformed_demand_vectors, beta, gamma)
        state = eval_env.reset()

        for day in range(101):
            ret = 0

            central_fails = 0
            per_fails = 0
            rem_fails = 0
            global_fails = 0

            central_rebalancing = 0
            per_rebalancing = 0
            rem_rebalancing = 0
            global_rebalancing = 0

            costs = 0

            for time in (0, 1):
                actions = np.zeros(num_stations, dtype=np.int64)
                if day > 0:
                    for i in range(num_stations):
                        if G.nodes[i]['station'] == 0:
                            actions[i] = agent_0.decide_action(state[i])
                        elif G.nodes[i]['station'] == 2:
                            actions[i] = agent_2.decide_action(state[i])
                        else:
                            actions[i] = agent_4.decide_action(state[i])

                next_state, reward, failures = eval_env.step(actions)

                ret += np.sum(reward)

                central_fails += np.sum(failures[90:])
                per_fails += np.sum(failures[60:90])
                rem_fails += np.sum(failures[:60])
                global_fails += np.sum(failures)

                for a in range(len(actions)):
                    if actions[a] != 0:
                        global_rebalancing += 1
                        if a < 60:
                            rem_rebalancing += 1
                            costs += 1
                        elif a < 90:
                            per_rebalancing += 1
                            costs += 0.4
                        else:
                            central_rebalancing += 1
                            costs += 0.1

                state = next_state

            if day > 0:
                daily_central_failures.append(central_fails/10)
                daily_per_failures.append(per_fails/30)
                daily_rem_failures.append(rem_fails/60)
                daily_global_failures.append(global_fails)

                daily_central_rebalancing.append(central_rebalancing/10)
                daily_per_rebalancing.append(per_rebalancing/30)
                daily_rem_rebalancing.append(rem_rebalancing/60)
                daily_global_rebalancing.append(global_rebalancing)

                daily_global_costs.append(costs)

        central_requests = 0
        per_requests = 0
        rem_requests = 0
        global_requests = 0

        for day in range(101):
            for i in range(24):
                for j in range(100):
                    if j < 60:
                        if all_days_demand_vectors[day][j][i] < 0:
                            rem_requests += abs(all_days_demand_vectors[day][j][i])
                            global_requests += abs(all_days_demand_vectors[day][j][i])
                    elif j < 90:
                        if all_days_demand_vectors[day][j][i] < 0:
                            per_requests += abs(all_days_demand_vectors[day][j][i])
                            global_requests += abs(all_days_demand_vectors[day][j][i])
                    else:
                        if all_days_demand_vectors[day][j][i] < 0:
                            central_requests += abs(all_days_demand_vectors[day][j][i])
                            global_requests += abs(all_days_demand_vectors[day][j][i])

        central_requests = central_requests / 101 / 10
        per_requests = per_requests / 101 / 30
        rem_requests = rem_requests / 101 / 60
        global_requests = global_requests / 101

        failure_rate_central = np.mean(daily_central_failures) / central_requests * 100
        failure_rate_per = np.mean(daily_per_failures) / per_requests * 100
        failure_rate_rem = np.mean(daily_rem_failures) / rem_requests * 100
        failure_rate_global = np.mean(daily_global_failures) / global_requests * 100

        gini_coefficient = np.round(ineq.gini([failure_rate_central, failure_rate_per, failure_rate_rem]), 3)
        gini_values_tot[index].append(gini_coefficient)
        costs_tot[index].append(np.mean(daily_global_costs) + n_bikes / 100 + failure_rate_global / 10)

np.save('results/gini_3_cat_10seeds.npy', gini_values_tot)
np.save('results/cost_3_cat_10seeds.npy', costs_tot)
