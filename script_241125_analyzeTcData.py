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

from fct_readRawTcData import *
import os.path
import numpy as np

inpPath = '/home/markus/Arbeit/2024-11-21_testAufEvalBoard/tcOut241121agcAt50dB/'
outPath = '/home/markus/Arbeit/2024-11-21_testAufEvalBoard/out/'

minAgc       = 0
maxAgc       = 100
stpAgc       = 5
idxAgc       = minAgc
minGen       = -100
maxGen       = 0
stpGen       = 2
idxGen       = minGen
inpPrefixAdc = "tcAdc"
#tcAdc_agc50dB_gen-31dBm

while idxAgc < maxAgc + stpAgc:
  idxGen = minGen

  while idxGen < maxGen + stpGen:
    inpFileAdc = inpPath+inpPrefixAdc+"_agc"+str(idxAgc)+"dB_gen"+str(idxGen)+"dBm"

    if os.path.isfile(inpFileAdc):
      #print("[tb_241125_cutTcData] found file: %s" % inpFileAdc)
      inpData  = fct_readRawTcData(inpFileAdc)
      data     = np.array(inpData)
      imag     = np.array(data[0::2])
      real     = np.array(data[1::2])
      cplx     = real + imag * 1j
      print("Data ADC :: AGC: %ddB :: P_Tx: %ddBm" % (idxAgc, idxGen))
      print("  >> IMAG :: min Magintude: %f" % np.min(imag))
      print("  >>      :: max Magintude: %f" % np.max(imag))
      print("  >>      :: rms:           %f" % np.sqrt(np.sum(imag**2) / len(imag)))
      print("  >> REAL :: min Magintude: %f" % np.min(real))
      print("  >>      :: max Magintude: %f" % np.max(real))
      print("  >>      :: rms:           %f" % np.sqrt(np.sum(real**2) / len(real)))
      print("  >> CPLX :: min Magintude: %f" % np.min(np.absolute(cplx)))
      print("  >>      :: max Magintude: %f" % np.max(np.absolute(cplx)))
      print("  >>      :: rms:           %f" % np.sqrt(np.sum(np.absolute(cplx)**2) / len(cplx)))

    idxGen = idxGen + stpGen

  idxAgc = idxAgc + stpAgc

#print(text)