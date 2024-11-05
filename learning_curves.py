import numpy as np
import matplotlib.pyplot as plt

# Sample data
data = np.random.randn(100)  # Replace with your own vector of numbers

# Calculate mean and standard deviation
mean = np.mean(data)
std_dev = np.std(data)

# Set up the figure
plt.figure(figsize=(8, 6))

# Plot data points (optional, to visualize data)
plt.plot(data, 'o', alpha=0.5, label="Data points")

# Plot the mean as a horizontal line
plt.axhline(mean, color='blue', linestyle='-', linewidth=2, label="Mean")

# Plot confidence intervals as shaded areas
plt.fill_between(range(len(data)), mean - std_dev, mean + std_dev, color='blue', alpha=0.2, label="±1 Std Dev")
plt.fill_between(range(len(data)), mean - 2 * std_dev, mean + 2 * std_dev, color='blue', alpha=0.1, label="±2 Std Dev")

# Add labels and legend
plt.xlabel("Index")
plt.ylabel("Value")
plt.title("Mean with Confidence Intervals (Standard Deviations)")
plt.legend()

plt.show()
