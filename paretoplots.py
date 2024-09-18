import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import matplotlib.patches as mpatches

parser = argparse.ArgumentParser()
parser.add_argument("--cat", default=0, type=int)
parser.add_argument("--save", action='store_true')
args = parser.parse_args()

gini = np.load(f'results/gini_{args.cat}_cat_10seeds.npy').transpose()
cost = np.load(f'results/cost_{args.cat}_cat_10seeds.npy').transpose()

sns.set(style="whitegrid")

fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
if args.cat in (3, 5):
    front = 10
elif args.cat == 4:
    front = 8
else:
    front = 7

avg_ginis = [np.mean(gini[:, i]) for i in range(11)]
avg_costs = [np.mean(cost[:, i]) for i in range(11)]

beta = [r'$\beta$=0.0', r'$\beta$=0.1', r'$\beta$=0.2', r'$\beta$=0.3', r'$\beta$=0.4', r'$\beta$=0.5',
        r'$\beta$=0.6', r'$\beta$=0.7', r'$\beta$=0.8', r'$\beta$=0.9', r'$\beta$=1.0']

ax.scatter(avg_costs[:front+1], avg_ginis[:front+1], 40, color='blue', marker='s')
if front < 10:
    ax.scatter(avg_costs[front+1:], avg_ginis[front+1:], 100, color='red', marker='+')

for i in range(front):
    ax.plot([avg_costs[i], avg_costs[i+1]], [avg_ginis[i], avg_ginis[i]], color='blue', linewidth=1)
    ax.plot([avg_costs[i+1], avg_costs[i+1]], [avg_ginis[i], avg_ginis[i+1]], color='blue', linewidth=1)

# 5 CATEGORIES
if args.cat == 5:
    for i in range(11):
        if i == 7:
            plt.text(avg_costs[i] - 2.1, avg_ginis[i] - 0.005, beta[i], fontsize=24)
        elif i == 1:
            plt.text(avg_costs[i] - 1.4, avg_ginis[i] - 0.03, beta[i], fontsize=24)
        elif i == 8:
            plt.text(avg_costs[i] + 0.2, avg_ginis[i] + 0.007, beta[i], fontsize=24)
        elif i in (9, 10):
            plt.text(avg_costs[i] - 2.3, avg_ginis[i], beta[i], fontsize=24)
        elif i in (5, 6):
            plt.text(avg_costs[i] - 2, avg_ginis[i] - 0.025, beta[i], fontsize=24)
        else:
            plt.text(avg_costs[i] - 0.8, avg_ginis[i] - 0.03, beta[i], fontsize=24)
    blue_patch = mpatches.Patch(color='blue', label='Pareto efficient solutions')
    ax.legend(handles=[blue_patch], fontsize=30, loc='lower left')

# 4 CATEGORIES
if args.cat == 4:
    for i in range(11):
        if i == 7:
            plt.text(avg_costs[i] - 2, avg_ginis[i] - 0.005, beta[i], fontsize=24)
        elif i in (0, 1, 2):
            plt.text(avg_costs[i] - 0.8, avg_ginis[i] - 0.02, beta[i], fontsize=24)
        elif i == 3:
            plt.text(avg_costs[i] - 2.2, avg_ginis[i] - 0.005, beta[i], fontsize=24)
        elif i == 4:
            plt.text(avg_costs[i] - 2.1, avg_ginis[i] - 0.005, beta[i], fontsize=24)
        elif i in (5, 6):
            plt.text(avg_costs[i] + 0.3, avg_ginis[i] + 0.005, beta[i], fontsize=24)
        elif i == 8:
            plt.text(avg_costs[i] - 2, avg_ginis[i] + 0.005, beta[i], fontsize=24)
        elif i == 9:
            plt.text(avg_costs[i] - 1, avg_ginis[i] - 0.025, beta[i], fontsize=24)
        elif i == 10:
            plt.text(avg_costs[i] - 1, avg_ginis[i] + 0.008, beta[i], fontsize=24)
    blue_patch = mpatches.Patch(color='blue', label='Pareto efficient solutions')
    red_patch = mpatches.Patch(color='red', label='Non-Pareto solutions')
    ax.legend(handles=[blue_patch, red_patch], fontsize=26, loc='lower left')

# 3 CATEGORIES
if args.cat == 3:
    for i in range(11):
        if i in (5, 6, 7):
            plt.text(avg_costs[i] - 1.6, avg_ginis[i] - 0.02, beta[i], fontsize=24)
        elif i == 4:
            plt.text(avg_costs[i] - 1.8, avg_ginis[i] - 0.01, beta[i], fontsize=24)
        elif i in (0, 1):
            plt.text(avg_costs[i] - 0.3, avg_ginis[i] - 0.025, beta[i], fontsize=24)
        elif i in (2, 3):
            plt.text(avg_costs[i] - 1, avg_ginis[i] - 0.025, beta[i], fontsize=24)
        elif i == 8:
            plt.text(avg_costs[i] + 0.3, avg_ginis[i] + 0.005, beta[i], fontsize=24)
        elif i == 9:
            plt.text(avg_costs[i] - 1.7, avg_ginis[i] - 0.002, beta[i], fontsize=24)
        else:
            plt.text(avg_costs[i] - 1.7, avg_ginis[i] - 0.01, beta[i], fontsize=24)
    blue_patch = mpatches.Patch(color='blue', label='Pareto efficient solutions')
    ax.legend(handles=[blue_patch], fontsize=30, loc='lower left')

# 2 CATEGORIES
if args.cat == 2:
    for i in range(11):
        if i in (0, 2):
            plt.text(avg_costs[i] - 0.5, avg_ginis[i] - 0.025, beta[i], fontsize=24)
        elif i == 1:
            plt.text(avg_costs[i] - 0.8, avg_ginis[i] - 0.025, beta[i], fontsize=24)
        elif i in (3, 4, 5):
            plt.text(avg_costs[i] - 1.6, avg_ginis[i] - 0.012, beta[i], fontsize=24)
        elif i == 6:
            plt.text(avg_costs[i] - 1.6, avg_ginis[i] + 0.02, beta[i], fontsize=24)
        elif i == 7:
            plt.text(avg_costs[i], avg_ginis[i] - 0.02, beta[i], fontsize=24)
        elif i == 8:
            plt.text(avg_costs[i] - 1.9, avg_ginis[i] - 0.002, beta[i], fontsize=24)
        elif i == 9:
            plt.text(avg_costs[i] + 0.2, avg_ginis[i] - 0.01, beta[i], fontsize=24)
        elif i == 10:
            plt.text(avg_costs[i] - 0.5, avg_ginis[i] + 0.005, beta[i], fontsize=24)
    blue_patch = mpatches.Patch(color='blue', label='Pareto efficient solutions')
    red_patch = mpatches.Patch(color='red', label='Non-Pareto solutions')
    ax.legend(handles=[blue_patch, red_patch], fontsize=26, loc='lower left')

ax.set_ylabel('Gini index', fontsize=36)
ax.set_xlabel('Global service cost', fontsize=36)
ax.tick_params(labelsize=34)
ax.grid(True, which='major', linestyle=':', linewidth=1, color='grey', alpha=0.7)
# Show the plot
plt.tight_layout()
if args.save:
    plt.savefig(f"plots/pareto_costs_gini_{args.cat}_cat.pdf", format='pdf')
    plt.savefig(f"plots/pareto_costs_gini_{args.cat}_cat.png", format='png')
plt.show()
