# Documentation => https://tedboy.github.io/bs4_doc/1_quick_start.html

import csv
import requests
from bs4 import BeautifulSoup
url = "http://books.toscrape.com/index.html"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
# print(soup.get_text()) - DOES NOT WORK !!!

#for link in soup.find_all('a'):
    #print(link.get('href'))

# print("\n **** BOOKS ONLINE **** \n")
categories = {}
products = []

# scrapping and storing books categories in a dictionnary
for a in soup.find('div', {'class': 'side_categories'}).ul.find_all('a'):
    if 'books_1' not in a.get('href'):
        link = categories[a.text.replace('\n', '').replace('  ', '')] = 'http://books.toscrape.com/' + a.get('href')
        # print(link)
        # print(categories)

print("\n")
titles_arr = []
prices_arr = []
links_arr = []
cat_arr = []
stocks_arr = []
ratings_arr = []
# querying categories url 
for category, catUrl in categories.items():
    htmlResponse = requests.get(catUrl)
    soup = BeautifulSoup(htmlResponse.content, 'html.parser')
    url = soup.find('div', {'class': 'image_container'}).find('a')
    dict = {}
    #category
    cat_arr.append(category)
    #title
    title = soup.h3.a.get('title')
    titles_arr.append(title)
    #title
    price = soup.find('p', {'class': 'price_color'})
    prices_arr.append(price.text)
    #link
    link = 'http://books.toscrape.com/catalogue/' + url.get('href').replace("../../../", "")
    links_arr.append(link)
    #in stock
    stock = soup.find('p', {'class': 'instock availability'})
    stock = stock.text.replace("\n", "").replace(" ", "") 
    is_in_stock = "In stock" if stock == "Instock" else "not available"
    stocks_arr.append(is_in_stock)
    
    #review rating
    star_rating = soup.find('p', {'class', 'star-rating'}).get('class')
    ratings_arr.append(star_rating[1])
    products.append(
        { "category": category, 
         "title": title, 
         "price": price.text, 
         "link": link, 
         "in stock": is_in_stock, 
         "ratings": star_rating[1]
         })
   
def write_to_csv() :
    try:
        with open('data.csv', 'w') as csvfile:
              writer = csv.writer(csvfile, delimiter=',')
              writer.writerow(field_names)
              for category, title, price, link, stock, rating in zip(cat_arr, titles_arr, prices_arr, links_arr, stocks_arr, ratings_arr):
                row = [category, title, price, link, stock, rating]
                writer.writerow(row)
    except IOError:
        print("I/O error")


field_names = ["category", "title","price", "link", "in stock", "ratings"]
def dict_to_csv() :
    try:
        with open('data.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(products)
    except IOError:
        print("I/O error")

dict_to_csv()
