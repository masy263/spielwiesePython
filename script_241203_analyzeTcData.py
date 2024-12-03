#!/bin/python3

# script_241203_analyzeTcData

import matplotlib as plt
import numpy as np
import os.path

from fct_tcDataHandle import *


inpPath = '/home/markus/Arbeit/2024-11-21_testAufEvalBoard/tcRawData/'


fileIdxStart = 0
fileIdxEnd   = 15
fileIdxIncr  = 1
fileIdx      = fileIdxStart

while fileIdx < fileIdxEnd + 1:
  tcAdcFile  = inpPath+"tc"+str("%03d" % fileIdx)+"adc"
  tcMetaFile = inpPath+"tc"+str("%03d" % fileIdx)+"meta"

  if os.path.isfile(tcAdcFile):
    print("[script_241203_analyzeTcData] found: %s" % tcAdcFile)
    adcData = fct_readRawTcData(tcAdcFile)

  if os.path.isfile(tcMetaFile):
    print("[script_241203_analyzeTcData] found: %s" % tcMetaFile)
    metaData = fct_readRawTcData(tcMetaFile)
    metaData = fct_tc2uint(metaData, 2, 4)
    fct_tcMetaAnalyze(metaData, tcMetaFile)

  fileIdx = fileIdx + fileIdxIncr

