# Documentation => https://tedboy.github.io/bs4_doc/1_quick_start.html

import requests
from bs4 import BeautifulSoup
import functions

url = "http://books.toscrape.com/index.html"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')


# 1- scraping books of home page
articles = []

for article in soup.find_all('article', {'class': 'product_pod'}):
    articles.append(article)

books = functions.getBooks(articles)
functions.dict_to_csv('data.csv', books, ["title","price", "link", "in stock", "ratings"])

# 2- scraping books of all pages of the catalogue
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
 
# 3- scraping books from all categories
categories = {}
_categories_links = {}
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


# if soup.find('ul', {'class': 'pager'}):
#    pages = soup.find('li', {'class': 'current'}).text.replace("\n", "").split(" ")
#    pages = list(filter(lambda p: p != "", pages))
#    pages_count = int(pages[-1])

# while index < pages_count:
#     url = "http://books.toscrape.com/catalogue/page-" + str(index) + ".html"
#     booksUrls.append(url)
#     index +=1

def get_all_categories_articles(url, count):
    _catUrls = []
    index = 1
    while index < count:
        _url = url.split("/")[ : -1]
        _url = list(filter(lambda i: i != "", _url))
        _url = "/".join(_url) 
        _url = _url + "/" + "page-" + str(index) + ".html"
        _catUrls.append(_url)
        index +=1
    return _catUrls

for category, _url in categories.items():
    cat_page = requests.get(_url)
    cat_soup = BeautifulSoup(cat_page.content, 'html.parser')
    if cat_soup.find('ul', {'class': 'pager'}):
        p = cat_soup.find('li', {'class': 'current'}).text.replace("\n", "").split(" ")
        p = list(filter(lambda i: i != "", p))
        p_count = int(p[-1])
    _urls = get_all_categories_articles(_url, p_count)
    _categories_links[category] = urls

# print(_categories_links)
    

    # page = requests.get(url)
    # soup = BeautifulSoup(page.content, 'html.parser')
    # for article in soup.find_all('article', {'class': 'product_pod'}):
    #     _articles.append(article)
    # books = functions.get_all_books(url)
    # all_books_by_category = getBooks(books)
    # print(all_books_by_category)

# functions.get_books_by_category(categories.items())