from bincat.token_manager import TokenManager
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

def main():
    print(Fore.CYAN + Style.BRIGHT + "Welcome to BinCat - Token Management\n")

    # Create an instance of TokenManager
    token_manager = TokenManager()

    while True:
        print(Fore.YELLOW + "\nWhat action would you like to perform?")
        print(Fore.GREEN + "1. Generate a token")
        print(Fore.GREEN + "2. Revoke a token")
        print(Fore.GREEN + "3. Validate a token")
        print(Fore.RED + "4. Exit")

        choice = input(Fore.WHITE + "Select an option (1-4): ")

        if choice == "1":
            # Generate a new token
            token = token_manager.generate_token()
            print(Fore.GREEN + f"Generated token: {token}")

        elif choice == "2":
            # Revoke a token
            token = input(Fore.WHITE + "Enter the token to revoke: ")
            if token_manager.revoke_token(token):
                print(Fore.RED + f"Token {token} successfully revoked.")
            else:
                print(Fore.YELLOW + f"Could not revoke token {token}.")

        elif choice == "3":
            # Validate a token
            token = input(Fore.WHITE + "Enter the token to validate: ")
            is_valid = token_manager.is_token_valid(token)
            if is_valid:
                print(Fore.GREEN + f"Token {token} is valid.")
            else:
                print(Fore.YELLOW + f"Token {token} is either invalid or expired.")

        elif choice == "4":
            print(Fore.CYAN + Style.BRIGHT + "Exiting the program...")
            break

        else:
            print(Fore.RED + "Invalid option. Please try again.")

if __name__ == "__main__":
    main()
