import requests
from pathlib import Path
from random import randint


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


if __name__ == '__main__':
    Path("books").mkdir(parents=True, exist_ok=True)

    for book_number in range(10):
        url = f"https://tululu.org/txt.php?id={book_number+1}"
        response = requests.get(url)
        response.raise_for_status()
        try:
            check_for_redirect(response)
        except requests.HTTPError:
            continue
        filename = f'book_{book_number+1}.txt'
        with open('books/'+filename, 'w') as file:
            file.write(response.text)