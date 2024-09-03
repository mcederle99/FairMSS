import numpy as np
from network import generate_network
from demand import generate_global_demand

num_central = 10
num_remote = 60
num_days = 100

time_slots = \
    [(0, 12), (12, 24)]
remote_params = \
        [(0.3, 2), (1.5, 0.3)]
central_params = \
        [(13.8, 3.6), (6.6, 13.8)]

G = generate_network([num_remote, num_central])
all_days_demand_vectors, transformed_demand_vectors = (
    generate_global_demand([num_remote, num_central], num_days,
                           [remote_params, central_params], time_slots))


central_requests = 0
# per_requests = 0
rem_requests = 0
global_requests = 0

central_arrivals = 0
# per_arrivals = 0
rem_arrivals = 0
global_arrivals = 0

for day in range(100):
    for i in range(12, 24):
        for j in range(num_central + num_remote):
            if j < 60:
                if all_days_demand_vectors[day][j][i] < 0:
                    rem_requests += abs(all_days_demand_vectors[day][j][i])
                    global_requests += abs(all_days_demand_vectors[day][j][i])
                else:
                    rem_arrivals += abs(all_days_demand_vectors[day][j][i])
                    global_arrivals += abs(all_days_demand_vectors[day][j][i])
            # elif j < 90:
            #     if all_days_demand_vectors[day][j][i] < 0:
            #         per_requests += abs(all_days_demand_vectors[day][j][i])
            #         global_requests += abs(all_days_demand_vectors[day][j][i])
            #     else:
            #         per_arrivals += abs(all_days_demand_vectors[day][j][i])
            #         global_arrivals += abs(all_days_demand_vectors[day][j][i])
            else:
                if all_days_demand_vectors[day][j][i] < 0:
                    central_requests += abs(all_days_demand_vectors[day][j][i])
                    global_requests += abs(all_days_demand_vectors[day][j][i])
                else:
                    central_arrivals += abs(all_days_demand_vectors[day][j][i])
                    global_arrivals += abs(all_days_demand_vectors[day][j][i])

central_requests = central_requests / 100 / 10
# per_requests = per_requests / 100 / 30
rem_requests = rem_requests / 100 / 60
global_requests = global_requests / 100

central_arrivals = central_arrivals / 100 / 10
# per_arrivals = per_arrivals / 100 / 30
rem_arrivals = rem_arrivals / 100 / 60
global_arrivals = global_arrivals / 100

print(f'Average daily requests in a central station: {central_requests}')
# print(f'Average daily requests in a peripheral station: {per_requests}')
print(f'Average daily requests in a remote station: {rem_requests}')
print(f'Average daily requests in the network: {global_requests}')
print("==================================")
print(f'Average daily arrivals in a central station: {central_arrivals}')
# print(f'Average daily arrivals in a peripheral station: {per_arrivals}')
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
