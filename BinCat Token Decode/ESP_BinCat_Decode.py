from base64 import b64decode
from colorama import Fore, Style, init
init(autoreset=True)

token1 = input(Fore.GREEN + 'Introduzca el Token: ' + Style.RESET_ALL)
token = token1.partition(".")
token2 = token[2].partition(".")

id = token[0]
fecha = token2[2]
numero = token2[0]

print(Fore.YELLOW + token[0] + " | " + token2[0] + " | " + token2[2])
print(Fore.GREEN + 'La ID del token es: ')
print(b64decode(id))
print(Fore.GREEN + 'La fecha de creación del Token es: ')
print(b64decode(fecha))
print(Fore.GREEN + 'El número de identificación del Token es: ' +
      Style.RESET_ALL + Style.BRIGHT + numero)
