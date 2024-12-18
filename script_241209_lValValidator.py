#!/bin/python3

from fct_diy import *
import numpy as np

inpPath = '/home/markus/Arbeit/2024-11-21_ibnHdl/data241205/tcRawData/'
inpFile = 'tc032meta_lVal.csv'

data = fct_readCsv(inpPath + inpFile)
BITS = np.zeros(len(data) * 2)
data = np.transpose(data)
BITS[0::2] = data[0]
BITS[1::2] = data[1]
BITS       = BITS[0:len(BITS) - len(BITS) % 8]
tmpBits    = np.zeros(len(BITS))
idxBits    = 0

while idxBits < 8:
  tmpBits[idxBits::8] = BITS[7-idxBits::8]
  idxBits = idxBits + 1

BITS = tmpBits
BITS = (BITS < 0) * 1

idxByte = 0

while idxByte < 8:
  BITS    = BITS[0:len(BITS) - len(BITS) % 8]
  BYTE    = np.zeros(len(BITS) // 8)
  idxBits = 0
  
  while idxBits < 8:
    BYTE    = BYTE + BITS[7-idxBits::8] * 2**idxBits
    idxBits = idxBits + 1
  
  print(np.sum(np.abs(np.diff(BYTE)) == 1))
  
  BITS    = BITS[1:]
  idxByte = idxByte + 1