#!/bin/python3

from fct_diy import *
import numpy as np
import matplotlib.pyplot as plt

inpPath         = '/home/markus/Arbeit/2024-11-04_debuggingSimulation/.simPrmk_241104a/'
inpFileAccu0ram = 'accu0_ram.dat.bak241104a'

plt.style.use('dark_background')

#  1176,   207,    0,     0,      0,      0
#    39, -1110, 1176,   207,   1176,    207
#    46,  -551,   39, -1110,  16383, 261034
#  1528,   727,   46,  -551,  16383, 261593

xDec = np.array([1176, 207, 39, -1110, 16383, 261034])
idx = 0

while idx < len(xDec):
  xBin = fct_uint2bin(fct_int2complementOnTwo(xDec[idx],18))
  print("%d :: %d" % (xDec[idx], xBin))
  idx = idx + 1
print((xBin))
