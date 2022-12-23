# Documentation => https://tedboy.github.io/bs4_doc/1_quick_start.html

import requests
from bs4 import BeautifulSoup
import functions

url = "http://books.toscrape.com/index.html"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

booksUrls = []
articles = []
all_articles = []
all_books = []
pages_count = 1
index = 1
 
# 1- scraping books of home page
for article in soup.find_all('article', {'class': 'product_pod'}):
    articles.append(article)

books = functions.getBooks(articles)

# for book in books:
#     del book["page"]
    

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


def get_all_books():
    _articles = []
    for url in booksUrls:
        page_number = url.split("-").pop(-1).split(".")[0]
        print("scraping page#" + str(page_number))
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        for article in soup.find_all('article', {'class': 'product_pod'}):
            _articles.append(article)
    _articles = functions.getBooks(_articles)
    return _articles

all_books = get_all_books()
functions.dict_to_csv('all_data.csv', all_books, ["title","price", "link", "in stock", "ratings"])
 