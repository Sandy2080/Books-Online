# Documentation => https://tedboy.github.io/bs4_doc/1_quick_start.html

import requests
from bs4 import BeautifulSoup
import functions

url = "http://books.toscrape.com/index.html"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

categories = {}
articles = []
all_articles = []
all_books = []
booksUrls = []
pages_count = 1
index = 1
 
# 1- scraping books of home page
for article in soup.find_all('article', {'class': 'product_pod'}):
    articles.append(article)

books = functions.getBooks(articles)
functions.dict_to_csv('data.csv', books, ["title","price", "link", "in stock", "ratings"])

# 2- scraping books of all pages of the catalogue
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
for a in soup.find('div', {'class': 'side_categories'}).ul.find_all('a'):
    urls = []
    category = a.text.replace('\n', '').replace('  ', '')
    if 'books_1' not in a.get('href'):
        urls.append('http://books.toscrape.com/' + a.get('href'))
    categories[category] = 'http://books.toscrape.com/' + a.get('href')


def get_books(url):
    cat_articles = []

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    for article in soup.find_all('article', {'class': 'product_pod'}):
        cat_articles.append(article)
    return cat_articles
    


# for category, url in categories.items():  
#     print(url)
#     articles = get_books(url)
#     books = functions.getBooks(articles) 
#     filename = str(category).lower()+".csv"
#     functions.dict_to_csv(filename, books, ["title","price", "link", "in stock", "ratings"])
