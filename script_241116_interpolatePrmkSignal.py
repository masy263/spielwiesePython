#!/bin/python3

import matplotlib.pyplot as plt
import numpy as np

plt.style.use('dark_background')

inpFileImag = '/home/markus/Arbeit/2024-10-22_prmkSimSampleInput/samples_input_imag.dat'
inpFileReal = '/home/markus/Arbeit/2024-10-22_prmkSimSampleInput/samples_input_real.dat'
outFileImag = '/home/markus/Arbeit/2024-10-22_prmkSimSampleInput/samples_input_imag_Nos15.dat'
outFileReal = '/home/markus/Arbeit/2024-10-22_prmkSimSampleInput/samples_input_real_Nos15.dat'

print("read input file imag")
inpSigImag = np.genfromtxt(inpFileImag, delimiter='\n')
print("read input file real")
inpSigReal = np.genfromtxt(inpFileReal, delimiter='\n')

interpFactor = 15

print("interpolate imag data")
xInpImag   = np.arange(0, len(inpSigImag)) * interpFactor
xOutImag   = np.arange(0, np.max(xInpImag))
outSigImag = np.interp(xOutImag, xInpImag, inpSigImag)

print("interpolate real data")
xInpReal   = np.arange(0, len(inpSigReal)) * interpFactor
xOutReal   = np.arange(0, np.max(xInpReal))
outSigReal = np.interp(xOutReal, xInpReal, inpSigReal)

print("export imag data")
np.savetxt(outFileImag, outSigImag, fmt='%d', delimiter='\n')

print("export real data")
np.savetxt(outFileReal, outSigReal, fmt='%d', delimiter='\n')

# plt.plot(x2, y2, 'o', color='yellow')
# plt.plot(x1, y1, '-', color='red')
# plt.show()
