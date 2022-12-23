# Documentation => https://tedboy.github.io/bs4_doc/1_quick_start.html

import csv
import requests
from bs4 import BeautifulSoup
url = "http://books.toscrape.com/index.html"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

books = []
articles = []
for article in soup.find_all('article', {'class': 'product_pod'}):
    articles.append(article)

def getBooks(): 
    for article in articles:
        print(article)
        ratings_arr = []
        link = 'http://books.toscrape.com/catalogue/' + article.find("div", {'class', 'image_container'}).a.get('href')
        title = article.h3.a.get('title')
        stock = article.find('p', {'class': 'instock availability'})
        stock = stock.text.replace("\n", "").replace(" ", "") 
        is_in_stock = "In stock" if stock == "Instock" else "not available"
        price = article.find('p', {'class': 'price_color'})
        star_rating = article.find('p', {'class', 'star-rating'}).get('class')
        ratings_arr.append(star_rating[1])
        books.append(
            {  
            "title": title, 
            "price": price.text, 
            "link": link, 
            "in stock": is_in_stock, 
            "ratings": star_rating[1]
        })
    return books



def dict_to_csv(items, field_names) :
    try:
        with open('data.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(items)
    except IOError:
        print("I/O error")

books = getBooks()
print(books)
dict_to_csv(books, ["title","price", "link", "in stock", "ratings"])
