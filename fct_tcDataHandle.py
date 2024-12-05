import numpy as np
from fct_diy import *

def fct_readRawTcData(inpFile):
  sofDelimiter = '2E 16 D2 04 0C '
  asciiCmp     = [ord(c) for c in sofDelimiter]
  ret          = 0

  with open(inpFile) as f:
    lines     = f.readlines()

  textData  = ''.join(lines)
  textData  = textData.replace('a', 'A')
  textData  = textData.replace('b', 'B')
  textData  = textData.replace('c', 'C')
  textData  = textData.replace('d', 'D')
  textData  = textData.replace('e', 'E')
  textData  = textData.replace('f', 'F')
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
      idxChar = lenData

    idxChar = idxChar + 1

  if cutPos > 0:
    textData            = ''.join([chr(c) for c in asciiData[cutPos:]])
    payloadLengthLSByte = int(textData[0:2], 16)
    payloadLengthMSByte = int(textData[3:5], 16)
    payloadLength       = (payloadLengthMSByte * 256 + payloadLengthLSByte) * 3

    if len(textData) > payloadLength + 5:
      textData = textData[6:payloadLength + 5]
    else:
      textData = textData[6:]

    with open(inpFile+"_payload.hex", "w") as text_file:
      text_file.write("%s\n" % textData.replace(' ', '\n'))

  else:
    print("[fct_readRawTcData] could not found sof in inp file...")
    print("[fct_readRawTcData] assuming whole data is payload data...")
    textData            = ''.join([chr(c) for c in asciiData])

  while textData[0] == '' or textData[0] == ' ':
    textData = textData[1:]

  while textData[len(textData)-1] == '' or textData[len(textData)-1] == ' ':
    textData = textData[0:len(textData)-2]

  textData = textData.split(' ')
  decData = [int(cnt, 16) for cnt in textData]
  strData = [str(cnt)+"\n" for cnt in decData]

  with open(inpFile+"_payload.csv", "w") as text_file:
    text_file.write("%s" % ''.join(strData))

  ret = decData

  return ret

