import numpy as np

inpFileImag = '/home/markus/Arbeit/2024-06-21_TestsignalPrmkUL/Nos5/samples_input_imag.dat'
inpFileReal = '/home/markus/Arbeit/2024-06-21_TestsignalPrmkUL/Nos5/samples_input_real.dat'

with open(inpFileImag) as f:
  inpText = f.readlines()
  inpText = ''.join(inpText)
  inpText = inpText.split('\n')
  inpText = inpText[0:len(inpText) - 1]
  inpData = [int(cnt) for cnt in inpText]

imag = np.array(inpData)

with open(inpFileReal) as f:
  inpText = f.readlines()
  inpText = ''.join(inpText)
  inpText = inpText.split('\n')
  inpText = inpText[0:len(inpText) - 1]
  inpData = [int(cnt) for cnt in inpText]

real = np.array(inpData)
cplx = real + imag * 1j

print("IMAG :: min Magintude: %f" % np.min(imag))
print("     :: max Magintude: %f" % np.max(imag))
print("     :: rms:           %f" % np.sqrt(np.sum(imag**2) / len(imag)))
print("REAL :: min Magintude: %f" % np.min(real))
print("     :: max Magintude: %f" % np.max(real))
print("     :: rms:           %f" % np.sqrt(np.sum(real**2) / len(real)))
print("CPLX :: min Magintude: %f" % np.min(np.absolute(cplx)))
print("     :: max Magintude: %f" % np.max(np.absolute(cplx)))
print("     :: rms:           %f" % np.sqrt(np.sum(np.absolute(cplx)**2) / len(cplx)))