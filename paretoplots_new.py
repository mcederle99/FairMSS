import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import matplotlib.patches as mpatches

parser = argparse.ArgumentParser()
parser.add_argument("--cat", default=0, type=int)
parser.add_argument("--save", action='store_true')
args = parser.parse_args()

gini = np.load(f'results/gini_{args.cat}_cat_10seeds_bis.npy').transpose()
cost = np.load(f'results/cost_{args.cat}_cat_10seeds_bis.npy').transpose()

sns.set(style="whitegrid")

fig, ax = plt.subplots(figsize=(10, 6), dpi=100)

avg_ginis = [np.mean(gini[:, i]) for i in range(11)]
avg_costs = [np.mean(cost[:, i]) for i in range(11)]

beta = [r'$\beta$=0.0', r'$\beta$=0.1', r'$\beta$=0.2', r'$\beta$=0.3', r'$\beta$=0.4', r'$\beta$=0.5',
        r'$\beta$=0.6', r'$\beta$=0.7', r'$\beta$=0.8', r'$\beta$=0.9', r'$\beta$=1.0']

# 5 CATEGORIES
if args.cat == 5:
    ax.scatter(avg_costs, avg_ginis, 40, color='blue', marker='s')
    for i in range(10):
        ax.plot([avg_costs[i], avg_costs[i + 1]], [avg_ginis[i], avg_ginis[i]], color='blue', linewidth=1)
        ax.plot([avg_costs[i + 1], avg_costs[i + 1]], [avg_ginis[i], avg_ginis[i + 1]], color='blue', linewidth=1)

    plt.text(avg_costs[0] - 0.5, avg_ginis[0] - 0.035, beta[0], fontsize=24)
    plt.text(avg_costs[1] - 1, avg_ginis[1] - 0.032, beta[1], fontsize=24)
    plt.text(avg_costs[2] - 2, avg_ginis[2] - 0.025, beta[2], fontsize=24)
    plt.text(avg_costs[3] - 1.8, avg_ginis[3] - 0.028, beta[3], fontsize=24)
    plt.text(avg_costs[4] - 1.7, avg_ginis[4] - 0.03, beta[4], fontsize=24)
    plt.text(avg_costs[5] - 2, avg_ginis[5] - 0.008, beta[5], fontsize=24)
    plt.text(avg_costs[6] - 1.7, avg_ginis[6] - 0.03, beta[6], fontsize=24)
    plt.text(avg_costs[7] - 2, avg_ginis[7] - 0.025, beta[7], fontsize=24)
    plt.text(avg_costs[8] - 2, avg_ginis[8] - 0.02, beta[8], fontsize=24)
    plt.text(avg_costs[9] - 1.9, avg_ginis[9] - 0.03, beta[9], fontsize=24)
    plt.text(avg_costs[10] - 2, avg_ginis[10] - 0.021, beta[10], fontsize=24)

    blue_patch = mpatches.Patch(color='blue', label='Pareto efficient solutions')
    ax.legend(handles=[blue_patch], fontsize=26, loc='lower left', framealpha=0.4)

# 4 CATEGORIES
if args.cat == 4:
    ax.scatter(avg_costs, avg_ginis, 40, color='blue', marker='s')
    for i in range(10):
        ax.plot([avg_costs[i], avg_costs[i + 1]], [avg_ginis[i], avg_ginis[i]], color='blue', linewidth=1)
        ax.plot([avg_costs[i + 1], avg_costs[i + 1]], [avg_ginis[i], avg_ginis[i + 1]], color='blue', linewidth=1)

    plt.text(avg_costs[0] - 0.5, avg_ginis[0] - 0.03, beta[0], fontsize=24)
    plt.text(avg_costs[1] - 1, avg_ginis[1] - 0.03, beta[1], fontsize=24)
    plt.text(avg_costs[2] - 0.8, avg_ginis[2] - 0.03, beta[2], fontsize=24)
    plt.text(avg_costs[3] - 2, avg_ginis[3] - 0.02, beta[3], fontsize=24)
    plt.text(avg_costs[4] - 2, avg_ginis[4] - 0.015, beta[4], fontsize=24)
    plt.text(avg_costs[5] - 1.2, avg_ginis[5] - 0.028, beta[5], fontsize=24)
    plt.text(avg_costs[6] - 2, avg_ginis[6] - 0.01, beta[6], fontsize=24)
    plt.text(avg_costs[7] - 2, avg_ginis[7] - 0.01, beta[7], fontsize=24)
    plt.text(avg_costs[8] - 2, avg_ginis[8] - 0.01, beta[8], fontsize=24)
    plt.text(avg_costs[9] - 2, avg_ginis[9] - 0.025, beta[9], fontsize=24)
    plt.text(avg_costs[10] - 1.8, avg_ginis[10] - 0.02, beta[10], fontsize=24)

    blue_patch = mpatches.Patch(color='blue', label='Pareto efficient solutions')
    ax.legend(handles=[blue_patch], fontsize=26, loc='lower left', framealpha=0.4)

