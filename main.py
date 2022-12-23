# Documentation => https://tedboy.github.io/bs4_doc/1_quick_start.html

import csv
import requests
from bs4 import BeautifulSoup
import functions
url = "http://books.toscrape.com/index.html"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')


booksUrls = []
pages_count = 1
if soup.find('ul', {'class': 'pager'}):
   pages = soup.find('li', {'class': 'current'}).text.replace("\n", "").split(" ")
   pages = list(filter(lambda p: p != "", pages))
   pages_count = int(pages[-1])

# http://books.toscrape.com/catalogue/page-2.html
index = 1
while index < pages_count:
    url = "http://books.toscrape.com/catalogue/page-" + str(index) + ".html"
    booksUrls.append(url)
    index +=1
    # page = requests.get(url)
    # soup = BeautifulSoup(page.content, 'html.parser')



def dict_to_csv(items, field_names) :
    try:
        with open('data.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(items)
    except IOError:
        print("I/O error")

books = functions.getBooks()
dict_to_csv(books, ["title","price", "link", "in stock", "ratings"])
