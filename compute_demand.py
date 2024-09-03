import numpy as np
from network import generate_network
from demand import generate_global_demand

num_central = 10
num_subcentral = 20
num_peripheral = 30
num_subremote = 40
num_remote = 60
node_list = [num_remote, num_subremote, num_peripheral, num_subcentral, num_central]
num_days = 100

time_slots = \
    [(0, 12), (12, 24)]
demand_params_0 = \
    [(0.3, 2), (1.5, 0.3)]
demand_params_1 = \
    [(0.45, 3), (2.25, 0.45)]
demand_params_2 = \
    [(3.3, 1.5), (1.5, 3.3)]
demand_params_3 = \
    [(9.2, 5.1), (6.6, 9.2)]
demand_params_4 = \
    [(13.8, 7), (10, 13.8)]
demand_params = [demand_params_0, demand_params_1, demand_params_2, demand_params_3, demand_params_4]

G = generate_network(node_list)
all_days_demand_vectors, transformed_demand_vectors = (
    generate_global_demand(node_list, num_days,
                           demand_params, time_slots))


central_requests = 0
subcentral_requests = 0
per_requests = 0
subrem_requests = 0
rem_requests = 0
global_requests = 0

central_arrivals = 0
subcentral_arrivals = 0
per_arrivals = 0
subrem_arrivals = 0
rem_arrivals = 0
global_arrivals = 0

for day in range(100):
    for i in range(12, 24):
        for j in range(np.sum(node_list)):
            if j < 60:
                if all_days_demand_vectors[day][j][i] < 0:
                    rem_requests += abs(all_days_demand_vectors[day][j][i])
                    global_requests += abs(all_days_demand_vectors[day][j][i])
                else:
                    rem_arrivals += abs(all_days_demand_vectors[day][j][i])
                    global_arrivals += abs(all_days_demand_vectors[day][j][i])
            elif j < 100:
                if all_days_demand_vectors[day][j][i] < 0:
                    subrem_requests += abs(all_days_demand_vectors[day][j][i])
                    global_requests += abs(all_days_demand_vectors[day][j][i])
                else:
                    subrem_arrivals += abs(all_days_demand_vectors[day][j][i])
                    global_arrivals += abs(all_days_demand_vectors[day][j][i])
            elif j < 130:
                if all_days_demand_vectors[day][j][i] < 0:
                    per_requests += abs(all_days_demand_vectors[day][j][i])
                    global_requests += abs(all_days_demand_vectors[day][j][i])
                else:
                    per_arrivals += abs(all_days_demand_vectors[day][j][i])
                    global_arrivals += abs(all_days_demand_vectors[day][j][i])
            elif j < 150:
                if all_days_demand_vectors[day][j][i] < 0:
                    subcentral_requests += abs(all_days_demand_vectors[day][j][i])
                    global_requests += abs(all_days_demand_vectors[day][j][i])
                else:
                    subcentral_arrivals += abs(all_days_demand_vectors[day][j][i])
                    global_arrivals += abs(all_days_demand_vectors[day][j][i])
            else:
                if all_days_demand_vectors[day][j][i] < 0:
                    central_requests += abs(all_days_demand_vectors[day][j][i])
                    global_requests += abs(all_days_demand_vectors[day][j][i])
                else:
                    central_arrivals += abs(all_days_demand_vectors[day][j][i])
                    global_arrivals += abs(all_days_demand_vectors[day][j][i])

central_requests = central_requests / 100 / 10
subcentral_requests = subcentral_requests / 100 / 20
per_requests = per_requests / 100 / 30
subrem_requests = subrem_requests / 100 / 40
rem_requests = rem_requests / 100 / 60
global_requests = global_requests / 100

central_arrivals = central_arrivals / 100 / 10
subcentral_arrivals = subcentral_arrivals / 100 / 20
per_arrivals = per_arrivals / 100 / 30
subrem_arrivals = subrem_arrivals / 100 / 40
rem_arrivals = rem_arrivals / 100 / 60
global_arrivals = global_arrivals / 100

print(f'Average daily requests in a central station: {central_requests}')
print(f'Average daily requests in a subcentral station: {subcentral_requests}')
print(f'Average daily requests in a peripheral station: {per_requests}')
print(f'Average daily requests in a subremote station: {subrem_requests}')
print(f'Average daily requests in a remote station: {rem_requests}')
print(f'Average daily requests in the network: {global_requests}')
print("==================================")
print(f'Average daily arrivals in a central station: {central_arrivals}')
print(f'Average daily arrivals in a subcentral station: {subcentral_arrivals}')
print(f'Average daily arrivals in a peripheral station: {per_arrivals}')
print(f'Average daily arrivals in a subremote station: {subrem_arrivals}')
print(f'Average daily arrivals in a remote station: {rem_arrivals}')
print(f'Average daily arrivals in the network: {global_arrivals}')

a_c = 9
a_p = 1.5
a_r = 2
n_c = 10
n_p = 30
n_r = 60

A = np.array([[0, n_p*0.9, 0.1*n_r], [0.2*n_c, 0, 0.9*n_r], [0.8*n_c, 0.1*n_p, 0]])
b = np.array([n_c*a_c, n_p*a_p, n_r*a_r])
z = np.linalg.solve(A, b)

# print(f'Central arrivals: {z[0]}')
# print(f'Peripheral arrivals: {z[1]}')
# print(f'Remote arrivals: {z[2]}')
