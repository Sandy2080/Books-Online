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

    products.append({ "category": category, "title": title, "price": price.text, "link": link})
   



def write_to_csv() :
    try:
        with open('data.csv', 'w') as csvfile:
              writer = csv.writer(csvfile, delimiter=',')
              writer.writerow(field_names)
              for category, title, price, link in zip(cat_arr, titles_arr, prices_arr, links_arr):
                row = [category, title, price, link]
                print(row)
                writer.writerow(row)
    except IOError:
        print("I/O error")

print(products)
field_names = ["category", "title","price", "link"]
def dict_to_csv() :
    try:
        with open('data.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(products)
    except IOError:
        print("I/O error")

dict_to_csv()
