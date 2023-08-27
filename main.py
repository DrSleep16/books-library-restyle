import requests
from pathlib import Path
from random import randint


Path("books").mkdir(parents=True, exist_ok=True)

for book_number in range(10):
    url = f"https://tululu.org/txt.php?id={randint(10000,99999)}"
    response = requests.get(url)
    response.raise_for_status()
    filename = f'book_{book_number+1}.txt'
    with open('books/'+filename, 'w') as file:
        file.write(response.text)