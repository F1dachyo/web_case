import requests
from bs4 import BeautifulSoup
import sqlite3
import time

main_link = 'https://wiki.swapskins.com/weapons/ak-47'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

con = sqlite3.connect('db.sqlite3')
cur = con.cursor()
convert = []
full_page = requests.get(main_link, headers=headers)
soup = BeautifulSoup(full_page.content, 'html.parser')
convert = soup.findAll('a')[16:-14]
print(convert)
for id, i in enumerate(convert):
    name = i.findAll('div', {'class': 'item-skin-name category-item-skin__skin ellipsis'})[0].text[5:-3]
    t = i.findAll('div', {'class': 'item-type-name category-item-skin__type'})[0].text[3:-1]
    price = i.findAll('div', {'class': 'item-label category-item-skin__info-label'})[0].text[7:-5]
    img_link = i.findAll('img', {'class': 'item-image__img'})[0].get('src')
    color = i.findAll('div', {'class': 'item-skin-name category-item-skin__skin ellipsis'})[0].get('style')[6:-1]
    img = requests.get(img_link, headers=headers).content
    print(img)
    print(color)
    print(img_link)
    print(t)
    print(f'{name}: {price}')
    cur.execute('INSERT INTO items (id, name, img, price, type, color)'
                'VALUES (?, ?, ?, ?, ?, ?)',
                (id + 1, name, img, price, t, color))

con.commit()
con.close()

# print(convert)