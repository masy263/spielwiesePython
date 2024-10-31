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

