import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--cat", default=0, type=int)
parser.add_argument("--save", action='store_true')
args = parser.parse_args()

gini = np.load(f'results/gini_{args.cat}_cat_10seeds.npy').transpose()
cost_reb = np.load(f'results/cost_reb_{args.cat}_cat_10seeds.npy').transpose()
cost_fail = np.load(f'results/cost_fail_{args.cat}_cat_10seeds.npy').transpose()
cost_bikes = np.load(f'results/cost_bikes_{args.cat}_cat_10seeds.npy').transpose()
beta = ['w', '0.0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1.0']

# GINI INDEX

# Setting a nice aesthetic for the plots
sns.set(style="whitegrid")
# Creating a figure and axis with higher resolution
fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
# Using a single custom color
box_color = sns.color_palette("viridis", 11)[7]
# Creating the boxplot with custom settings
box = ax.boxplot(gini, patch_artist=True, notch=False, vert=True, widths=0.6)
# Customizing each box with the same color
for patch in box['boxes']:
    patch.set_facecolor(box_color)
    patch.set_edgecolor('black')
    patch.set_alpha(0.8)
    patch.set_linewidth(1.5)
# Customizing whiskers, caps, and medians
for whisker in box['whiskers']:
    whisker.set(color='black', linewidth=1.5, linestyle='--')
for cap in box['caps']:
    cap.set(color='black', linewidth=1.5)
for median in box['medians']:
    median.set(color='black', linewidth=1.5)
for flier in box['fliers']:
    flier.set(marker='o', color='red', alpha=0.75)
# Adding a title and axis labels with custom fonts
ax.set_xlabel(r'$\beta$', fontsize=36)
ax.set_ylabel("Gini index", fontsize=36)
# Customizing the gridlines
ax.grid(True, which='major', linestyle=':', linewidth=1, color='grey', alpha=0.7)
# Tweaking x and y axes ticks
ax.set_xticks(range(1, 12))
ax.set_xticklabels([beta[i] for i in range(1, 12)], fontsize=34)
ax.tick_params(labelsize=34)
ax.tick_params(axis='y')
# Show the plot
plt.tight_layout()
if args.save:
    plt.savefig(f"plots/boxplot_gini_{args.cat}_cat.pdf", format='pdf')
    plt.savefig(f"plots/boxplot_gini_{args.cat}_cat.png", format='png')
plt.show()

# REBALANCING COSTS

# Setting a nice aesthetic for the plots
sns.set(style="whitegrid")
# Creating a figure and axis with higher resolution
fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
# Using a single custom color
box_color = sns.color_palette("viridis", 11)[2]
# Creating the boxplot with custom settings
box = ax.boxplot(cost_reb, patch_artist=True, notch=False, vert=True, widths=0.6)
# Customizing each box with the same color
for patch in box['boxes']:
    patch.set_facecolor(box_color)
    patch.set_edgecolor('black')
    patch.set_alpha(0.8)
    patch.set_linewidth(1.5)
# Customizing whiskers, caps, and medians
for whisker in box['whiskers']:
    whisker.set(color='black', linewidth=1.5, linestyle='--')
for cap in box['caps']:
    cap.set(color='black', linewidth=1.5)
for median in box['medians']:
    median.set(color='gold', linewidth=1.5)
for flier in box['fliers']:
    flier.set(marker='o', color='red', alpha=0.75)
ax.set_xlabel(r'$\beta$', fontsize=36)
ax.set_ylabel("Weighted reb. op's", fontsize=36)
# Customizing the gridlines
ax.grid(True, which='major', linestyle=':', linewidth=1, color='grey', alpha=0.7)
# Tweaking x and y axes ticks
ax.set_xticks(range(1, 12))
ax.set_xticklabels([beta[i] for i in range(1, 12)], fontsize=34)
ax.tick_params(labelsize=34)
ax.tick_params(axis='y')
# Show the plot
plt.tight_layout()
if args.save:
    plt.savefig(f"plots/boxplot_costs_reb_{args.cat}_cat.pdf", format='pdf')
    plt.savefig(f"plots/boxplot_costs_reb_{args.cat}_cat.png", format='png')
