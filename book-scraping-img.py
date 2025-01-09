import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

books = []
img_sources = []

for page in range(1, 5):
    url = f'https://books.toscrape.com/catalogue/page-{page}.html'
    response = requests.get(url)

    content = response.content
    soup = BeautifulSoup(content, 'html.parser')

    ol = soup.find('ol')
    articles = ol.find_all('article', class_='product_pod')  # class_= is a css class

    for article in articles:
        image = article.find('img')
        title = image.attrs['alt']  # alt / how to access an attribute of a html tag
        src = image.attrs['src']
        # Save all image tags
        img_sources.append(src)

        p = article.find('p')
        class_attr = p.attrs['class']  # output: ['star-rating', 'Three']
        # class_attr = p.attrs['class'][1]  'Three'
        star = class_attr[1]

        str_price = article.find('p', attrs={'class': 'price_color'}).text
        price = float(str_price[1:])

        books.append([title, price, star])

# Create a folder to save images (if not already present)
if not os.path.exists('images'):
    os.makedirs('images')

url = 'http://books.toscrape.com/'
for img in img_sources:
    # To create the direct address
    img_url = urljoin(url, img)

    # Get the image's filename from the URL
    # ex: http://books.toscrape.com/media/cache/27/a5/27a53d0bb95bdd88288eaf66c9230d7e.jpg
    img_name = os.path.join('images', img_url.split('/')[-1])

    # Send a GET request to fetch the image
    img_response = requests.get(img_url)

    # Save the image to the local directory
    with open(img_name, 'wb') as f:
        f.write(img_response.content)

df = pd.DataFrame(books, columns=['Title', 'Price', 'Star Rating'])
df.to_csv('Books-Data.csv')
