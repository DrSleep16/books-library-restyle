# -*- coding: utf-8 -*-
import requests
from pathlib import Path
from bs4 import BeautifulSoup
import pathvalidate
import os


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def get_book_title(book_number):
    url = f"https://tululu.org/b{book_number}/"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    content_div = soup.find('div', id='content')
    book_title = content_div.find('h1') if content_div else None

    if book_title:
        return book_title.text.split('::')[0].strip()


def get_book_cover(book_number):
    url = f"https://tululu.org/b{book_number}/"
    response = requests.get(url)
    response.raise_for_status()

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

    soup = BeautifulSoup(response.text, 'lxml')

    genre_elements = soup.select('span.d_book a')

    genres = [genre.text.strip() for genre in genre_elements]

    return genres

if __name__ == '__main__':
    for book_number in range(10):
        url = f"https://tululu.org/txt.php?id={book_number+1}"
        # filepath = get_book_txt(url, str(book_number + 1), 'books/')
        # print(filepath)
        # img = get_book_cover(book_number)
        title = get_book_title(book_number)
        if title:
            print(title)
            comments = get_book_comments(book_number)
            if comments:
                for i, comment in enumerate(comments, 1):
                    print(f"Comment {i}:\n{comment}\n")
            genres = get_book_genres(book_number)
            if genres:
                print(f"Жанры: {', '.join(genres)}")