plt.show()

# FAILURE COSTS

# Setting a nice aesthetic for the plots
sns.set(style="whitegrid")
# Creating a figure and axis with higher resolution
fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
# Using a single custom color
box_color = sns.color_palette("viridis", 11)[2]
# Creating the boxplot with custom settings
box = ax.boxplot(cost_fail, patch_artist=True, notch=False, vert=True, widths=0.6)
# Customizing each box with the same color
for patch in box['boxes']:
    patch.set_facecolor(box_color)
    patch.set_edgecolor('black')
    patch.set_alpha(0.8)
    patch.set_linewidth(1.5)
# Customizing whiskers, caps, and medians
for whisker in box['whiskers']:
    whisker.set(color='black', linewidth=1.5, linestyle='--')
for cap in box['caps']:
    cap.set(color='black', linewidth=1.5)
for median in box['medians']:
    median.set(color='gold', linewidth=1.5)
for flier in box['fliers']:
    flier.set(marker='o', color='red', alpha=0.75)
ax.set_xlabel(r'$\beta$', fontsize=36)
ax.set_ylabel("Failure rate [%]", fontsize=36)
# Customizing the gridlines
ax.grid(True, which='major', linestyle=':', linewidth=1, color='grey', alpha=0.7)
# Tweaking x and y axes ticks
ax.set_xticks(range(1, 12))
ax.set_xticklabels([beta[i] for i in range(1, 12)], fontsize=34)
ax.tick_params(labelsize=34)
ax.tick_params(axis='y')
# Show the plot
plt.tight_layout()
if args.save:
    plt.savefig(f"plots/boxplot_costs_fails_{args.cat}_cat.pdf", format='pdf')
    plt.savefig(f"plots/boxplot_costs_fails_{args.cat}_cat.png", format='png')
plt.show()

# BIKES COSTS

initial_bikes = np.load(f'results/initial_bikes_{args.cat}_cat_10seeds.npy').transpose()[:, 0]
mean = np.mean(initial_bikes)
std_dev = np.std(initial_bikes)
# Setting a nice aesthetic for the plots
sns.set(style="whitegrid")
# Creating a figure and axis with higher resolution
fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
# Plot the mean as a horizontal line
ax.axhline(mean, color='gold', linestyle='--', linewidth=2, label="Mean")
# Plot confidence intervals as shaded areas
ax.fill_between([0.5, 11.5], mean - 1.96*std_dev, mean + 1.96*std_dev, color='gold', alpha=0.2)
# Using a single custom color
box_color = sns.color_palette("viridis", 11)[2]
# Creating the boxplot with custom settings
box = ax.boxplot(cost_bikes, patch_artist=True, notch=False, vert=True, widths=0.6)
# Customizing each box with the same color
for patch in box['boxes']:
    patch.set_facecolor(box_color)
    patch.set_edgecolor('black')
    patch.set_alpha(0.8)
    patch.set_linewidth(1.5)
# Customizing whiskers, caps, and medians
for whisker in box['whiskers']:
    whisker.set(color='black', linewidth=1.5, linestyle='--')
for cap in box['caps']:
    cap.set(color='black', linewidth=1.5)
for median in box['medians']:
    median.set(color='gold', linewidth=1.5)
for flier in box['fliers']:
    flier.set(marker='o', color='red', alpha=0.75)
ax.set_xlabel(r'$\beta$', fontsize=36)
ax.set_ylabel("Number of vehicles", fontsize=36)
# Customizing the gridlines
ax.grid(True, which='major', linestyle=':', linewidth=1, color='grey', alpha=0.7)
# Tweaking x and y axes ticks
ax.set_xticks(range(1, 12))
ax.set_xticklabels([beta[i] for i in range(1, 12)], fontsize=34)
ax.tick_params(labelsize=34)
ax.tick_params(axis='y')
# Show the plot
plt.tight_layout()
if args.save:
    plt.savefig(f"plots/boxplot_costs_bikes_{args.cat}_cat.pdf", format='pdf')
    plt.savefig(f"plots/boxplot_costs_bikes_{args.cat}_cat.png", format='png')
plt.show()
