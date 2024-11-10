import numpy as np
import matplotlib.pyplot as plt
import argparse
import matplotlib.patches as mpatches

parser = argparse.ArgumentParser()
parser.add_argument("--save", action='store_true')
parser.add_argument("--cat", default=0, type=int)
args = parser.parse_args()


# Exponential moving average function
def exponential_moving_average(data, a=0.1):
    ema = np.zeros_like(data)
    ema[0] = data[0]
    for t in range(1, len(data)):
        ema[t] = a * data[t] + (1 - a) * ema[t - 1]
    return ema


num_seeds = 10
num_episodes = 109999

rewards_0 = np.zeros((num_seeds, num_episodes))
rewards_05 = np.zeros((num_seeds, num_episodes))
rewards_1 = np.zeros((num_seeds, num_episodes))
for s in range(100, 110):
    test_0 = np.load(f'results/learning_curve_{args.cat}_cat_0.0_{s}.npy')
    test_05 = np.load(f'results/learning_curve_{args.cat}_cat_0.5_{s}.npy')
    test_1 = np.load(f'results/learning_curve_{args.cat}_cat_1.0_{s}.npy')
    rewards_0[s - 100] = test_0
    rewards_05[s - 100] = test_05
    rewards_1[s - 100] = test_1

# Plot the learning curve
episodes = np.arange(num_episodes)
alpha = 0.05

plt.figure(figsize=(10, 6))
for rewards, colors in zip((rewards_0, rewards_05, rewards_1), ('#1f77b4', '#ff7f0e', '#2ca02c')):
    mean_rewards = np.mean(rewards, axis=0)
    std_rewards = np.std(rewards, axis=0)

    mean_rewards = exponential_moving_average(mean_rewards, alpha)

    # Plot the mean reward
    if colors == "#1f77b4":
        plt.plot(episodes, mean_rewards, color=colors, label=r'$\beta$=0.0')
    elif colors == "#ff7f0e":
        plt.plot(episodes, mean_rewards, color=colors, label=r'$\beta$=0.5')
    else:
        plt.plot(episodes, mean_rewards, color=colors, label=r'$\beta$=1.0')

    # Plot the confidence interval (mean ± std deviation)
    plt.fill_between(episodes, mean_rewards - std_rewards*1.96, mean_rewards + std_rewards*1.96,
                     color=colors, alpha=0.2)

# Labels and legend
plt.xlim([0, 109999])
plt.xlabel("Episodes (Days)", fontsize=36)
plt.ylabel("Daily Return", fontsize=36)
plt.xticks((0, 20000, 40000, 60000, 80000, 100000), ['0', '20k', '40k', '60k', '80k', '100k'])
if args.cat == 5:
    plt.yticks((-1000, -2000, -3000, -4000, -5000, -6000), ['-1k', '-2k', '-3k', '-4k', '-5k', '-6k'])
else:
    plt.yticks((-1000, -2000, -3000), ['-1k', '-2k', '-3k'])
plt.tick_params(labelsize=34)
blue_patch = mpatches.Patch(color='#1f77b4', label=r'$\beta$=0.0')
red_patch = mpatches.Patch(color='#ff7f0e', label=r'$\beta$=0.5')
green_patch = mpatches.Patch(color='#2ca02c', label=r'$\beta$=1.0')
plt.legend(handles=[blue_patch, red_patch, green_patch], fontsize=26)
plt.grid(True, which='major', linestyle=':', linewidth=1, color='grey', alpha=0.7)
plt.tight_layout()

if args.save:
    plt.savefig(f"plots/learning_curves_{args.cat}_cat.pdf", format='pdf')
    plt.savefig(f"plots/learning_curves_{args.cat}_cat.png", format='png')

plt.show()
