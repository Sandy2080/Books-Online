import csv
import requests
import helpers
from bs4 import BeautifulSoup
url = "http://books.toscrape.com/index.html"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')


# Transform
def get_books(articles): 
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
        image_url = helpers.get_image_url('http://books.toscrape.com/', 'a img', article) 
        download_img(title, image_url)
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
    _articles = get_books(_articles)
    return _articles

def get_books_by_category(url, count):
    _catUrls = []
    index = 1
    while index <= count:
        _url = url.split("/")[ : -1]
        _url = list(filter(lambda el: el != "", _url))
        _url = list(map(helpers.update, _url))
        _url = "/".join(_url) 
        _url = _url + "/" + "page-" + str(index) + ".html"
        _catUrls.append(_url)
        index +=1
    return _catUrls

def get_all_books_by_category(categories):
    _books = []
    for category, _urls in categories:
        _articles = []
        for u in _urls:
            p = requests.get(u)
            s = BeautifulSoup(p.content, 'html.parser')
            for article in s.find_all('article', {'class': 'product_pod'}):
                _articles.append(article)
            _books = get_books(_articles)
        for b in _books:
            b["link"] = b["link"].replace("/../../", "/")
            _books.append(b)
        filename = str(category).lower()+".csv"
        dict_to_csv("categories/"+filename, _books, ["title","price", "link", "in stock", "ratings"])

# Load
def dict_to_csv(filename, items, field_names) :
    try:
        with open(filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(items)
    except IOError:
        print("I/O error")

def download_img(title, img_url):
    img = img_url.split("/")[-1]
    filename = "images/"+img
    img_data = requests.get(img_url).content
    try:
        with open(filename, 'wb') as handler: 
            handler.write(img_data) 
    except IOError:
        print("I/O error:" + str(IOError))