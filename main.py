# Documentation => https://tedboy.github.io/bs4_doc/1_quick_start.html

import csv
import requests
from bs4 import BeautifulSoup
url = "http://books.toscrape.com/index.html"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

products = []

def getBooks(): 
    for article in soup.find('article', {'class': 'product_pod'}):
        ratings_arr = []
        link = 'http://books.toscrape.com/catalogue/' + soup.find("div", {'class', 'image_container'}).a.get('href')
        title = soup.h3.a.get('title')
        stock = soup.find('p', {'class': 'instock availability'})
        stock = stock.text.replace("\n", "").replace(" ", "") 
        is_in_stock = "In stock" if stock == "Instock" else "not available"
        price = soup.find('p', {'class': 'price_color'})
        star_rating = soup.find('p', {'class', 'star-rating'}).get('class')
        ratings_arr.append(star_rating[1])
        products.append(
            {  
            "title": title, 
            "price": price.text, 
            "link": link, 
            "in stock": is_in_stock, 
            "ratings": star_rating[1]
        })
    return products


arr = getBooks()
print(arr)
