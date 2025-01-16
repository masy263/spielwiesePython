#!/bin/python3
# script_250107_simSymbolPlot

from fct_diy import *
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('dark_background')

inpPath     = '/home/markus/Git-Repos/adrv9361z7035ccbobCmos/verilog/simOut/'
inpFileImag = 'symbolImag.dat'
inpFileReal = 'symbolReal.dat'
outFile     = 'symbols.csv'

inpImag = np.genfromtxt(inpPath + inpFileImag, delimiter='\n')
inpReal = np.genfromtxt(inpPath + inpFileReal, delimiter='\n')

plt.plot(inpReal, inpImag, '*', color='yellow')
plt.suptitle('Symbols')

with open(inpPath + outFile, "w") as fid:
  idx = 0

  while idx < len(inpReal):
    imag = inpImag[idx]
    real = inpReal[idx]

    if(imag < 0):
      fid.write("%d-%di\n" % (real, -imag))
    else:
      fid.write("%d+%di\n" % (real, imag))

    idx = idx + 1

# lVals

inpFileLVal0 = 'lVal0.dat'
inpFileLVal1 = 'lVal1.dat'
lVal0        = np.genfromtxt(inpPath + inpFileLVal0, delimiter='\n')
lVal1        = np.genfromtxt(inpPath + inpFileLVal1, delimiter='\n')
lVals        = np.zeros(2*len(lVal0))
lVals[0::2]  = lVal0
lVals[1::2]  = lVal1
numBytes     = len(lVals) // 8
idx          = 0

while idx < numBytes:
  lValByte = lVals[idx*8:idx*8+7]
  lValByte = lValByte[::-1]
  lValByte = (lValByte < 0) * 1
  lValByte = fct_bits2Byte(lValByte)
  print("%4d" % lValByte, end='')
  idx = idx + 1
  
  if idx % 16 == 0:
    print()

print()




plt.show()