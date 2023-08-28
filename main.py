# -*- coding: utf-8 -*-
import sys
import time

import requests
from pathlib import Path
from bs4 import BeautifulSoup
import pathvalidate
import os
import argparse


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def parse_book_page(book_number):
    try:
        url = f"https://tululu.org/b{book_number}/"
        response = requests.get(url)
        response.raise_for_status()

        try:
            check_for_redirect(response)
        except requests.HTTPError:
            return None, None, None, None, None

        soup = BeautifulSoup(response.text, 'lxml')

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

        return book_title, book_author, genres, comments, book_img

    except requests.exceptions.HTTPError as e:
        sys.stderr.write(f"HTTPError: {e}\n")
    except requests.exceptions.ConnectionError as e:
        sys.stderr.write(f"ConnectionError: {e}\n")
        time.sleep(5)
    except Exception as e:
        sys.stderr.write(f"An error occurred: {e}\n")

    return None, None, None, None, None


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("start_id", type=int, help="Начальная страница")
    parser.add_argument("end_id", type=int, help="Последняя страница")
    args = parser.parse_args()

    start_id = args.start_id
    end_id = args.end_id

    for book_number in range(start_id, end_id):
        title, author, genres, comments, img = parse_book_page(book_number)
        if title:
            print(f"Автор: {author}")
            if genres:
                print(f"Жанры: {', '.join(genres)}")
            if comments:
                for i, comment in enumerate(comments, 1):
                    print(f"Comment {i}: {comment}")