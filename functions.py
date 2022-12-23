import csv
import requests
from bs4 import BeautifulSoup
url = "http://books.toscrape.com/index.html"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

articles = []
books = []

for article in soup.find_all('article', {'class': 'product_pod'}):
    articles.append(article)

def getBooks(): 
    for article in articles:
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

