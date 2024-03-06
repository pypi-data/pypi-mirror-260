import os

def store_api_key(api_key):
    home_dir = os.path.expanduser('~')
    api_key_file = os.path.join(home_dir, '.sigiq_api_key')
    with open(api_key_file, 'w') as file:
        file.write(api_key)

def login_main():
    try:
        api_key = input("Enter your API key: ")
        store_api_key(api_key)
        
        print("API key stored successfully.")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return

