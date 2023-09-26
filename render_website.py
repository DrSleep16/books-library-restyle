# -*- coding: utf-8 -*-
import json
import os
import more_itertools
import math
import argparse

from jinja2 import Environment, FileSystemLoader
from livereload import Server


def rebuild(json_file_path):
    with open(json_file_path, 'r', encoding="utf-8") as json_file:
        books = json.load(json_file)
    total_books = len(books)
    book_pages = list(more_itertools.chunked(books, 20))
    total_pages = math.ceil(total_books / 20)
    for page_num, page_books in enumerate(book_pages, start=1):
        env = Environment(loader=FileSystemLoader("."))
        template = env.get_template("template.html")
        render_html = template.render(
            books=page_books,
            current_page=page_num,
            total_pages=total_pages
        )
        page_filename = f"pages/index{page_num}.html"
        with open(page_filename, 'w', encoding="utf-8") as html_file:
            html_file.write(render_html)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--json',
        default='media/book_parse.json',
        help='Путь к файлу book_parse.json'
    )
    args = parser.parse_args()

    if not os.path.exists("pages"):
        os.makedirs("pages")

    rebuild(args.json)
    server = Server()
    server.watch('template.html', lambda: rebuild(args.json))
    server.serve(root='.')
