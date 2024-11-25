#!/bin/python3

# tb_241125_cutTcData

from fct_readRawTcData import *
import os.path
import numpy as np

inpPath = '/home/markus/Arbeit/2024-11-21_testAufEvalBoard/tcOut241121agcAt50dB/'
outPath = '/home/markus/Arbeit/2024-11-21_testAufEvalBoard/out/'

text = fct_readRawTcData("tc.test")

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
    inpFile = inpPath+inpPrefixAdc+"_agc"+str(idxAgc)+"dB_gen"+str(idxGen)+"dBm"

    if os.path.isfile(inpFile):
      #print("[tb_241125_cutTcData] found file: %s" % inpFile)
      inpData = fct_readRawTcData(inpFile)
      data = np.array(inpData)
      rms  = np.sqrt(np.sum(data**2) / len(data))
      print(rms)

    idxGen = idxGen + stpGen

  idxAgc = idxAgc + stpAgc

#print(text)