#!/bin/python3

from fct_diy import *
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('dark_background')

nOs      = 3
rollOff  = 0.3
nPeriods = 2

rrcFilter  = fct_rrcGen(nOs, rollOff, nPeriods=3)
rcFilter   = fct_rcGen(nOs, rollOff, nPeriods=3)
diffRc     = rrcFilter - rcFilter
sqrtRc     = np.sqrt(np.abs(rcFilter))
diffSqrtRc = sqrtRc - np.sqrt(np.abs(rrcFilter))

fig, ax = plt.subplots(4,1)
ax[0].plot(np.arange(0, len(rrcFilter)), rrcFilter, 'o-', color='yellow')
ax[1].plot(np.arange(0, len(rcFilter)), rcFilter, 'o-', color='white')
ax[2].plot(np.arange(0, len(diffRc)), diffRc, 'o-', color='green')
ax[2].plot(np.arange(0, len(diffSqrtRc)), diffSqrtRc, 'o-', color='blue')
ax[3].plot(np.arange(0, len(sqrtRc)), sqrtRc, 'o-', color='white')
plt.show()

