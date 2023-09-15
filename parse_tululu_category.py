# -*- coding: utf-8 -*-
import requests

from bs4 import BeautifulSoup
from check_for_redirect import check_for_redirect
from urllib.parse import urljoin
from time import sleep


def get_urls_books(start_page, end_page):
    book_urls = []
    for page in range(start_page, end_page):
        try:
            url = f"https://tululu.org/l55/{page}"
            response = requests.get(url)
            check_for_redirect(response)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            books = soup.find_all('table', class_="d_book")
            for book in books:
                book = book.find('a')['href']
                book_url = urljoin(url, book)
                book_urls.append(book_url)
        except requests.HTTPError:
            print("Такой страницы нету")
        except requests.ConnectionError:
            print("Повторное подключение")
            sleep(20)
    return book_urls
