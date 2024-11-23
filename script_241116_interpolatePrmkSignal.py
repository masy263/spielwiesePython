#!/bin/python3

import matplotlib.pyplot as plt
import numpy as np
import time

plt.style.use('dark_background')

tStart = time.time()
tStep = time.time()

inpNos       = 5
outNos       = 15
interpFactor = outNos / inpNos
scaleFactor  = 1500

inpPath = '/home/markus/Arbeit/2024-06-21_TestsignalPrmkUL/Nos5/'
# inpPath = './'
outPath = '/home/markus/Arbeit/2024-11-15_adcInputData/.sim/'

# inpFileNameImag = inpPath + 'imagInp.dat'
# inpFileNameReal = inpPath + 'imagInp.dat'
inpFileNameImag = inpPath + 'samples_input_imag.dat'
inpFileNameReal = inpPath + 'samples_input_real.dat'
outFileNameImag = outPath + 'adcImag.dat'
outFileNameReal = outPath + 'adcReal.dat'


tStep = time.time()
tTotal = time.time() - tStart
print("%4d :: read input file imag" % tTotal)
inpSigImag = np.genfromtxt(inpFileNameImag, delimiter='\n')
tStep = time.time() - tStep
print("     :: exec time: %d" % tStep)

tStep = time.time()
tTotal = time.time() - tStart
print("%4d :: read input file real" % tTotal)
inpSigReal = np.genfromtxt(inpFileNameReal, delimiter='\n')
tStep = time.time() - tStep
print("     :: exec time: %d" % tStep)

tStep = time.time()
tTotal = time.time() - tStart
print("%4d :: determine inp max magnitude" % tTotal)
maxImag = np.max(np.abs(inpSigImag))
maxReal = np.max(np.abs(inpSigReal))
maxMagn = np.max(np.array([maxImag, maxReal]))
print("     :: max magnitude imag: %d" % maxImag)
print("     :: max magnitude real: %d" % maxReal)
print("     :: max magnitude:      %d" % maxMagn)
tStep = time.time() - tStep
print("     :: exec time: %d" % tStep)

tStep = time.time()
tTotal = time.time() - tStart
print("%4d :: scale imag data" % tTotal)
inpSigImag = inpSigImag * scaleFactor
inpSigImag = inpSigImag // maxMagn
tStep = time.time() - tStep
print("     :: exec time: %d" % tStep)

tStep = time.time()
tTotal = time.time() - tStart
print("%4d :: scale real data" % tTotal)
inpSigReal = inpSigReal * scaleFactor
inpSigReal = inpSigReal // maxMagn
tStep = time.time() - tStep
print("     :: exec time: %d" % tStep)

tStep = time.time()
tTotal = time.time() - tStart
print("%4d :: interpolate imag data" % tTotal)
xInpImag   = np.arange(0, len(inpSigImag)) * interpFactor
xOutImag   = np.arange(0, np.max(xInpImag))
outSigImag = np.interp(xOutImag, xInpImag, inpSigImag)
tStep = time.time() - tStep
print("     :: exec time: %d" % tStep)

tStep = time.time()
tTotal = time.time() - tStart
print("%4d :: interpolate real data" % tTotal)
xInpReal   = np.arange(0, len(inpSigReal)) * interpFactor
xOutReal   = np.arange(0, np.max(xInpReal))
outSigReal = np.interp(xOutReal, xInpReal, inpSigReal)
tStep = time.time() - tStep
print("     :: exec time: %d" % tStep)

# tStep = time.time()
# tTotal = time.time() - tStart
# print("%4d :: generate imag output string" % tTotal)
# lenOutImag = len(outSigImag)
# outStrImag = "{:<lenOutImag*10}".format(" ")
# idxOutImag = 0
# waypoint = 1

# print("percentage: 0", end='')
# while idxOutImag < lenOutImag:
#   outStrImag = outStrImag + str(int(outSigImag[idxOutImag])) + '\n'
#   idxOutImag = idxOutImag + 1
#   if (idxOutImag * 100 / lenOutImag) > waypoint:
#     print(" :: %d" % waypoint, end='')
#     waypoint = waypoint + 1

# print(" :: 100")

tStep = time.time()
tTotal = time.time() - tStart
print("%4d :: export imag output file" % tTotal)

# with open(outFileNameImag, "w") as outFileImag:
#     outFileImag.write("%s" % outStrImag)

np.savetxt(outFileNameImag, outSigImag, fmt='%d', delimiter='\n')
tStep = time.time() - tStep
print("     :: exec time: %d" % tStep)

tStep = time.time()
tTotal = time.time() - tStart
print("%4d :: export real output file" % tTotal)
np.savetxt(outFileNameReal, outSigReal, fmt='%d', delimiter='\n')
tStep = time.time() - tStep
print("     :: exec time: %d" % tStep)

# plt.plot(x2, y2, 'o', color='yellow')
# plt.plot(x1, y1, '-', color='red')
# plt.show()
