import numpy as np

a_c = 9
a_p = 1.5
a_r = 2
n_c = 10
n_p = 30
n_r = 60

A = np.array([[0, n_p*0.9, 0.1*n_r], [0.2*n_c, 0, 0.9*n_r], [0.8*n_c, 0.1*n_p, 0]])
b = np.array([n_c*a_c, n_p*a_p, n_r*a_r])
z = np.linalg.solve(A, b)

print(f'Central arrivals: {z[0]}')
print(f'Peripheral arrivals: {z[1]}')
print(f'Remote arrivals: {z[2]}')
