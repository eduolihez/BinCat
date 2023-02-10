from base64 import b64decode
from colorama import Fore, Style, init
init(autoreset=True)

token1 = input(Fore.GREEN + 'Enter the Token: ' + Style.RESET_ALL)
token = token1.partition(".")
token2 = token[2].partition(".")

id = token[0]
fecha = token2[2]
numero = token2[0]

print(Fore.YELLOW + token[0] + " | " + token2[0] + " | " + token2[2])
print(Fore.GREEN + 'The Token is: ')
print(b64decode(id))
print(Fore.GREEN + 'The creation date of the Token is: ')
print(b64decode(fecha))
print(Fore.GREEN + 'The Token identification number is: ' +
      Style.RESET_ALL + Style.BRIGHT + numero)
