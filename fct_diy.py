def fct_determineBitWidth(a):
  bitWidth = 0;

  while a > 0:
    bitWidth = bitWidth + 1;
    a = (a - a % 2) / 2

  return bitWidth;

