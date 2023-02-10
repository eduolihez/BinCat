import random
from colorama import Fore, Style, init
import base64
import time
import qrcode

# Declaramos todas las veriables
fecha = time.strftime("%d-%m-%y %X")
fecha2 = time.strftime("%x")
chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789"
nums = "9183726450"
init(autoreset=True)

username = input(
    Fore.GREEN + '[+] ' + Style.RESET_ALL + 'Introduce un nombre de usuario: ')

for c in range(1):

    part1 = ""
    part2 = ""
    part3 = fecha2

    for x in range(10):
        # Selecionamos 10 números aleatorios como si fuera la ID
        part1 += random.choice(nums)
    for x in range(7):
        part2 += random.choice(chars)  # 7 números aleatorios

    part1 = str(part1)
    part2 = str(part2)
    part3 = str(part3)

############################## CODIFICACIÓN ##############################
    # Codificamos la ID en Base64
    encodedBytes = base64.b64encode(part1.encode("utf-8"))
    part1encode = str(encodedBytes, "utf-8")

    # Codificamos la Fecha en Base64
    encodedBytes = base64.b64encode(part3.encode("utf-8"))
    part3encode = str(encodedBytes, "utf-8")

##########################################################################

    # Juntamos todas las partes
    token = part1encode + "." + part2 + "." + part3encode

    # Mostramos el Token creado
    print(Fore.BLUE + '[?] ' + Style.RESET_ALL + 'El Token para ' +
          Style.BRIGHT + username + ' es: ' + Fore.YELLOW + token)
    print(Fore.BLUE + '[?] ' + Style.RESET_ALL + 'La ID del usuario ' +
          Style.BRIGHT + username + ' es: ' + Fore.YELLOW + part1)
    print(Fore.BLUE + '[?] ' + Style.RESET_ALL +
          'La Fecha de creación del Token es el: ' + Fore.YELLOW + fecha)

# Preguntamos si quiere un QR con el Token

data = token
filename = 'BinCat_Token.png'
img = qrcode.make(data)
img.save(filename)
print(Fore.GREEN + '[+]' + 'Token guardado como QR')

# Estas dos lineas es para adaptar el programa a un ejecutable .exe
exit = input('Pulse enter para salir...')
exit = quit()
