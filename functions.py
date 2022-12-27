import csv
import requests
from bs4 import BeautifulSoup
url = "http://books.toscrape.com/index.html"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

def page_number(page):
    if page is not None:
        current = page.text.replace("\n", "").split(" ")
        current = list(filter(lambda c: c != "", current))
        current.pop(0)
    return current[0]

def getBooks(articles): 
    books = []
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


def get_all_books(urls):
    _articles = []
    for url in urls:
        page_number = url.split("-").pop(-1).split(".")[0]
        # print("scraping page#" + str(page_number))
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        for article in soup.find_all('article', {'class': 'product_pod'}):
            _articles.append(article)
    _articles = getBooks(_articles)
    return _articles


def dict_to_csv(filename, items, field_names) :
    try:
        with open(filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(items)
    except IOError:
        print("I/O error")


def get_books_by_category(categories):
    for category, url in categories:
        cat_articles = []
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        for article in soup.find_all('article', {'class': 'product_pod'}):
            cat_articles.append(article)
        books = get_all_books(cat_articles)
        filename = str(category).lower()+".csv"
        dict_to_csv("categories/"+filename, books, ["title","price", "link", "in stock", "ratings"])
