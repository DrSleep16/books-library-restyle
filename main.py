# -*- coding: utf-8 -*-
import os
import sys
import time
from pathlib import Path
from urllib.parse import urljoin

import pathvalidate
import requests
from bs4 import BeautifulSoup
import argparse


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


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

    book = {
        'title':book_title,
        'author':book_author,
        'genres':genres,
        'comments':comments,
        'img':book_img
    }
    return book


def download_book(book_number, book_title):
    params = {
        'id':book_number
    }
    url = "https://tululu.org/txt.php"
    response = requests.get(url, params=params)
    response.raise_for_status()
    check_for_redirect(response)
    Path('books/').mkdir(parents=True, exist_ok=True)
    safe_filename = pathvalidate.sanitize_filename(f'{book_number}. {book_title}')
    file_path = Path(f'books/{safe_filename}.txt')
    with open(file_path, 'w') as file:
        file.write(response.text)


def download_cover(book_number, relative_url):
    book_url = f"https://tululu.org/b{book_number}/"
    response = requests.get(book_url)
    response.raise_for_status()

    base_url = response.url

    img_url = urljoin(base_url, relative_url)
    img_response = requests.get(img_url)
    img_response.raise_for_status()
    os.makedirs('images', exist_ok=True)

    if img_url.endswith('nopic.gif'):
        book_img = 'images/nopic.gif'
    else:
        book_img = f'images/{book_number}.jpg'

    with open(book_img, 'wb') as img_file:
        img_file.write(img_response.content)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Скрипт для парсинга библиотеки')
    parser.add_argument("start_id", type=int, help="Начальная страница")
    parser.add_argument("end_id", type=int, help="Последняя страница")
    args = parser.parse_args()

    start_id = args.start_id
    end_id = args.end_id

    for book_number in range(start_id, end_id):
        try:
            url = f"https://tululu.org/b{book_number}/"
            response = requests.get(url)
            response.raise_for_status()
            check_for_redirect(response)
            book = parse_book_page(response)
            download_book(book_number, book_title=book['title'])
            download_cover(book_number, relative_url=book['img']['src'])

        except requests.HTTPError:
            sys.stderr.write("HTTPError\n")
        except requests.ConnectionError:
            sys.stderr.write("ConnectionError\n")
            time.sleep(5)
