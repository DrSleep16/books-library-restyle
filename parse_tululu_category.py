# -*- coding: utf-8 -*-
import requests

from bs4 import BeautifulSoup
from main import check_for_redirect
from urllib.parse import urljoin


book_urls = []
try:
    url = "https://tululu.org/l55/1"
    response = requests.get(url)
    check_for_redirect(response)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    book_ids = soup.find_all('table', class_="d_book")
    for book_id in book_ids:
        book_id = book_id.find('a')['href']
        book_url = urljoin(url, book_id)
        book_urls.append(book_url)
except requests.HTTPError:
    print("Такой страницы нету")
except requests.ConnectionError:
    print("Ошибка подключения")

print(book_urls)