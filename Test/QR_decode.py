import qrtools
qr = qrtools.qr()
path = input('Introduce the QR path: ')
qr.decode(path)
print(qr.data)