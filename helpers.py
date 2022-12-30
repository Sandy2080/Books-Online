def update(el):  
    return 'http:/' if el == 'http:' else el

def page_number(page):
    if page is not None:
        current = page.text.replace("\n", "").split(" ")
        current = list(filter(lambda c: c != "", current))
        current.pop(0)
    return current[0]

def get_image_url(base_url, el, soup):
    images = soup.select(el) 
    return  base_url + images[0]['src'] 