#!/bin/python3

from fct_diy import *
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('dark_background')

# inpPath    = '/home/markus/Git-Repos/adrv9361z7035ccbobCmos/verilog/.sim/'
inpFileMif = '/home/markus/Git-Repos/adrv9361z7035ccbobCmos/verilog/mif/mogup_lval.mif'
inpFileSim = '/home/markus/Git-Repos/adrv9361z7035ccbobCmos/verilog/.sim/demodLValOut.hex'
# inpFileMif = 'test.csv'

# +++ begin: handle mif data +++

with open(inpFileMif, "r") as fidMif:
  inpDataMifHex = fidMif.read()
fidMif.closed

inpDataMifHex = inpDataMifHex.replace("\n", ",")
inpDataMifHex = inpDataMifHex.replace(" ", "")
inpDataMifHex = inpDataMifHex.split(",")
inpDataMifHex = inpDataMifHex[0:len(inpDataMifHex) - 1]
inpDataMifDec = np.zeros((len(inpDataMifHex),1), dtype=int)
idxMifData    = 0

while idxMifData < len(inpDataMifHex):
  inpDataMifDec[idxMifData] = int(inpDataMifHex[idxMifData], 16)
  idxMifData = idxMifData + 1

inpDataMifDec = fct_complementOnTwo2int(inpDataMifDec)
inpDataMifDec = inpDataMifDec.reshape(len(inpDataMifDec) // 2, 2)

print("[script_241015_lValValidation] lVal data points from mif file: %d" % len(inpDataMifDec))

np.savetxt("outputData/mif.csv", inpDataMifDec, fmt='%4d', delimiter=',')

# +++ begin: handle sim data +++

with open(inpFileSim, "r") as fidSim:
  inpDataSimHex = fidSim.read()
fidSim.closed

inpDataSimHex = inpDataSimHex.replace("\n", ",")
inpDataSimHex = inpDataSimHex.replace(" ", "")
inpDataSimHex = inpDataSimHex.split(",")
inpDataSimHex = inpDataSimHex[0:len(inpDataSimHex) - 1]
inpDataSimDec = np.zeros((len(inpDataSimHex),1), dtype=int)
idxSimData    = 0

while idxSimData < len(inpDataSimHex):
  inpDataSimDec[idxSimData] = int(inpDataSimHex[idxSimData], 16)
  idxSimData = idxSimData + 1

inpDataSimDec = fct_complementOnTwo2int(inpDataSimDec)
inpDataSimDec = inpDataSimDec.reshape(len(inpDataSimDec) // 2, 2)

print("[script_241015_lValValidation] lVal data points from sim file: %d" % len(inpDataSimDec))

np.savetxt("outputData/sim.csv", inpDataSimDec, fmt='%4d', delimiter=',')

# +++ begin: plot +++

plotRangeStart = 0
plotRangeEnd   = 72
x              = np.arange(0,plotRangeEnd - plotRangeStart)
lValMif0plot   = inpDataMifDec[:,0][plotRangeStart:plotRangeEnd]
lValMif1plot   = inpDataMifDec[:,1][plotRangeStart:plotRangeEnd]
lValSim0plot   = inpDataSimDec[:,0][plotRangeStart:plotRangeEnd]
lValSim1plot   = inpDataSimDec[:,1][plotRangeStart:plotRangeEnd]

fig, ax = plt.subplots(2, 1)

ax[0].set_title("lVals from MIF %d...%d" % (plotRangeStart, plotRangeEnd - 1))
ax[0].set_xlabel('n')
ax[0].set_ylabel('Value')
ax[0].plot(x, lValMif0plot, '*-', color="yellow", label="My Line 1")
ax[0].plot(x, lValMif1plot, '.-', color="green", label="My Line 2")
ax[0].grid()

ax[1].set_title("lVals from SIM %d...%d" % (plotRangeStart, plotRangeEnd - 1))
ax[1].set_xlabel('n')
ax[1].set_ylabel('Value')
ax[1].plot(x, lValSim0plot, '*-', color="yellow", label="My Line 1")
ax[1].plot(x, lValSim1plot, '.-', color="green", label="My Line 2")
ax[1].grid()

plt.show()

