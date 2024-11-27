# determine spectrum including resolution ans axis

import numpy as np

def fct_spectrum(sig, fSamp, fftRes=1024):
  spec  = np.abs(np.fft.fft(sig, n=fftRes))
  spec  = np.append(spec[len(spec) // 2:], spec[0:len(spec) // 2])
  fAxis = (np.arange(0,fftRes) / fftRes - 0.5) * fSamp
  ret   = np.array([fAxis, spec])

  return ret

# testbench

# import matplotlib.pyplot as plt

# plt.style.use('dark_background')

# fSamp = 100

# t = np.arange(0, 32, 1 / fSamp)
# f = 0.1
# a = 10
# vz = 1
# sig = a * np.sin(2*np.pi*f*t)

# while f < 20:
#   f = f + 0.02
#   a = a + vz * 0.5
#   if a < 0:
#     vz = vz * -1
#   sig = sig + a * np.sin(2*np.pi*f*t)

# spec = fct_spectrum(sig, fSamp, 16)
# xAxis = spec[0]
# yAxis = spec[1]

# plt.plot(xAxis, yAxis)
# plt.show()