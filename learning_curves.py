import numpy as np
import matplotlib.pyplot as plt

# Simulate reward data across different seeds
# Assume 10 seeds and 100 episodes
# Replace this with actual reward data from your experiments
num_seeds = 10
num_episodes = 100
rewards = np.random.rand(num_seeds, num_episodes) * 10  # Simulated rewards

# Calculate the mean and standard deviation across seeds for each episode
mean_rewards = np.mean(rewards, axis=0)
std_rewards = np.std(rewards, axis=0)

# Plot the learning curve
plt.figure(figsize=(10, 6))
episodes = np.arange(num_episodes)

# Plot the mean reward
plt.plot(episodes, mean_rewards, color="blue", label="Mean Reward")

# Plot the confidence interval (mean ± std deviation)
plt.fill_between(episodes, mean_rewards - std_rewards, mean_rewards + std_rewards,
                 color="blue", alpha=0.2, label="±1 Std Dev")

# Labels and legend
plt.xlabel("Episode")
plt.ylabel("Reward")
plt.title("Learning Curve with Confidence Intervals (Std Dev)")
plt.legend()

plt.show()