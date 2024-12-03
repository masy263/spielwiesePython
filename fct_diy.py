import numpy as np

def fct_determineBitWidth(a):
  bitWidth = 0

  while a > 0:
    bitWidth = bitWidth + 1
    a = a // 2

  return bitWidth;

def fct_complementOnTwo2int(inp, bitWidth=0):
  ret      = inp * 0
  bitWidth = max(bitWidth, fct_determineBitWidth(np.max(inp)))
  bitIdx   = 0

  while bitIdx < bitWidth:
    tmp    = (inp % 2)
    inp    = (inp - tmp) // 2
    tmp    = tmp * 2**bitIdx
    bitIdx = bitIdx + 1

    if bitIdx == bitWidth:
      ret = ret - tmp
    else:
      ret = ret + tmp

  return ret

def fct_rrcGen(nOs, rollOff, nPeriods = 10, TSym = 1):
  TSum     = nPeriods * TSym
  dt       = TSym / nOs
  t        = np.arange(-TSum, TSum + dt, dt)
  lRrc     = len(t)
  rrc      = np.zeros(lRrc)
  idxRrc   = 0

  while idxRrc < lRrc:
    tNow = t[idxRrc]

    if tNow == 0:
      rrc[idxRrc] =  1 / np.sqrt(TSym) * (1 - rollOff + 4 * rollOff / np.pi)
    else:
      tmp = 0

      if tNow == np.abs(TSym / 4 / rollOff):
        tmp = tmp + (1 + 2 / np.pi) * np.sin(np.pi / 4 / rollOff)
        tmp = tmp + (1 - 2 / np.pi) * np.cos(np.pi / 4 / rollOff)
        tmp = tmp * rollOff / np.sqrt(2 * TSym)
      else:
        tmp = tmp + 4 * rollOff * tNow / TSym * np.cos(np.pi * tNow / TSym * (1 + rollOff))
        tmp = tmp + np.sin(np.pi * tNow / TSym * (1 - rollOff))
        tmp = tmp / (np.pi * tNow / TSym * (1 - (4 * rollOff * tNow / TSym) ** 2))
        tmp = tmp / np.sqrt(TSym)

      rrc[idxRrc] = tmp

    idxRrc = idxRrc + 1

  return rrc

def fct_rcGen(nOs, rollOff, nPeriods = 10, TSym = 1):
  TSum     = nPeriods * TSym
  dt       = TSym / nOs
  t        = np.arange(-TSum, TSum + dt, dt)
  lRc      = len(t)
  rc       = np.zeros(lRc)
  idxRc    = 0

  while idxRc < lRc:
    tNow = t[idxRc]

    if tNow == 0:
      rc[idxRc] =  1
    else:
      tmp = 0

      if tNow == np.abs(TSym / 2 / rollOff):
        tmp = tmp + np.sin(np.pi / 2 / rollOff)
        tmp = tmp / (np.pi / 2 / rollOff)
        tmp = tmp * np.pi / rollOff
      else:
        tmp = tmp + np.cos(tNow * np.pi * rollOff / TSym)
        print((1 - (2 * rollOff * tNow / TSym)**2))
        tmp = tmp / (1 - (2 * rollOff * tNow / TSym)**2)
        tmp = tmp * np.sin(np.pi * tNow / TSym)
        tmp = tmp / (np.pi * tNow / TSym)

      rc[idxRc] = tmp

    idxRc = idxRc + 1

  return rc

def fct_uint2binStr(inp, bitWidth=0):
  inp    = int(inp)
  bitIdx = 0
  ret    = ''

  while (inp > 0) or (bitIdx < bitWidth):

    if (inp % 2) > 0:
      ret = "1"+ret
    else:
      ret = "0"+ret

    bitIdx = bitIdx + 1
    inp    = inp // 2

  return ret

def fct_uint2binReverse(inp, bitWidth=0):
  binStr = fct_uint2binStr(inp, bitWidth)
  idx    = 0
  ret    = 0

  while idx < len(binStr):

    if(binStr[idx] == '1'):
      ret = ret + 2**idx

    idx = idx + 1

  return ret