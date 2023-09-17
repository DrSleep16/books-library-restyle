import json
import os
import more_itertools
import math

from jinja2 import Environment, FileSystemLoader
from livereload import Server


def rebuild():
    with open("media/book_parse.json", 'r', encoding="utf-8") as json_file:
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
    if not os.path.exists("pages"):
        os.makedirs("pages")
    rebuild()
    server = Server()
    server.watch('template.html', rebuild)
    server.serve(root='')
