from pathlib import Path

def get_user_input():
    api_key = input("Enter the API Key: ")
    search_engine_id = input("Enter the Search Engine Id: ")
    return api_key, search_engine_id


def update_or_create(API_KEY, SEARCH_ENGINE_ID):
    file_path = Path.home() / ".env"
    try:
        with open(file_path, 'w') as file:
            file.write(f'API_KEY="{API_KEY}"\nSEARCH_ENGINE_ID="{SEARCH_ENGINE_ID}"')
            print(".env file sucessfully created and updated..")
    except Exception as  e:
        print(f"Exception Occured: {e}")

def main():
    keys  = get_user_input()
    API_KEY = keys[0]
    SEARCH_ENGINE_ID = keys[1]
    update_or_create(API_KEY, SEARCH_ENGINE_ID)

if __name__ == '__main__':
    main()
