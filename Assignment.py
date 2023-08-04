import pip._vendor.requests as requests
from bs4 import BeautifulSoup
import pandas as pd
import gzip
from time import sleep
from urllib.request import urlopen, Request


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
        "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.google.com/",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
}
product_to_search=input("Enter the product to search: ")
search_query = product_to_search.replace(' ', '+')
base_url = 'https://www.amazon.in/s?k={0}'.format(search_query)
count=0
items = []
for i in range(1, 100):
    print('Processing {0}...'.format(base_url + '&page={0}'.format(i)))
    req = Request(base_url + '&page={0}'.format(i), headers=headers)
    response = urlopen(req)
    charset = response.headers.get_content_charset()
    if response.headers.get('Content-Encoding') == 'gzip':
        content = gzip.decompress(response.read()).decode(charset)
    else:
        content = response.read().decode(charset)
    soup = BeautifulSoup(content, 'html.parser')
    results = soup.find_all('div', {'class': 's-result-item', 'data-component-type': 's-search-result'})

    for result in results:
        product_name = result.h2.text

        try:
            rating = result.find('i', {'class': 'a-icon'}).text
            rating_count = result.find_all('span', {'aria-label': True})
            if len(rating_count) >= 2:
               rating_count = rating_count[1].text
            else:
               rating_count = 'N/A' 
        except AttributeError:
            continue

        try:
            price1 = result.find('span', {'class': 'a-price-whole'}).text
            # description = result.find('span', {'class': 'a-size-base-plus a-color-base a-text-normal'}).text
            product_url = 'https://amazon.in' + result.h2.a['href']

            # New code to scrape product description
            req_product = Request(product_url, headers=headers)
            response_product = urlopen(req_product)
            charset_product = response_product.headers.get_content_charset()
            if response_product.headers.get('Content-Encoding') == 'gzip':
               content_product = gzip.decompress(response_product.read()).decode(charset_product)
            else:
               content_product = response_product.read().decode(charset)
            soup_product = BeautifulSoup(content_product, 'html.parser')
            
            try:
                description_element = soup_product.find('div', {'id': 'productDescription'}).find('p').find('span')
                
                description = description_element.text.strip()

             
            except AttributeError:
                description = 'No description available'
            
            # print(rating_count, product_url)
            count+=1
            items.append([product_name, rating, rating_count, price1, description])
        except AttributeError:
            continue
    if(count+1>2000):
        break
    sleep(1.5)

df = pd.DataFrame(items, columns=['product', 'rating', 'rating count', 'price(inr)', 'description'])
df.to_csv('{0}.csv'.format(search_query), index=False)
    