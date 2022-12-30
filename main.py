# Documentation => https://tedboy.github.io/bs4_doc/1_quick_start.html

import requests
from bs4 import BeautifulSoup
import functions
import helpers

url = "http://books.toscrape.com/index.html"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

# 1- scraping books of home page
articles = []

for article in soup.find_all('article', {'class': 'product_pod'}):
    articles.append(article)

books = functions.get_books(articles)
functions.dict_to_csv('data.csv', books, ["title","price", "link", "in stock", "ratings"])

# 2- scraping all books (every page)
booksUrls = []
pages_count = 1
index = 1
all_articles = []
all_books = []
if soup.find('ul', {'class': 'pager'}):
   pages = soup.find('li', {'class': 'current'}).text.replace("\n", "").split(" ")
   pages = list(filter(lambda p: p != "", pages))
   pages_count = int(pages[-1])

while index < pages_count:
    url = "http://books.toscrape.com/catalogue/page-" + str(index) + ".html"
    booksUrls.append(url)
    index +=1

all_books = functions.get_all_books(booksUrls)
functions.dict_to_csv('all_data.csv', all_books, ["title","price", "link", "in stock", "ratings"])
 
# 3- scraping all books from every category
categories = {}
categories_links = {}
catUrls = []
all_books_by_category = []
_articles = []
p_count = 0

for a in soup.find('div', {'class': 'side_categories'}).ul.find_all('a'):
    urls = []
    category = a.text.replace('\n', '').replace('  ', '')
    if 'books_1' not in a.get('href'):
        urls.append('http://books.toscrape.com/' + a.get('href'))
    categories[category] = 'http://books.toscrape.com/' + a.get('href')


for category, _url in categories.items():
    cat_page = requests.get(_url)
    cat_soup = BeautifulSoup(cat_page.content, 'html.parser')
    if cat_soup.find('ul', {'class': 'pager'}):
        p = cat_soup.find('li', {'class': 'current'}).text.replace("\n", "").split(" ")
        p = list(filter(lambda i: i != "", p))
        p_count = int(p[-1])
        _urls = functions.get_books_by_category(_url, p_count)
        categories_links[category] = _urls
    else:
        categories_links[category] = [_url]

functions.get_all_books_by_category(categories_links.items())