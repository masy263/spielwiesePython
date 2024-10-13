import matplotlib.pyplot as plt
import numpy as np
import sys

from fct_diy import *

plt.style.use('dark_background')

x = np.arange(0, 2 * np.pi, 5E-2)
y1 = np.sin(1 * x)
y2 = np.sin(3 * x)
y3 = np.sin(7 * x)
x = x / max(x);
fig, ax = plt.subplots(2, 1)
ax[0].set_title('Freq = 1 Hz, 3 Hz')
ax[0].set_xlabel('Zeit [s]')
ax[0].set_ylabel('Amplitude')
ax[0].plot(x, y1, '*-', color="white", label="My Line 1")
ax[0].plot(x, y2, '.-', color="green", label="My Line 2")
ax[0].grid()
ax[1].set_title('Freq = 7 Hz')
ax[1].set_xlabel('Zeit [s]')
ax[1].set_ylabel('Amplitude')
ax[1].plot(x, y3, 'o-', color="yellow", label="My Line 3")
ax[1].grid()

plt.show()

# fidOut = open("output.txt", "w")

# it = 1;
# bits = 0;

# while bits < 64:
#   bits = fct_determineBitWidth(it - 1);
#   print("%20d >> %2d Bits\n" % (it - 1, bits), end = '', file=fidOut);
#   it = it * 2;

# fidOut.close()
