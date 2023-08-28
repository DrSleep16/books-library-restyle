# -*- coding: utf-8 -*-
import requests
from pathlib import Path
from bs4 import BeautifulSoup
import pathvalidate
import os
import argparse


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def get_book_title(book_number):
    url = f"https://tululu.org/b{book_number}/"
    response = requests.get(url)
    response.raise_for_status()

    try:
        check_for_redirect(response)
    except requests.HTTPError:
        return 'redirect'

    soup = BeautifulSoup(response.text, 'lxml')
    content_div = soup.find('div', id='content')
    book_title = content_div.find('h1') if content_div else None

    if book_title:
        return book_title.text.split('::')[0].strip()


def get_book_cover(book_number):
    url = f"https://tululu.org/b{book_number}/"
    response = requests.get(url)
    response.raise_for_status()

    try:
        check_for_redirect(response)
    except requests.HTTPError:
        return 'redirect'

    soup = BeautifulSoup(response.text, 'lxml')
    book_img = soup.find(class_='bookimage').find('img') if soup.find(class_='bookimage') else None

    if book_img:
        img_url = 'https://tululu.org' + book_img['src']
        img_response = requests.get(img_url)
        img_response.raise_for_status()
        os.makedirs('images', exist_ok=True)

        if img_url.endswith('nopic.gif'):
            img_filename = 'images/nopic.gif'
        else:
            img_filename = f'images/{book_number}.jpg'

        with open(img_filename, 'wb') as img_file:
            img_file.write(img_response.content)

        return img_filename
    else:
        return None


def get_book_txt(url, book_number, folder='books/'):
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


def get_book_comments(book_number):
    url = f"https://tululu.org/b{book_number}/"
    response = requests.get(url)
    response.raise_for_status()

    try:
        check_for_redirect(response)
    except requests.HTTPError:
        return 'redirect'

    soup = BeautifulSoup(response.text, 'lxml')
    comments = []

    comment_divs = soup.find_all('div', class_='texts')
    for comment_div in comment_divs:
        comment_text = comment_div.find('span', class_='black')
        if comment_text:
            comments.append(comment_text.text.strip())

    return comments


def get_book_genres(book_number):
    url = f"https://tululu.org/b{book_number}/"
    response = requests.get(url)
    response.raise_for_status()

    try:
        check_for_redirect(response)
    except requests.HTTPError:
        return 'redirect'

    soup = BeautifulSoup(response.text, 'lxml')

    genre_elements = soup.select('span.d_book a')

    genres = [genre.text.strip() for genre in genre_elements]

    return genres


def parse_book_page(html_content):
    soup = BeautifulSoup(html_content, 'lxml')

    book_title = soup.select_one('div#content h1').text.split('::')[0].strip()

    book_author = soup.select_one('span[itemprop="author"] a')
    if book_author:
        book_author = book_author.text.strip()
    else:
        book_author = "Unknown Author"

    genre_elements = soup.select('span.d_book a')
    genres = [genre.text.strip() for genre in genre_elements]

    comments = []
    comment_divs = soup.select('div.texts')
    for comment_div in comment_divs:
        comment_text = comment_div.select_one('span.black').text.strip()
        comments.append(comment_text)

    book_img = soup.select_one('div.bookimage img')
    if book_img:
        book_img = book_img['src']
    else:
        book_img = None

    book = {
        'title': book_title,
        'author': book_author,
        'genres': genres,
        'comments': comments,
        'image_url': book_img
    }
    return book


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("start_id", type=int, help="Начальная страница")
    parser.add_argument("end_id", type=int, help="Последняя страница")
    args = parser.parse_args()

    start_id = args.start_id
    end_id = args.end_id

    for book_number in range(start_id, end_id):
        params = {
            'id':str(book_number)
        }
        url = requests.get("https://tululu.org/txt.php", params=params).url
        filepath = get_book_txt(url, str(book_number), 'books/')
        img = get_book_cover(book_number)
        title = get_book_title(book_number)
        if title:
            print(title)
            genres = get_book_genres(book_number)
            if genres:
                print(f"Жанры: {', '.join(genres)}")
            comments = get_book_comments(book_number)
            if comments:
                for i, comment in enumerate(comments, 1):
                    print(f"Comment {i}:{comment}")

