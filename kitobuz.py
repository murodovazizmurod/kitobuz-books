import requests
import json
import os
import re

url = "https://raw.githubusercontent.com/murodovazizmurod/kitobuz-books/main/data.json"


books_folder = 'books'

# Check if the books folder exists, if not, create it
if not os.path.exists(books_folder):
    os.makedirs(books_folder)
    print(f"Folder '{books_folder}' created.")
else:
    print(f"Folder '{books_folder}' already exists.")

# Check if the data.json file exists
if not os.path.exists('data.json'):
    print(f"'{'data.json'}' does not exist. Downloading...")
    # Send a GET request to the URL
    response = requests.get(url)
    response.raise_for_status()  # Check for request errors
    
    # Save the downloaded content to data.json
    with open('data.json', 'wb') as file:
        file.write(response.content)
    print(f"File downloaded and saved as '{'data.json'}'.")
else:
    print(f"'{'data.json'}' already exists.")


def sanitize_filename(filename):
    """
    Sanitize the given filename by removing or replacing characters that are not allowed in file paths.

    Args:
    filename (str): The filename to sanitize.

    Returns:
    str: The sanitized filename.
    """
    # Replace any character that is not alphanumeric, a hyphen, an underscore, or a space with an underscore
    sanitized = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Remove any leading or trailing whitespace
    sanitized = sanitized.strip()
    # Ensure the filename is not empty after sanitization
    if not sanitized:
        raise ValueError("The sanitized filename is empty. Please provide a valid filename.")
    return sanitized


def download_pdf(url, save_name):
    """
    Downloads a PDF file from the given URL and saves it to the specified folder with the given name.

    Args:
    url (str): URL of the PDF file to download.
    save_folder (str): Folder to save the downloaded PDF file.
    save_name (str): Name to save the PDF file as (including .pdf extension).

    Returns:
    str: Path to the saved PDF file.
    """
    # Ensure the save folder exists
    if os.path.exists('books/'+save_name):
        print(f"File '{'books/'+save_name}' already exists. Skipping download.")
        return None
    # Define the full path to save the file

    # Send a GET request to the URL
    response = requests.get(url)
    response.raise_for_status()  # Check for request errors

    # Save the PDF file
    with open('books/'+save_name, 'wb') as file:
        file.write(response.content)

# # Define the URL
url = "https://api.kitob.itsm.uz/api/v1/uz/books/"

# # Define the headers
headers = {
    "x-api-key": "18f057d42feadf59b4943b7fb4c064fcd626778f",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

save_directory = 'books'
# # Send the GET request
# response = requests.get(url, headers=headers)
# response.raise_for_status()



with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for a in data:
    response = requests.get(url+a['id'], headers=headers)
    book = response.json()
    try:
        print(a['id'], book['name_uz'], book['files'][0]['sizeText'])
        if "Qozoq tili" in book['name_uz'] or "Tojik tili" in book['name_uz'] or "Qirg'iz tili" in book['name_uz'] or "Turkman tili" in book['name_uz'] or book['lang'] != 'uz' or "Qoraqalpoq tili" in book['name_uz']:
            print(f'Skipped! {book["name_uz"]}')
            continue
        
        download_pdf(book['files'][0]['url'], sanitize_filename(book['name_uz'])+'.pdf')
    except Exception as e:
        print(f"Error occured and it says: {e}")
# print(sanitize_filename(requests.get('https://api.kitob.itsm.uz/api/v1/uz/books/3965', headers=headers).json()['name_uz']))
