#!/bin/python3

# script_241204_cfoEstimation

from fct_diy import *
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('dark_background')

inpPath = "./outputData/"
inpFile = "tc000adc_payload"

data = np.transpose(np.int16(fct_readCsv(inpPath+inpFile+".csv") // 1))
data = data[0]
imag = fct_complementOnTwo2int(data[0::4] * 256 + data[1::4])
real = fct_complementOnTwo2int(data[2::4] * 256 + data[3::4])
cplx = real + imag * 1j

strCplx = cplx
strCplx = [str(elem) for elem in strCplx]
strCplx = ''.join(strCplx)
strCplx = strCplx.replace('[', ')')
strCplx = strCplx.replace(']', '(')
strCplx = strCplx.replace(')', '\n')
strCplx = strCplx.replace('(', '')

with open(inpPath+inpFile+"_cplx.csv", "w") as fid:
  fid.write("%s" % strCplx)

maxEAbs = 100
chosenPhase = 0

idxPP = 0
while idxPP < 15:
  phase = cplx[idxPP::15]
  cAbs  = np.abs(phase)
  mAbs  = np.sum(cAbs) / len(phase)
  eAbs  = np.abs(cAbs / mAbs - 1) * 100

  if maxEAbs > np.sum(eAbs) / len(phase):
    chosenPhase = idxPP
    maxEAbs     = np.sum(eAbs) / len(phase)

  idxPP = idxPP + 1

print("[script_241204_cfoEstimation] choose phase idx: %d :: mean failure %f" % (chosenPhase, maxEAbs))

pPhase = cplx[chosenPhase::15]
phiErr = np.zeros(len(pPhase))
idx    = 0

while idx < len(pPhase):
  tmp = pPhase[idx]

  while np.abs(tmp) < 0.001:
    idx = idx + 1
    tmp = pPhase[idx]

  if np.real(tmp) < 0:
    tmp = tmp * np.exp(np.pi * 1j)
  if np.imag(tmp) < 0:
    tmp = tmp * np.exp(np.pi / 2 * 1j)

  phiErr[idx]  = np.pi / 4 - np.asin(np.imag(tmp) / np.abs(tmp))
  pPhase[idx:] = pPhase[idx:] * np.exp(phiErr[idx] * 1j)

  idx = idx + 1

phiErrDevel = np.zeros(len(phiErr))
idx = 0

while idx < len(phiErr):
  phiErrDevel[idx] = np.sum(phiErr[:idx]) / idx
  idx = idx + 1

plt.plot(phiErrDevel)

fixPhi = np.sum(phiErr) / len(phiErr) / 15
cfo = fixPhi *13500000 / 2 / np.pi

print("[script_241204_cfoEstimation] estimated mean cfo [Hz]: %d" % int(cfo))
print("[script_241204_cfoEstimation] phase shift per sample: %f" % fixPhi)

cplx = real + imag * 1j

idx = 0
while idx < len(cplx):
  tmp = (idx * fixPhi) % (2 * np.pi)
  cplx[idx] = cplx[idx] * np.exp(tmp * 1j)
  idx = idx + 1

imag = np.int16(np.imag(cplx))
real = np.int16(np.real(cplx))

pltLen  = len(imag)
pPhase  = 0
fig, ax = plt.subplots(3,5)

while pPhase < 15:
  pltLine = pPhase // 5
  pltClmn = pPhase % 5
  ax[pltLine][pltClmn].plot(real[pPhase:pltLen][::15], imag[pPhase:pltLen][::15], '*', color='yellow')

  pPhase = pPhase + 1

plt.show()

