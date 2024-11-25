def fct_readRawTcData(inpFile):
  textCmp  = '2E 16 D2 04 0C '
  asciiCmp = [ord(c) for c in textCmp]
  ret      = 0

  with open(inpFile) as f:
    lines     = f.readlines()

  textData  = ''.join(lines)
  textData  = textData.replace('\n', ' ')
  textData  = textData.replace('  ', ' ')
  asciiData = [ord(c) for c in textData]
  lenData   = len(asciiData)
  lenCmp    = len(asciiCmp)
  idxChar   = lenCmp
  cutPos    = 0


  while idxChar < lenData:

    if asciiCmp == asciiData[idxChar - lenCmp:idxChar]:
      cutPos  = idxChar
      print(cutPos)
      idxChar = lenData

    idxChar = idxChar + 1

  if cutPos > 0:
    #print("found sof at char idx: %d" % cutPos)

    textData            = ''.join([chr(c) for c in asciiData[cutPos:]])
    payloadLengthLSByte = int(textData[0:2], 16)
    payloadLengthMSByte = int(textData[3:5], 16)
    payloadLength = (payloadLengthMSByte * 256 + payloadLengthLSByte) * 3

    if len(textData) > payloadLength + 5:
      textData = textData[6:payloadLength + 5]
    else:
      textData = textData[6:]

    with open(inpFile+"_cut.hex", "w") as text_file:
      text_file.write("%s\n" % textData.replace(' ', '\n'))

    textData = textData.split(' ')
    decData = [int(cnt, 16) for cnt in textData]
    strData = [str(cnt)+"\n" for cnt in decData]

    with open(inpFile+"_cut.dec", "w") as text_file:
      text_file.write("%s" % ''.join(strData))

    ret = decData
  else:
    print("[fct_readRawTcData] could not found sof in inp file")

  return ret