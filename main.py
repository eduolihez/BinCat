from colorama import Fore, Style, init
from bincat.token_manager import TokenManager

# Initialize colorama
init(autoreset=True)

def main():
    token_manager = TokenManager()

    while True:
        print(f"{Fore.CYAN}=== BinCat Token Manager ===")
        print(f"{Fore.YELLOW}1. Generate Token")
        print(f"{Fore.YELLOW}2. Revoke Token")
        print(f"{Fore.YELLOW}3. Validate Token")
        print(f"{Fore.YELLOW}4. Exit")
        choice = input(f"{Fore.CYAN}Choose an option: ")

        if choice == "1":
            print(f"{Fore.GREEN}Generating a new token...")
            token = token_manager.generate_token()
            print(f"{Fore.GREEN}Token generated: {token}")

        elif choice == "2":
            token = input(f"{Fore.CYAN}Enter the token to revoke: ")
            if token_manager.revoke_token(token):
                print(f"{Fore.GREEN}Token successfully revoked.")
            else:
                print(f"{Fore.RED}Failed to revoke token. Ensure it exists and has not been revoked.")

        elif choice == "3":
            token = input(f"{Fore.CYAN}Enter the token to validate: ")
            if token_manager.is_token_valid(token):
                print(f"{Fore.GREEN}Token is valid.")
            else:
                print(f"{Fore.RED}Token is invalid or expired.")

        elif choice == "4":
            print(f"{Fore.GREEN}Exiting the program. Goodbye!")
            break

        else:
            print(f"{Fore.RED}Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
