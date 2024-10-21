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
