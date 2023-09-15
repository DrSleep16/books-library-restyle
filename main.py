# -*- coding: utf-8 -*-
import os
import sys
import time
import json
from pathvalidate import sanitize_filename
import requests
import argparse

from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from check_for_redirect import check_for_redirect
from parse_tululu_category import get_urls_books


def parse_book_page(response):
    soup = BeautifulSoup(response.text, 'lxml')

    book_title = soup.select_one('div#content h1').text.split('::')[0].strip()

    book_author = soup.select_one('h1 a')
    if book_author:
        book_author = book_author.text.strip()

    genre_elements = soup.select('span.d_book a')
    genres = [genre.text.strip() for genre in genre_elements]

    comments = []
    comment_divs = soup.select('div.texts')
    for comment_div in comment_divs:
        comment_text = comment_div.select_one('span.black').text.strip()
        comments.append(comment_text)

    book_img = soup.select_one('div.bookimage img')
    book_img_url = book_img['src'] if book_img else None

    book = {
        'title':book_title,
        'author':book_author,
        'genres':genres,
        'comments':comments,
        'img':book_img_url
    }

    return book


def download_book(url, params, filename, folder='books/'):
    os.makedirs(folder, exist_ok=True)
    response = requests.get(url, params=params)
    response.raise_for_status()
    check_for_redirect(response)
    file_path = os.path.join(folder, sanitize_filename(filename))
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(response.text)


def download_cover(url, folder='/images'):
    os.makedirs(folder, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()

    file_name = os.path.basename(urlparse(url).path)
    file_number = file_name.replace("images", "")
    new_file_name = os.path.join(folder, file_number)

    with open(new_file_name, 'wb') as file:
        file.write(response.content)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Скрипт для парсинга библиотеки'
    )
    parser.add_argument(
        'start_page',
        help='Начальная страница',
        default=1,
        type=int
    )
    parser.add_argument(
        'end_page',
        help='Последняя страница',
        default=10,
        type=int
    )
    parser.add_argument(
        '--skip_imgs',
        help='не скачивать картинки',
        action="store_true"
    )
    parser.add_argument(
        '--skip_txt',
        help='не скачивать книги',
        action="store_true"
    )
    parser.add_argument(
        '--dest_folder',
        help='путь к картинкам, книгам, JSON',
        default="media",
        type=str
    )

    args = parser.parse_args()

    start_page = args.start_page
    end_page = args.end_page

    books = []
    books_urls = get_urls_books(start_page, end_page)
    loading_book_url = "https://tululu.org/txt.php"

    for book_url in books_urls:
        book_number = urlparse(book_url).path.split("/")[1][1:]
        params = {"id": book_number}
        try:
            page_response = requests.get(book_url)
            page_response.raise_for_status()
            check_for_redirect(page_response)

            book = parse_book_page(page_response)
            books.append(book)
            img_file_path = book["img"]
            if not args.skip_imgs:
                full_img_url = urljoin(book_url, img_file_path)
                folder = 'images'
                path = os.path.join(args.dest_folder, folder)
                download_cover(full_img_url, path)
            if not args.skip_txt:
                book_filename = f"{book['title']}.txt"
                folder = 'books'
                path = os.path.join(args.dest_folder, folder)
                download_book(loading_book_url, params, book_filename, path)

        except requests.HTTPError:
            sys.stderr.write("HTTPError\n")
        except requests.ConnectionError:
            sys.stderr.write("ConnectionError\n")
            time.sleep(5)
    folder = args.dest_folder
    os.makedirs(folder, exist_ok=True)
    filename = "book_parse.json"
    path = os.path.join(folder, sanitize_filename(filename))
    with open(path, 'w', encoding="utf-8") as json_file:
        json.dump(books, json_file, ensure_ascii=False)