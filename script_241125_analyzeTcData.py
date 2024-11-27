#!/bin/python3

# tb_241125_cutTcData

# REF SIGNAL ATTRIBUTES:
#   IMAG :: min Magintude: -5372.000000
#        :: max Magintude: 5460.000000
#        :: rms:           1023.809119
#   REAL :: min Magintude: -5452.000000
#        :: max Magintude: 5308.000000
#        :: rms:           1024.190905
#   CPLX :: min Magintude: 0.000000
#        :: max Magintude: 5905.876565
#        :: rms:           1448.154730

from fct_diy import *
from fct_readRawTcData import *
from fct_spectrum import *
import os.path
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('dark_background')


inpPath = '/home/markus/Arbeit/2024-11-21_testAufEvalBoard/tcOut241121agcAt50dB/'
outPath = '/home/markus/Arbeit/2024-11-21_testAufEvalBoard/out/'

minAgc        = 0
maxAgc        = 100
stpAgc        = 5
idxAgc        = minAgc
minGen        = -100
maxGen        = 0
stpGen        = 1
idxGen        = minGen
inpPrefixAdc  = "tcAdc"
inpPrefixLVal = "tcLVals"
infoFileAdc   = "infoAdc.dat"
infoFileLVal  = "infoLVal.dat"

with open(infoFileAdc, "w") as fid:
  fid.write("   AGC  P_Tx -----------IMAG-------- -----------REAL-------- -----------CPLX--------       CFO Rel. to\n")
  fid.write("  [dB] [dBm]    Min.    Max.     RMS    Min.    Max.     RMS    Min.    Max.     RMS      [Hz] ADC Max.\n")
  fid.write("  <Ref.Data> %7d %7d %7d %7d %7d %7d %7d %7d %7d %9d\n" % (-5372,5460,1023,5452,5308,1024,0,5905,1448,192))

with open(infoFileLVal, "w") as fid:
  fid.write(" AGC. | Gen. | Min. | Max. | Amount Zeros | maxZeroRow\n")


while idxAgc < maxAgc + stpAgc:
  idxGen = minGen

  while idxGen < maxGen + stpGen:
    inpFileAdc  = inpPath+inpPrefixAdc+"_agc"+str(idxAgc)+"dB_gen"+str(idxGen)+"dBm"
    inpFileLVal = inpPath+inpPrefixLVal+"_agc"+str(idxAgc)+"dB_gen"+str(idxGen)+"dBm"

    if os.path.isfile(inpFileAdc):
      inpData    = fct_readRawTcData(inpFileAdc)
      data       = np.array(inpData)
      maxVal     = 0
      imagMSByte = np.array(data[0::4])
      imagLSByte = np.array(data[1::4])
      imag       = imagMSByte * 256 + imagLSByte
      imag       = fct_complementOnTwo2int(imag)
      maxVal     = np.max(np.append(np.abs(imag), maxVal))
      realMSByte = np.array(data[2::4])
      realLSByte = np.array(data[3::4])
      real       = realMSByte * 256 + realLSByte
      real       = fct_complementOnTwo2int(real)
      maxVal     = np.max(np.append(np.abs(real), maxVal))
      cplx       = real + imag * 1j
      cfoData    = cplx ** 4
      spec       = fct_spectrum(cplx, 13500000, fftRes=256)
      freqAxis   = spec[0]
      specAxis   = spec[1]
      cfo        = np.arange(0,len(specAxis))
      cfo        = cfo * (specAxis == np.max(specAxis))
      cfo        = np.max(cfo)
      cfo        = freqAxis[cfo]

      with open(infoFileAdc, "a") as fid:
        fid.write(" %5d %5d" % (idxAgc, idxGen))
        fid.write(" %7d %7d %7d" % (int(np.min(imag)), int(np.max(imag)), int(np.sqrt(np.sum(imag**2) / len(imag)))))
        fid.write(" %7d %7d %7d" % (int(np.min(real)), int(np.max(real)), int(np.sqrt(np.sum(real**2) / len(real)))))
        fid.write(" %7d %7d %7d" % (int(np.min(np.abs(cplx))), int(np.max(np.abs(cplx))), int(np.sqrt(np.sum(np.abs(cplx)**2) / len(cplx)))))
        fid.write(" %9d" % cfo)
        fid.write(" %7d\n" % int(maxVal / 2**15 *100))

    if  os.path.isfile(inpFileLVal):
      inpData = fct_readRawTcData(inpFileLVal)
      tmp     = np.array(inpData)
      lVal    = np.zeros(len(tmp) // 4)
      idx     = 0

      while idx < 4:
        lVal = lVal + tmp[3-idx::4] * 256**idx
        idx  = idx + 1

      lVal       = (lVal - lVal % 2**9) / 2**9
      lVal       = fct_complementOnTwo2int(lVal)
      minLVal    = np.min(lVal)
      maxLVal    = np.max(lVal)
      cntZero    = 0
      rowZero    = 0
      maxRowZero = 0
      idx        = 1

      while idx < len(lVal):

        if lVal[idx] == 0 and lVal[idx-1] == 0:
          cntZero    = cntZero + 1
          rowZero    = rowZero + 1
          maxRowZero = max(rowZero, maxRowZero)
        else:
          rowZero    = 0

        idx = idx + 2

      with open(infoFileLVal, "a") as fid:
        fid.write(" %4d | %4d |" % (idxAgc, idxGen))
        fid.write(" %4d | %4d |        %5d |      %5d\n" % (minLVal, maxLVal, cntZero, maxRowZero))

    idxGen = idxGen + stpGen

  idxAgc = idxAgc + stpAgc

      #print("Data ADC :: AGC: %ddB :: P_Tx: %ddBm" % (idxAgc, idxGen))
      #print("  >> IMAG :: min Magintude: %d" % int(np.min(imag)))
      #print("  >>      :: max Magintude: %d" % int(np.max(imag)))
      #print("  >>      :: rms:           %d" % int(np.sqrt(np.sum(imag**2) / len(imag))))
      #print("  >> REAL :: min Magintude: %d" % int(np.min(real)))
      #print("  >>      :: max Magintude: %d" % int(np.max(real)))
      #print("  >>      :: rms:           %d" % int(np.sqrt(np.sum(real**2) / len(real))))
      #print("  >> CPLX :: min Magintude: %d" % int(np.min(np.absolute(cplx))))
      #print("  >>      :: max Magintude: %d" % int(np.max(np.absolute(cplx))))
      #print("  >>      :: rms:           %d" % int(np.sqrt(np.sum(np.absolute(cplx)**2) / len(cplx))))
      #print("  >>      :: rms:           %d" % int(np.sqrt(np.sum(np.absolute(cplx)**2) / len(cplx))))
      #print("  >>      :: cfo:           %d" % int(cfo))
