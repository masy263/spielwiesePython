import numpy as np

def fct_determineBitWidth(a):
  bitWidth = 0;

  while a > 0:
    bitWidth = bitWidth + 1;
    a = (a - a % 2) / 2

  return bitWidth;

def fct_complementOnTwo2int(inp):
  nInp     = len(inp)
  ret      = inp * 0
  bitWidth = fct_determineBitWidth(max(inp))
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

      if tNow == np.abs(TSym / 4 / rollOff):
        tmp = tmp + np.sin(np.pi / 2 / rollOff)
        tmp = tmp / (np.pi / 2 / rollOff)
        tmp = tmp * np.pi / rollOff
      else:
        tmp = tmp + np.cos(tNow * np.pi * rollOff / TSym)
        tmp = tmp / (1 - (2 * rollOff * tNow / TSym)**2)
        tmp = tmp * np.sin(np.pi * tNow / TSym)
        tmp = tmp / (np.pi * tNow / TSym)

      rc[idxRc] = tmp

    idxRc = idxRc + 1

  return rc

def fct_uint2bin(x, bitWidth=0):

  if np.ndim(x) == 0:
    lenX = 1
    x = np.array([x])
  else:
    lenX = len(x)

  if bitWidth == 0:
    bitWidth =  fct_determineBitWidth(np.max(x))

  ret = np.zeros(lenX * bitWidth, dtype=int)
  ret = ret.reshape(lenX, bitWidth)
  divVec = np.ones(lenX) * 2
  bitIdx = 0
  while np.max(x) > 0:
    bitIdx = bitIdx + 1
    ret[:,bitWidth - bitIdx] = x % divVec
    x = x // divVec
  return ret

def fct_int2complementOnTwo(x, bitWidth=0):
  minVal = np.min(x)
  maxVal = np.max(x)

  if (maxVal + 1) > (2**bitWidth - 1):
    bitWidth = fct_determineBitWidth(maxVal) + 1

  if -minVal> (2**bitWidth - 1):
    bitWidth = fct_determineBitWidth(-minVal) + 1

  ret = x * (x >= 0) + (x < 0) * (2**bitWidth + x);

  return ret

