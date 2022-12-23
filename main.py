# Documentation => https://tedboy.github.io/bs4_doc/1_quick_start.html

import requests
from bs4 import BeautifulSoup
import functions

url = "http://books.toscrape.com/index.html"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')


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

all_books = functions.get_all_books(booksUrls)
functions.dict_to_csv('all_data.csv', all_books, ["title","price", "link", "in stock", "ratings"])
 