def fct_tc2uint(inpData, nColumns, bytesPerColumn):
  splitter = nColumns * bytesPerColumn
  data     = np.zeros((nColumns, len(inpData) // splitter))
  idxClmn  = 0

  while idxClmn < nColumns:

    idxByte  = 0

    while idxByte < bytesPerColumn:
      posByte = idxClmn * bytesPerColumn + idxByte
      data[idxClmn] = data[idxClmn] + np.array(inpData[posByte::splitter]) * 256**(3-idxByte)
      idxByte       = idxByte + 1

    idxClmn = idxClmn + 1

  return data

def fct_tcMetaAnalyze(inpData, fileName):
  pdDetec       = "new pd detection event..."
  pdStateChange = "pd changed state..."
  sig0cf0       = "cfo output at first sig module..."
  sig1cf0       = "cfo output at second sig module..."
  sig2cf0       = "cfo output at third sig module..."
  sig0sigBits   = "sig bits output at first sig module..."
  sig1sigBits   = "sig bits output at second sig module..."
  sig2sigBits   = "sig bits output at third sig module..."
  demodLVals    = "new lVal output from demod..."
  logFile       = fileName+"_info.log"
  lValDecFile   = fileName+"_lVal.csv"
  lValHexFile   = fileName+"_lVal.hex"
  outDat        = np.zeros(32, dtype=np.int64)
  outTxt        = ['', '', '']
  writeFlag     = 0
  datCntLast    = 0
  typeIdLast    = 0
  lValFlag      = 0

  with open(lValDecFile, "w") as fid:
    fid.write('')

  with open(lValHexFile, "w") as fid:
    fid.write('')

  with open(logFile, "w") as fid:
    fid.write('%s\n' % fileName)

  idx = 0
  while idx < len(inpData[0]):
    data0 = int(inpData[0][idx])
    data1 = int(inpData[1][idx])

    data0  = int(data0 // 2**13)
    datCnt = int(data0 % 2**3)
    data0  = int(data0 // 2**3)
    typeId = int(data0 % 2**16)

    if typeId == np.sum([ord(ch) for ch in pdDetec]):

      if datCntLast != (datCnt + 1):

        with open(logFile, "a") as fid:
          fid.write('\n%s\n' % pdDetec)

      datCntLast = datCnt

      if datCnt == 0:
        data1     = int(data1 // 2**10)
        outTxt[0] = "pdDetecFlag"
        outDat[0] = int(data1 % 2**1) 
        data1     = int(data1 // 2**1)
        outTxt[1] = "pdState"
        outDat[1] = int(data1 % 2**3)
        data1     = int(data1 // 2**3)
        outTxt[2] = "pdCfo"
        outDat[2] = fct_complementOnTwo2int((data1 % 2**18), 18)
        writeFlag = 3

      if datCnt == 1:
        outTxt[0] = "pdSymIdx1"
        outDat[0] = int(data1) // 2**14 # pdSymIdx1
        writeFlag = 1

      if datCnt == 2:
        outTxt[0] = "pdSymIdx2"
        outDat[0] = int(data1) // 2**14 # pdSymIdx2
        writeFlag = 1

      if datCnt == 3:
        outTxt[0] = "pdSymIdxPtr"
        outDat[0] = int(data1) // 2**14 # pdSymIdxPtr
        writeFlag = 1

      if datCnt == 4:
        outTxt[0] = "pdSymIdxTd2"
        outDat[0] = int(data1) // 2**14 # pdSymIdxTd2
        writeFlag = 1

      if datCnt == 5:
        outTxt[0] = "pdSymM1save"
        outDat[0] = int(data1) // 2**14 # pdSymM1save
        writeFlag = 1

      if datCnt == 6:
        outTxt[0] = "pdDistanceM2M1"
        outDat[0] = int(data1) // 2**14 # pdDistanceM2M1
        writeFlag = 1

      if datCnt == 7:
        outTxt[0] = "runCnt"
        outDat[0] = int(data1) # runCnt
        writeFlag = 1

    if typeId == np.sum([ord(ch) for ch in pdStateChange]):

      if datCntLast != (datCnt + 1):

        with open(logFile, "a") as fid:
          fid.write('\n%s\n' % pdStateChange)

      datCntLast = datCnt

      if datCnt == 0:
        data1     = int(data1 // 2**10)
        outTxt[0] = "pdDetecFlag"
        outDat[0] = int(data1 % 2**1) 
        data1     = int(data1 // 2**10)
        outTxt[1] = "pdState"
        outDat[1] = int(data1 % 2**3)
        data1     = int(data1 // 2**3)
        outTxt[2] = "pdCfo"
        outDat[2] = fct_complementOnTwo2int((data1 % 2**18), 18)
        writeFlag = 3

      if datCnt == 1:
        outTxt[0] = "pdSymIdx1"
        outDat[0] = int(data1) // 2**14 # pdSymIdx1
        writeFlag = 1

      if datCnt == 2:
        outTxt[0] = "pdSymIdx2"
        outDat[0] = int(data1) // 2**14 # pdSymIdx2
        writeFlag = 1

      if datCnt == 3:
        outTxt[0] = "pdSymIdxPtr"
        outDat[0] = int(data1) // 2**14 # pdSymIdxPtr
        writeFlag = 1

      if datCnt == 4:
        outTxt[0] = "pdSymIdxTd2"
        outDat[0] = int(data1) // 2**14 # pdSymIdxTd2
        writeFlag = 1

      if datCnt == 5:
        outTxt[0] = "pdSymM1save"
        outDat[0] = int(data1) // 2**14 # pdSymM1save
        writeFlag = 1

      if datCnt == 6:
        outTxt[0] = "pdDistanceM2M1"
        outDat[0] = int(data1) // 2**14 # pdDistanceM2M1
        writeFlag = 1

      if datCnt == 7:
        outTxt[0] = "runCnt"
        outDat[0] = int(data1) # runCnt
        writeFlag = 1

    if typeId == np.sum([ord(ch) for ch in sig0cf0]):

      if datCntLast != (datCnt + 1):

        with open(logFile, "a") as fid:
          fid.write('\n%s\n' % sig0cf0)

      datCntLast = datCnt

      if datCnt == 0:
        outTxt[0] = "sig0cfo"
        outDat[0] = fct_complementOnTwo2int(int(data1) // 2**22, 10) # pdDistanceM2M1
        writeFlag = 1

      if datCnt == 1:
        outTxt[0] = "runCnt"
        outDat[0] = int(data1) # runCnt
        writeFlag = 1

    if typeId == np.sum([ord(ch) for ch in sig1cf0]):

      if datCntLast != (datCnt + 1):

        with open(logFile, "a") as fid:
          fid.write('\n%s\n' % sig1cf0)

      datCntLast = datCnt

      if datCnt == 0:
        outTxt[0] = "sig0cfo"
        outDat[0] = fct_complementOnTwo2int(int(data1) // 2**22, 10) # pdDistanceM2M1
        writeFlag = 1

      if datCnt == 1:
        outTxt[0] = "runCnt"
        outDat[0] = int(data1) # runCnt
        writeFlag = 1

    if typeId == np.sum([ord(ch) for ch in sig2cf0]):

      if datCntLast != (datCnt + 1):

        with open(logFile, "a") as fid:
          fid.write('\n%s\n' % sig2cf0)

      datCntLast = datCnt

      if datCnt == 0:
        outTxt[0] = "sig0cfo"
        outDat[0] = fct_complementOnTwo2int(int(data1) // 2**22, 10) # pdDistanceM2M1
        writeFlag = 1

      if datCnt == 1:
        outTxt[0] = "runCnt"
        outDat[0] = int(data1) # runCnt
        writeFlag = 1

    if typeId == np.sum([ord(ch) for ch in sig0sigBits]):

      if datCntLast != (datCnt + 1):

        with open(logFile, "a") as fid:
          fid.write('\n%s\n' % sig0sigBits)

      datCntLast = datCnt

      if datCnt == 0:
        outTxt[1] = "sig0sigBits          :: "
        outTxt[0] = "sig0sigBits reversed :: "
        outDat[1] = int(data1 // 2**22)
        outDat[0] = fct_uint2binReverse(outDat[1], 10)
        sigTxt    = fct_uint2binStr(outDat[1],10)
        sigTxtRev = fct_uint2binStr(outDat[0],10)
        sigHex    = str("%3X" % outDat[1])
        sigHexRev = str("%3X" % outDat[0])
        outTxt[1] = outTxt[1] + sigHex + " :: " + sigTxt + " :"
        outTxt[0] = outTxt[0] + sigHexRev + " :: " + sigTxtRev + " :"
        writeFlag = 2

      if datCnt == 1:
        outTxt[0] = "runCnt"
        outDat[0] = int(data1) # runCnt
        writeFlag = 1

    if typeId == np.sum([ord(ch) for ch in sig1sigBits]):

      if datCntLast != (datCnt + 1):

        with open(logFile, "a") as fid:
          fid.write('\n%s\n' % sig1sigBits)

      datCntLast = datCnt

      if datCnt == 0:
        outTxt[1] = "sig0sigBits          :: "
        outTxt[0] = "sig0sigBits reversed :: "
        outDat[1] = int(data1 // 2**22)
        outDat[0] = fct_uint2binReverse(outDat[1], 10)
        sigTxt    = fct_uint2binStr(outDat[1],10)
        sigTxtRev = fct_uint2binStr(outDat[0],10)
        sigHex    = str("%3X" % outDat[1])
        sigHexRev = str("%3X" % outDat[0])
        outTxt[1] = outTxt[1] + sigHex + " :: " + sigTxt + " :"
        outTxt[0] = outTxt[0] + sigHexRev + " :: " + sigTxtRev + " :"
        writeFlag = 2

      if datCnt == 1:
        outTxt[0] = "runCnt"
        outDat[0] = int(data1) # runCnt
        writeFlag = 1

    if typeId == np.sum([ord(ch) for ch in sig2sigBits]):

      if datCntLast != (datCnt + 1):

        with open(logFile, "a") as fid:
          fid.write('\n%s\n' % sig2sigBits)

      datCntLast = datCnt

      if datCnt == 0:
        outTxt[1] = "sig0sigBits          :: "
        outTxt[0] = "sig0sigBits reversed :: "
        outDat[1] = int(data1 // 2**22)
        outDat[0] = fct_uint2binReverse(outDat[1], 10)
        sigTxt    = fct_uint2binStr(outDat[1],10)
        sigTxtRev = fct_uint2binStr(outDat[0],10)
        sigHex    = str("%3X" % outDat[1])
        sigHexRev = str("%3X" % outDat[0])
        outTxt[1] = outTxt[1] + sigHex + " :: " + sigTxt + " :"
        outTxt[0] = outTxt[0] + sigHexRev + " :: " + sigTxtRev + " :"
        writeFlag = 2

      if datCnt == 1:
        outTxt[0] = "runCnt"
        outDat[0] = int(data1) # runCnt
        writeFlag = 1

    #if typeId == np.sum([ord(ch) for ch in demodLVals+"nö"]): # ACHTUNG: TOTGELEGT!
    if typeId == np.sum([ord(ch) for ch in demodLVals]):
      
      if(typeIdLast != typeId):

        with open(logFile, "a") as fid:
          fid.write('\n%s\n' % demodLVals)

      if datCnt == 0:
        outTxt[1] = "lVal0"
        outTxt[0] = "lVal1"
        outDat[3] = (data1 // 2**14) % 2**9 # lVal0
        outDat[2] = (data1 // 2**23) % 2**9 # lVal1
        outDat[1] = fct_complementOnTwo2int(outDat[3], 9) # lVal0
        outDat[0] = fct_complementOnTwo2int(outDat[2], 9) # lVal1
        lValFlag  = 1
        writeFlag = 2

      if datCnt == 1:
        outTxt[0] = "runCnt"
        outDat[0] = int(data1) # runCnt
        writeFlag = 1


    typeIdLast = typeId

    while writeFlag > 0:
      writeFlag = writeFlag - 1

      with open(logFile, "a") as fid:
        fid.write('  >>  %s: %d\n' % (outTxt[writeFlag], outDat[writeFlag]))

    if (lValFlag > 0):
      lValFlag = 0

      with open(lValDecFile, "a") as fid:
        fid.write('%d, %d\n' % (outDat[1], outDat[0]))

      with open(lValHexFile, "a") as fid:
        fid.write('%03X, %03X\n' % (outDat[3], outDat[2]))

    #print("type id: %5d :: data counter: %d" % (typeId, datCnt))

    idx = idx + 1

  
