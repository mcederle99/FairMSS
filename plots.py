import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--cat", default=0, type=int)
args = parser.parse_args()

gini = np.load(f'results/gini_{args.cat}_cat_fixed_alsodemand.npy').transpose()
cost = np.load(f'results/cost_{args.cat}_cat_fixed_alsodemand.npy').transpose()
# bikes = np.load(f'results/bikes_{args.cat}_cat_fixed_alsodemand.npy')
# max_bikes = np.load(f'results/max_bikes_{args.cat}_cat_fixed_alsodemand.npy')

# TOTAL NUMBER OF BIKES INCREASE
# betas = ['0.0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1.0']
# increment = []
# max_increment = []
# for i in range(11):
#     increment.append(np.mean(bikes[i, :]))
#     max_increment.append(np.mean(max_bikes[i, :]))
#
# plt.figure(figsize=(10, 6))
# plt.scatter(range(1, 12), increment)
# plt.xlabel(r'$\beta$', fontsize=14)
# plt.ylabel('Bike increment wrt day 0 (%)', fontsize=14)
# plt.xticks(range(1, 12), ['0.0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1.0'])
# plt.grid(axis='y')
# # plt.savefig(f"plots/bike_increment_{args.cat}_cat.pdf", format='pdf')
# plt.show()

# BOX PLOT BETA VERSUS GINI
plt.figure(figsize=(10, 6))
bplot = plt.boxplot(gini, patch_artist=True)

colors = ['limegreen'] * 11
for patch, color in zip(bplot['boxes'], colors):
    patch.set_facecolor(color)

median_color = 'black'
plt.setp(bplot['medians'], color=median_color)

plt.xlabel(r'$\beta$', fontsize=14)
plt.ylabel('Gini index', fontsize=14)
plt.xticks(range(1, 12), ['0.0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1.0'])
plt.grid(axis='y')
# plt.savefig(f"plots/boxplot_gini_{args.cat}_cat_fixed.pdf", format='pdf')
plt.show()

# BOX PLOT BETA VERSUS COSTS
plt.figure(figsize=(10, 6))
bplot = plt.boxplot(cost, patch_artist=True)

median_color = 'black'
plt.setp(bplot['medians'], color=median_color)

plt.xlabel(r'$\beta$', fontsize=14)
plt.ylabel('Daily global cost', fontsize=14)
plt.xticks(range(1, 12), ['0.0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1.0'])
plt.grid(axis='y')
# plt.savefig(f"plots/boxplot_costs_{args.cat}_cat_fixed.pdf", format='pdf')
plt.show()

# PARETO FRONT COSTS VERSUS GINI
avg_ginis = [np.mean(gini[:, i]) for i in range(11)]
avg_costs = [np.mean(cost[:, i]) for i in range(11)]

# beta = [r'$\beta$=0.0', r'$\beta$=0.1', r'$\beta$=0.2', r'$\beta$=0.3', r'$\beta$=0.4', r'$\beta$=0.5',
#         r'$\beta$=0.6', r'$\beta$=0.7', r'$\beta$=0.8', r'$\beta$=0.9', r'$\beta$=1.0']
beta = ['0.0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1.0']

plt.figure(figsize=(10, 6))

plt.scatter(avg_costs, avg_ginis, color='blue')

for i in range(11):
    plt.text(avg_costs[i], avg_ginis[i], beta[i], fontsize=14)

# x = avg_costs[3:]
# y = avg_ginis[3:]
#
# interp_func = interp1d(x, y, kind='linear')
# x_interp = np.linspace(min(x), max(x), 100)
# y_interp = interp_func(x_interp)

# for i, (avg_gini, avg_cost) in enumerate(zip(avg_ginis, avg_costs)):
#     if i in (0, 1, 2):
#         plt.scatter(avg_cost, avg_gini, color='limegreen', marker='^')
#     else:
#         plt.scatter(avg_cost, avg_gini, color='blue')
#     if i == 0:
#         plt.text(avg_cost - 0.9, avg_gini - 0.03, beta[i], fontsize=14)
#     elif i == 3:
#         plt.text(avg_cost + 0.5, avg_gini - 0.008, beta[i], fontsize=14)
#     elif i == 2:
#         plt.text(avg_cost, avg_gini + 0.01, beta[i], fontsize=14)
#     else:
#         plt.text(avg_cost + 1, avg_gini, beta[i], fontsize=14)
#
# plt.plot(x_interp, y_interp, color='blue')

plt.ylabel('Average Gini coefficient', fontsize=14)
plt.xlabel('Average costs', fontsize=14)
plt.grid(True)
# plt.savefig(f"plots/pareto_costs_gini_{args.cat}_cat_fixed.pdf", format='pdf')
plt.show()