# 3 CATEGORIES
if args.cat == 3:
    ax.scatter(avg_costs[:8], avg_ginis[:8], 40, color='blue', marker='s')
    ax.scatter(avg_costs[9:11], avg_ginis[9:11], 40, color='blue', marker='s')
    ax.scatter(avg_costs[8], avg_ginis[8], 100, color='red', marker='+')

    for i in range(7):
        ax.plot([avg_costs[i], avg_costs[i + 1]], [avg_ginis[i], avg_ginis[i]], color='blue', linewidth=1)
        ax.plot([avg_costs[i + 1], avg_costs[i + 1]], [avg_ginis[i], avg_ginis[i + 1]], color='blue', linewidth=1)
    ax.plot([avg_costs[7], avg_costs[9]], [avg_ginis[7], avg_ginis[7]], color='blue', linewidth=1)
    ax.plot([avg_costs[9], avg_costs[9]], [avg_ginis[7], avg_ginis[9]], color='blue', linewidth=1)
    ax.plot([avg_costs[9], avg_costs[10]], [avg_ginis[9], avg_ginis[9]], color='blue', linewidth=1)
    ax.plot([avg_costs[10], avg_costs[10]], [avg_ginis[9], avg_ginis[10]], color='blue', linewidth=1)

    plt.text(avg_costs[0] - 0.5, avg_ginis[0] - 0.025, beta[0], fontsize=24)
    plt.text(avg_costs[1] - 1, avg_ginis[1] - 0.025, beta[1], fontsize=24)
    plt.text(avg_costs[2] - 0.8, avg_ginis[2] - 0.03, beta[2], fontsize=24)
    plt.text(avg_costs[3] - 1, avg_ginis[3] - 0.03, beta[3], fontsize=24)
    plt.text(avg_costs[4] - 1.2, avg_ginis[4] - 0.028, beta[4], fontsize=24)
    plt.text(avg_costs[5] - 1.2, avg_ginis[5] - 0.028, beta[5], fontsize=24)
    plt.text(avg_costs[6] - 1.2, avg_ginis[6] - 0.03, beta[6], fontsize=24)
    plt.text(avg_costs[7] - 1.5, avg_ginis[7] - 0.01, beta[7], fontsize=24)
    plt.text(avg_costs[8], avg_ginis[8] + 0.015, beta[8], fontsize=24)
    plt.text(avg_costs[9] - 1.6, avg_ginis[9] - 0.01, beta[9], fontsize=24)
    plt.text(avg_costs[10] - 0.8, avg_ginis[10] - 0.03, beta[10], fontsize=24)

    blue_patch = mpatches.Patch(color='blue', label='Pareto efficient solutions')
    red_patch = mpatches.Patch(color='red', label='Non-Pareto solutions')
    ax.legend(handles=[blue_patch, red_patch], fontsize=26, loc='lower left', framealpha=0.4)

# 2 CATEGORIES
if args.cat == 2:
    ax.scatter(avg_costs[:8], avg_ginis[:8], 40, color='blue', marker='s')
    ax.scatter(avg_costs[9:11], avg_ginis[9:11], 40, color='blue', marker='s')
    ax.scatter(avg_costs[8], avg_ginis[8], 100, color='red', marker='+')

    for i in range(7):
        ax.plot([avg_costs[i], avg_costs[i + 1]], [avg_ginis[i], avg_ginis[i]], color='blue', linewidth=1)
        ax.plot([avg_costs[i + 1], avg_costs[i + 1]], [avg_ginis[i], avg_ginis[i + 1]], color='blue', linewidth=1)
    ax.plot([avg_costs[7], avg_costs[9]], [avg_ginis[7], avg_ginis[7]], color='blue', linewidth=1)
    ax.plot([avg_costs[9], avg_costs[9]], [avg_ginis[7], avg_ginis[9]], color='blue', linewidth=1)
    ax.plot([avg_costs[9], avg_costs[10]], [avg_ginis[9], avg_ginis[9]], color='blue', linewidth=1)
    ax.plot([avg_costs[10], avg_costs[10]], [avg_ginis[9], avg_ginis[10]], color='blue', linewidth=1)

    plt.text(avg_costs[0] - 0.5, avg_ginis[0] - 0.035, beta[0], fontsize=24)
    plt.text(avg_costs[1] - 1, avg_ginis[1] - 0.035, beta[1], fontsize=24)
    plt.text(avg_costs[2] - 0.5, avg_ginis[2] - 0.035, beta[2], fontsize=24)
    plt.text(avg_costs[3] - 1, avg_ginis[3] - 0.035, beta[3], fontsize=24)
    plt.text(avg_costs[4] - 1.2, avg_ginis[4] - 0.035, beta[4], fontsize=24)
    plt.text(avg_costs[5] - 0.8, avg_ginis[5] - 0.035, beta[5], fontsize=24)
    plt.text(avg_costs[6] - 1.2, avg_ginis[6] - 0.04, beta[6], fontsize=24)
    plt.text(avg_costs[7] - 1.2, avg_ginis[7] - 0.035, beta[7], fontsize=24)
    plt.text(avg_costs[8], avg_ginis[8] + 0.015, beta[8], fontsize=24)
    plt.text(avg_costs[9] - 1.8, avg_ginis[9] - 0.015, beta[9], fontsize=24)
    plt.text(avg_costs[10] - 1.7, avg_ginis[10] - 0.01, beta[10], fontsize=24)

    blue_patch = mpatches.Patch(color='blue', label='Pareto efficient solutions')
    red_patch = mpatches.Patch(color='red', label='Non-Pareto solutions')
    ax.legend(handles=[blue_patch, red_patch], fontsize=26, loc='lower left', framealpha=0.4)

ax.set_ylabel('Gini index', fontsize=36)
ax.set_xlabel('Global service cost', fontsize=36)
ax.tick_params(labelsize=34)
ax.grid(True, which='major', linestyle=':', linewidth=1, color='grey', alpha=0.7)
# Show the plot
plt.tight_layout()
if args.save:
    plt.savefig(f"plots/pareto_costs_gini_{args.cat}_cat_new.pdf", format='pdf')
    plt.savefig(f"plots/pareto_costs_gini_{args.cat}_cat_new.png", format='png')
plt.show()
