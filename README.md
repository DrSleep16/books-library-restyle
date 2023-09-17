## ��� ������������ ������ ��� ���������� ���� � ����� tululu.org

���� ������ ��������� ��������� ����� � ����� [tululu.org](https://tululu.org), � ��� �� �������� ����������� ���������� ����. ������ ����� ��������� ��������� ����� ���� � �������, � ����� ��������� ���������� � ������ � ��������� � � JSON-����.

### ��������� ������������

����� ���������� ��� �����������, ��������� ��������� ����:

1. ��������� � �������, ���������� ���� `requirements.txt`.

2. �������� ��������� ������ (��������) � ��������� ��������� �������:

   ```bash
   pip install -r requirements.txt
   ```

   ��� ������� ������������� ��������� ��� ������ � ������, ��������� � ����� `requirements.txt`.
### �������������

1. ���������� ������ `main.py` � ���� ������� �������.

2. �������� ��������� ������ (��������) � ��������� � �������, ��� ��������� ������ `main.py`.

3. ��������� ������ � ������� ��������� ������, ������ ��������� ���������:

   ```
   python main.py <start_page> <end_page> [--skip_imgs] [--skip_txt]
   ```

   - `<start_page>`: ����� ��������� �������� ��� ���������� ���� (������������ ��������).
   - `<end_page>`: ����� ��������� �������� ��� ���������� ���� (������������ ��������).
   - `--skip_imgs`: ������������ ���� ��� �������� ���������� ������� ����. ���� ���� ���� ������, ������� �� ����� �����������.
   - `--skip_txt`: ������������ ���� ��� �������� ���������� ��������� ������ ����. ���� ���� ���� ������, ��������� ����� �� ����� �����������.

4. ������� �������������:

   - ��� ���������� ���� ���� � 1-�� �� 10-�� ��������:
     ```
     python main.py 1 10
     ```

   - ��� ���������� ������ ���������� � ������ (��� ���������� ������) � 5-�� �� 15-�� ��������:
     ```
     python main.py 5 15 --skip_imgs --skip_txt
     ```


### �������������� ����������

#### ��� ��� ��������

1. ������ �������� � ��������� ��������� �������� � ����������� �� ��������� ��������� ��������.
2. ��� ������ �������� �������� ������ URL-�� ���� � ������� ������� `get_urls_books` �� ������ `parse_tululu_category.py`.
3. ����� ������ ���������� ��������� �� ������� URL-� ����� � �������� ���������� � �����, ������� ���������, ������, �����, ����������� � ������ �� �������.
4. ���� ������ ���� `--skip_imgs`, ������ ���������� ���������� �������, ����� ��������� ������� � ����� "images".
5. ���� ������ ���� `--skip_txt`, ������ ���������� ���������� ��������� ������ ����, ����� ��������� �� � ����� "books".
6. ���������� � ������ ��������� ����� ����������� � JSON-����� "book_parse.json".


### �������� ����� `render_website.py`

���� ������ Python, `render_website.py`, ������������ ��� ������������ ��������� ����������� HTML-������� �� ������ ������ �� JSON-����� � ������� HTML. ��������������� �������� ����������� �� ��������� ������, � ����������� ������������� �������� ��� ������������ ����� ����������.

## ��� ��� ��������

1. **������ ���������:**
   - ������� ������������� ����������� ���������� � ������, ����� ��� `json`, `os`, `more_itertools`, `math`, `jinja2`, � `livereload`.

2. **������� `rebuild`:**
   - ������� `rebuild` ��������� ��������� ����:
      - ��������� JSON-���� `"media/book_parse.json"`, ���������� ������ � ������, � ��������� ��� � ���������� `books`.
      - ��������� ������ ���� �� ��������� �������, ��� ������ �������� �������� �� 20 ����, ��������� ������ `more_itertools.chunked`. ��������� ����������� � ���������� `book_pages`.
      - ������������ ����� ���������� ������� `total_pages`, �������� ����� ��������� ������� ������ ���������� ���� �� 20.
      - ����� �������� �� ������ �������� ����, ��������� ���� `for`, � ��� ������ ��������:
        - ��������� ������ HTML �� ����� `"template.html"` � ������� Jinja2.
        - �������� HTML, ��������� ������ � ������, ������� �������� � ����� ���������� �������.
        - ��������� ��������������� HTML � ���� � ������ `"pages/index{page_num}.html"`, ��� `{page_num}` - ����� ��������.

3. **�������� ����:**
   - � �������� ����� ���� ����������� ���������:
     - �����������, ���� ���������� `"pages"` �� ����������, �� ��� ��������� � ������� `os.makedirs`.
     - ����� ���������� ������� `rebuild()`, ����� ������������� �������� ��� ������� �������.
     - ��������� ������ `Server()` �� ���������� `livereload`, ������� ������ �� ����������� � ����� `"template.html"` � ������������� ����������� �������� ��� �� ���������.
     - ����������� ������ ��� ������� ������� � �������� ����� `''`.

���� ������ ��������� ��������� ��������������� ���-���� �� ������ ������ �� JSON � ������� HTML, � ����� ������������ �������������� ���������� ������� ��� ��������� �������.

### ����: https://drsleep16.github.io/books-library-restyle

### �������� �����:
![img.png](static/screenshot.png)
#### �������������� �����

- `check_for_redirect.py`: ������ ��� �������� ��������������� HTTP-��������.
- `parse_tululu_category.py`: ������ ��� ��������� URL-�� ���� �� ��������� �����.

### �����
������� �������