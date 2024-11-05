import numpy as np
import matplotlib.pyplot as plt

curve = np.load('results/learning_curve_5_cat_0.0_123.npy')

plt.plot(curve)
plt.show()