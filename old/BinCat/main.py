import random
from colorama import Fore, Style, init
import base64
import time
import qrcode

init(autoreset=True)

# We declare all the variables
fecha = time.strftime("%d-%m-%y %X")
fecha2 = time.strftime("%x")
chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789"
nums = "9183726450"

username = input(Fore.GREEN + '[+] ' + Style.RESET_ALL + 'Enter a username: ')

for c in range(1):
    part1 = ""
    part2 = ""
    part3 = fecha2

    for x in range(10):
        # We select 10 random numbers as if it were the ID
        part1 += random.choice(nums)
    for x in range(7):
        part2 += random.choice(chars)  # 7 random numbers

    part1 = str(part1)
    part2 = str(part2)
    part3 = str(part3)

    ################################ ENCODING ################################
    # We encode the ID in Base64
    encodedBytes = base64.b64encode(part1.encode("utf-8"))
    part1encode = str(encodedBytes, "utf-8")

    # We encode the Date in Base64
    encodedBytes = base64.b64encode(part3.encode("utf-8"))
    part3encode = str(encodedBytes, "utf-8")

    ##########################################################################

    # We put all the parts together
    token = part1encode + "." + part2 + "." + part3encode

    # We show the Token created
    print(Fore.BLUE + '[?] ' + Style.RESET_ALL + 'The Token for ' +
          Style.BRIGHT + username + ' is: ' + Fore.YELLOW + token)
    print(Fore.BLUE + '[?] ' + Style.RESET_ALL + 'The User ID for ' +
          Style.BRIGHT + username + ' is: ' + Fore.YELLOW + part1)
    print(Fore.BLUE + '[?] ' + Style.RESET_ALL +
          'The Token Creation Date is the: ' + Fore.YELLOW + fecha)

# Save the Token as QR
data = token
filename = 'BinCat_Token.png'
img = qrcode.make(data)
img.save(filename)
print(Fore.GREEN + '[+] ' + 'Token saved as QR')

# These two lines are to adapt the program to an executable .exe
input('Press enter to exit...')
quit()
