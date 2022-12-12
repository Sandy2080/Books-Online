import requests
from bs4 import BeautifulSoup
url = "https://www.gov.uk/search/news-and-communications"
page = requests.get(url)
# Voir le code html source

soup = BeautifulSoup(page.content, 'html.parser')
links = soup.find_all('a')

def content(arr):
    results = []
    for i in arr:
        results.append({ "content": i.string, "link": i['href']})
    return results
results = content(links)

for r in results:
    print(r["content"])
    print(r["link"])
# print(results)
