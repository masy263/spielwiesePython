#!/bin/python3

import numpy as np
import matplotlib.pyplot as plt

R  = 2
phiRes = 3
phi = np.arange(0, 90 + phiRes, phiRes) / 180 * np.pi

# print(phi)

x  = R * (1 - np.cos(phi))
y  = np.sqrt(2 * R * x - x**2)

A_sum = np.arccos(1 - x / R) * R**2
A_inv = (R - x) * y
A     = A_sum - A_inv

plt.style.use('dark_background')

plt.plot(x, A, 'y', x, A_sum, 'w*', x, A_inv, 'b--')
plt.show()

