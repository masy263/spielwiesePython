#!/bin/python3

import sys

nArgs = len(sys.argv)

print("amount of input args: %d" % nArgs)

idxArgs = 1;

while idxArgs < nArgs:

  inpText = list(sys.argv[idxArgs])
  outText = inpText

  while outText[-1] == '_' or outText[-1] == ' ':
    outText = outText[:-1]
    # print("%s" % ''.join(outText))

  while outText[0] == '_' or outText[0] == ' ':
    outText = outText[1:]
    # print("%s" % ''.join(outText))

  # replace lower cases by upper cases

  it = 0
  jt = 0

  while jt < len(outText):
    tmpCh = outText[jt]

    if tmpCh == '_' or tmpCh == ' ':
      # print(" >> kill underscore or space << ")
      jt = jt + 1
      tmpCh = ord(outText[jt])

      if tmpCh > 96 and tmpCh < 123:
        tmpCh = chr(tmpCh - 32)
      elif tmpCh == 228: # ä
        tmpCh = chr(tmpCh - 32)
      elif tmpCh == 246: # ö
        tmpCh = chr(tmpCh - 32)
      elif tmpCh == 252: # ü
        tmpCh = chr(tmpCh - 32)
      else:
        tmpCh = chr(tmpCh)

    outText[it] = tmpCh

    # print("char %02d :: %s" % (it, ''.join(outText)))
    it = it + 1
    jt = jt + 1

  outText = outText[:it]

  print("convert \"%s\" to \"%s\"" % (sys.argv[idxArgs], ''.join(outText)))

  idxArgs = idxArgs + 1