#!/bin/python3

# python info:
# a // b --> integer division

import numpy as np
import matplotlib.pyplot as plt

plt.style.use('dark_background')

inpPath   = '/home/markus/Git-Repos/adrv9361z7035ccbobCmos/verilog/.sim/'
inpFileMf = 'mfOutput.csv'

# +++ begin: handle mf data +++

inpDataMf = np.genfromtxt(inpPath+inpFileMf, delimiter=',')
nLines    = len(inpDataMf)
nClmns    = len(inpDataMf[0])
print("size of :: %s :: lines: %d // columns: %d" % (inpFileMf, nLines, nClmns))
nClmns    = nClmns // 2
dataMf    = np.zeros((nLines, nClmns), dtype='complex')
idxClmn   = 0

while idxClmn < nClmns:
  dataMf[:,idxClmn] = inpDataMf[:,idxClmn * 2] + inpDataMf[:,(idxClmn * 2 + 1)] * 1j
  idxClmn           = idxClmn + 1

plt.plot(np.real(dataMf[:,0]), np.imag(dataMf[:,0]), 'y*-')
plt.show()

# +++++ end: rearange mf data +++

