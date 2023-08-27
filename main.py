# -*- coding: utf-8 -*-
import requests
from pathlib import Path
from bs4 import BeautifulSoup
import pathvalidate


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def get_book_title(book_number):
    url = f"https://tululu.org/b{book_number}/"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    book_title = soup.find('h1')

    if book_title:
        return book_title.text.split('::')[0].strip()
    else:
        return "Unknown Title"


def download_txt(url, book_number, folder='books/'):
    response = requests.get(url)
    response.raise_for_status()

    try:
        check_for_redirect(response)
    except requests.HTTPError:
        return 'redirect'

    book_title = get_book_title(book_number)

    Path(folder).mkdir(parents=True, exist_ok=True)
    safe_filename = pathvalidate.sanitize_filename(f'{book_number}. {book_title}')
    file_path = Path(folder) / (safe_filename + '.txt')

    with open(file_path, 'w') as file:
        file.write(response.text)

    return str(file_path)



if __name__ == '__main__':
    for book_number in range(10):
        url = f"https://tululu.org/txt.php?id={book_number+1}"
        filepath = download_txt(url, str(book_number + 1), 'books/')
        print(filepath)
