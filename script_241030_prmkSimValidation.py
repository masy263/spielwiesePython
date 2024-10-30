#!/bin/python3

from fct_diy import *
import numpy as np
import matplotlib.pyplot as plt

calcCfo     = 1
calcSymbols = 1

plt.style.use('dark_background')

inpPath         = '/home/markus/Git-Repos/adrv9361z7035ccbobCmos/verilog/.simPrmk_241023b/'
inpFileCfos     = 'freq_out.dat'
inpFileHest     = 'hest_out.dat'
inpFileInfoBits = 'info_bit_out.dat'
inpFileInpSampI = 'samples_input_real.dat'
inpFileInpSampQ = 'samples_input_imag.dat'
inpFileLVals    = 'lval_out.dat'
inpFileSymbols  = 'sym_out.dat'

# +++ begin: cfo output +++

if calcCfo > 0:
  inpCfos = np.genfromtxt(''.join(inpPath+inpFileCfos), delimiter=',')
  inpCfos = inpCfos[0:len(inpCfos):2]
  xCfos   = np.arange(0,len(inpCfos))

  fig, pltCfos = plt.subplots()
  pltCfos.plot(xCfos, inpCfos, '-', color='yellow')
  pltCfos.set_title('CFO')

  expectedCfos = [-165, -175, -180, -189, -196]
  idxCfo       = 0

  print("[script_241030_prmkSimValidation] cfo analysis")
  print(" :: idx | expected | found | diff")
  print(" :: ----+----------+-------+-----")

  while idxCfo < 5:
    print(" :: %3d | %8d | %5d | %4d" % (idxCfo, expectedCfos[idxCfo], inpCfos[idxCfo], inpCfos[idxCfo] - expectedCfos[idxCfo]))
    idxCfo = idxCfo + 1

# +++++ end: cfo output +++

if calcSymbols > 0:

  inpSymbols     = np.genfromtxt(''.join(inpPath+inpFileSymbols), delimiter=',')
  inpSymbolsReal = inpSymbols[0::3]
  inpSymbolsImag = inpSymbols[1::3]
  pltNumberSym   = 108
  pltSymStartIdx = 0
  pltSymEndIdx   = pltSymStartIdx + pltNumberSym - 1

  if pltSymEndIdx > len(inpSymbolsImag) - 1:
    pltSymEndIdx = len(inpSymbolsImag) - 1
    print("[script_241030_prmkSimValidation] reduced pltSymEndIdx to %d" % pltSymEndIdx)

  fig, pltCfos = plt.subplots()
  pltCfos.plot(inpSymbolsReal[pltSymStartIdx:pltSymEndIdx], inpSymbolsImag[pltSymStartIdx:pltSymEndIdx], '*', color='yellow')
  pltCfos.set_title('Symbols')

# +++ begin: symbol output +++

# +++++ end: symbol output +++

# +++ begin: plot +++

plotFlag = calcCfo + calcSymbols

if plotFlag > 0:
  plt.show()

# plotRangeStart = 0
# plotRangeEnd   = 72
# x              = np.arange(0,plotRangeEnd - plotRangeStart)
# lValMif0plot   = inpDataMifDec[:,0][plotRangeStart:plotRangeEnd]
# lValMif1plot   = inpDataMifDec[:,1][plotRangeStart:plotRangeEnd]
# lValSim0plot   = inpDataSimDec[:,0][plotRangeStart:plotRangeEnd]
# lValSim1plot   = inpDataSimDec[:,1][plotRangeStart:plotRangeEnd]
# 
# fig, ax = plt.subplots(2, 1)
# 
# ax[0].set_title("lVals from MIF %d...%d" % (plotRangeStart, plotRangeEnd - 1))
# ax[0].set_xlabel('n')
# ax[0].set_ylabel('Value')
# ax[0].plot(x, lValMif0plot, '*-', color="yellow", label="My Line 1")
# ax[0].plot(x, lValMif1plot, '.-', color="green", label="My Line 2")
# ax[0].grid()
# 
# ax[1].set_title("lVals from SIM %d...%d" % (plotRangeStart, plotRangeEnd - 1))
# ax[1].set_xlabel('n')
# ax[1].set_ylabel('Value')
# ax[1].plot(x, lValSim0plot, '*-', color="yellow", label="My Line 1")
# ax[1].plot(x, lValSim1plot, '.-', color="green", label="My Line 2")
# ax[1].grid()
# 
# plt.show()

