from bincat.token_manager import TokenManager
from colorama import Fore, Style
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

def main():
    print(Fore.CYAN + "Welcome to BinCat Token Manager!" + Style.RESET_ALL)
    
    # Verificar que la clave de cifrado esté disponible
    encryption_key = os.getenv("ENCRYPTION_KEY")
    if not encryption_key:
        print(Fore.RED + "Error: ENCRYPTION_KEY is missing. Please add it to your .env file." + Style.RESET_ALL)
        return
    
    # Inicializar TokenManager
    token_manager = TokenManager()

    while True:
        print(Fore.GREEN + "\nMenu:" + Style.RESET_ALL)
        print("1. Generate Token")
        print("2. Revoke Token")
        print("3. Check Token Validity")
        print("4. Exit")

        choice = input(Fore.YELLOW + "Enter your choice: " + Style.RESET_ALL)
        if choice == "1":
            token = token_manager.generate_token()
            print(Fore.GREEN + f"Token generated: {token}" + Style.RESET_ALL)
        elif choice == "2":
            token = input(Fore.YELLOW + "Enter the token to revoke: " + Style.RESET_ALL)
            if token_manager.revoke_token(token):
                print(Fore.GREEN + "Token revoked successfully." + Style.RESET_ALL)
            else:
                print(Fore.RED + "Failed to revoke token. Token may not exist." + Style.RESET_ALL)
        elif choice == "3":
            token = input(Fore.YELLOW + "Enter the token to check: " + Style.RESET_ALL)
            is_valid = token_manager.is_token_valid(token)
            if is_valid:
                print(Fore.GREEN + "Token is valid." + Style.RESET_ALL)
            else:
                print(Fore.RED + "Token is invalid or expired." + Style.RESET_ALL)
        elif choice == "4":
            print(Fore.CYAN + "Exiting BinCat Token Manager. Goodbye!" + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
