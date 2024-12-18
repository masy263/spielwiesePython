#!/bin/python3

# script_241204_cfoEstimation

from fct_diy import *
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('dark_background')

inpPath      = "/home/markus/Arbeit/2024-11-21_ibnHdl/tcRawData/"
idxFileFirst = 0
idxFileLast  = 29
idxFile      = idxFileFirst

while idxFile < idxFileLast + 1:

  # read tc adc input file

  inpFile = "tc"+str("%03d" % idxFile)+"adc_payload"
  data    = np.transpose(np.int16(fct_readCsv(inpPath+inpFile+".csv") // 1))
  data    = data[0]
  imag    = fct_complementOnTwo2int(data[0::4] * 256 + data[1::4])
  real    = fct_complementOnTwo2int(data[2::4] * 256 + data[3::4])
  cplx    = real + imag * 1j

  # export complex symbols

  strCplx = cplx
  strCplx = [str(elem) for elem in strCplx]
  strCplx = ''.join(strCplx)
  strCplx = strCplx.replace('[', ')')
  strCplx = strCplx.replace(']', '(')
  strCplx = strCplx.replace(')', '\n')
  strCplx = strCplx.replace('(', '')

  with open(inpPath+inpFile+"_cplx.csv", "w") as fid:
    fid.write("%s" % strCplx)

  # search for polyphase which fits the symbol sequence best

  maxEAbs     = 100 # max magnitude error
  chosenPhase = 0

  idxPP = 0
  while idxPP < 15:
    phase = cplx[idxPP::15]
    cAbs  = np.abs(phase) # magnitudes
    mAbs  = np.sum(cAbs) / len(phase) # mean magnitude
    eAbs  = np.abs(cAbs / mAbs - 1) * 100 # magnitude error percentage

    if maxEAbs > np.sum(eAbs) / len(phase):
      chosenPhase = idxPP
      maxEAbs     = np.sum(eAbs) / len(phase)

    idxPP = idxPP + 1

  print("[script_241204_cfoEstimation] choose phase idx: %d :: mean failure %f" % (chosenPhase, maxEAbs))

  # determine phase error

  pPhase      = cplx[chosenPhase::15]
  phiErr      = np.zeros(len(pPhase))
  phiErrOrig  = np.zeros(len(pPhase))
  phiErrDevel = np.zeros(len(pPhase)+1)
  resMA       = 100
  phiErrMA    = np.zeros(len(phiErr)-resMA)
  idx         = 0

  while idx < len(pPhase):
    tmp = pPhase[idx]

    while np.abs(tmp) < 0.001:
      idx = idx + 1
      tmp = pPhase[idx]

    if np.real(tmp) < 0:
      tmp = tmp * np.exp(np.pi * 1j)
    if np.imag(tmp) < 0:
      tmp = tmp * np.exp(np.pi / 2 * 1j)

    phiErrOrig[idx] = np.pi / 4 - np.asin(np.imag(tmp) / np.abs(tmp))

    if np.abs((np.abs(tmp) / mAbs) - 1) > 0.66: # ignore sample that don't fit mean magnitude
      phiErr[idx] = phiErrDevel[idx]
    else:
      phiErr[idx] = phiErrOrig[idx]

    pPhase[idx:]       = pPhase[idx:] * np.exp(phiErr[idx] * 1j)
    phiErrDevel[idx+1] = np.sum(phiErr[:idx]) / (idx + 1)

    if idx >= resMA:
      phiErrMA[idx-resMA] = np.sum(phiErr[idx-resMA:idx]) / resMA

    idx = idx + 1

  phiErr      = phiErr[1:len(phiErr)]
  phiErrOrig  = phiErrOrig[1:len(phiErrOrig)]
  phiErrDevel = phiErrDevel[2:len(phiErrDevel)]
  fixPhi      = np.sum(phiErr) / len(phiErr) / 15
  cfo         = fixPhi *13500000 / 2 / np.pi

  print("[script_241204_cfoEstimation] estimated mean cfo [Hz]: %d" % int(cfo))
  print("[script_241204_cfoEstimation] phase shift per sample: %f" % fixPhi)

  # rebuild complex signal and apply correction angle

  cplx = real + imag * 1j

  idx = 0
  while idx < len(cplx):
    tmp = (idx * fixPhi) % (2 * np.pi)
    cplx[idx] = cplx[idx] * np.exp(tmp * 1j)
    idx = idx + 1

  pltLen  = len(imag)
  #pPhase   = 0
  #fig, ax0 = plt.subplots(3,5)

  #while pPhase < 15:
  #  pltLine = pPhase // 5
  #  pltClmn = pPhase % 5

  #  ax1[pltLine][pltClmn].plot(real[pPhase:pltLen][::15], imag[pPhase:pltLen][::15], '*', color='yellow')

  #  pPhase = pPhase + 1

  #plt.show()

  imagNeu = np.int16(np.imag(cplx))
  realNeu = np.int16(np.real(cplx))

  pltLenNeu  = len(imagNeu)
  #pPhase   = 0
  #fig, ax1 = plt.subplots(3,5)

  #while pPhase < 15:
  #  pltLine = pPhase // 5
  #  pltClmn = pPhase % 5

  #  ax1[pltLine][pltClmn].plot(realNeu[pPhase:pltLenNeu][::15], imagNeu[pPhase:pltLenNeu][::15], '*', color='yellow')

  #  pPhase = pPhase + 1

  #plt.show()

  # generate overview plot

  fig = plt.figure(layout='constrained', figsize=(10, 4)) 
  subfigs = fig.subfigures(1, 2, wspace=0.07, width_ratios=[1, 2])
  subfigs[0].suptitle(("Constellation of Poly Phase: %d (Record: %d)" % (chosenPhase, idxFile)), fontsize="x-large")
  axConst = subfigs[0].subplots(2,1)
  axConst[0].set_title('BEFORE')
  axConst[0].set_xlabel('real')
  axConst[0].set_ylabel('imag')
  axConst[0].plot(real[chosenPhase:pltLen][::15], imag[chosenPhase:pltLen][::15], '*', color='yellow')
  axConst[1].set_title('AFTER')
  axConst[1].set_xlabel('real')
  axConst[1].set_ylabel('imag')
  axConst[1].plot(realNeu[chosenPhase:pltLenNeu][::15], imagNeu[chosenPhase:pltLenNeu][::15], '*', color='yellow')
  subfigs[1].suptitle("Incremental Phase Offset", fontsize="x-large")
  axPhiErr = subfigs[1].subplots(3,1)
  axPhiErr[0].set_title('Phase Offset')
  axPhiErr[0].plot(phiErrOrig, color='white')
  axPhiErr[0].plot(phiErr, color='yellow')
  axPhiErr[1].set_title('Phase Offset Continous Average')
  axPhiErr[1].plot(phiErrDevel, color='white')
  axPhiErr[2].set_title('Phase Offset Moving Average')
  axPhiErr[2].plot(phiErrMA, color='orange')
  plt.show()

  # increment file index

  idxFile = idxFile + 1
