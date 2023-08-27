import requests
from bs4 import BeautifulSoup
import sys


sys.stdout.reconfigure(encoding='utf-8')
url = 'https://www.franksonnenbergonline.com/blog/are-you-grateful/'
response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'lxml')
# print(soup.prettify())
# print(soup.find('h1'))
# title_tag = soup.find('main').find('header').find('h1')
# print(title_tag.text)
# image_post = soup.find('img', class_='attachment-post-image')['src']
# print(image_post)
post_text = soup.find(class_='entry-content')
print(post_text.text)