# Documentation => https://tedboy.github.io/bs4_doc/1_quick_start.html

import requests
from bs4 import BeautifulSoup
url = "http://books.toscrape.com/index.html"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
# print(soup.get_text()) - DOES NOT WORK !!!

for link in soup.find_all('a'):
    print(link.get('href'))


print("\n **** BOOKS ONLINE **** \n")
categories = {}
products = {}

# scrapping and storing books categories in a dictionnary
for a in soup.find('div', {'class': 'side_categories'}).ul.find_all('a'):
    if 'books_1' not in a.get('href'):
        categories[a.text.replace('\n', '').replace('  ', '')] = 'http://books.toscrape.com/' + a.get('href')
        print(categories)

print("\n")

# querying categories url 
for categorie, catUrl in categories.items():
    htmlResponse = requests.get(catUrl)
    soup = BeautifulSoup(htmlResponse.content, 'html5lib')
    url = soup.find('div', {'class': 'image_container'}).find('a')
    title = soup.h3.a.get('title')
    products["title"] = title
    price = soup.find('p', {'class': 'price_color'})
    products["price"] = price
    link = 'http://books.toscrape.com/catalogue/' + url.get('href').replace("../../../", "")
    products["link"] = link
    print(products)

booksUrl = []