import json

from jinja2 import Environment, FileSystemLoader


with open("media/book_parse.json", 'r', encoding="utf-8") as json_file:
    books = json.load(json_file)
env = Environment(loader=FileSystemLoader("."))
template = env.get_template("template.html")
render_html = template.render(books=books)
with open("index.html", 'w', encoding="utf-8") as html_file:
    html_file.write(render_html)