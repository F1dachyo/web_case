import requests
from bs4 import BeautifulSoup
import sqlite3

main_link = 'https://wiki.swapskins.com/gloves'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

con = sqlite3.connect('db.sqlite3')
cur = con.cursor()
convert = []
full_page = requests.get(main_link, headers=headers)
soup = BeautifulSoup(full_page.content, 'html.parser')
convert = soup.findAll('a')[15:-14]
print(convert)
with open('id.txt', mode='r') as f:
    r = f.read()
with open('id.txt', mode='w') as f:
    f.write(str(int(r) + len(convert)))
for id, i in enumerate(convert, int(r)):
    n = i.findAll('div', {'class': 'item-name category-item-skin__name ellipsis'})[0].text
    name = i.findAll('div', {'class': 'item-skin-name category-item-skin__skin ellipsis'})[0].text[5:-3]
    name = f'{n} | {name}'
    t = i.findAll('div', {'class': 'item-type-name category-item-skin__type'})[0].text[3:-1]
    price = i.findAll('div', {'class': 'item-label category-item-skin__info-label'})[0].text[7:-5]
    if len(price) != 1:
        price = price[price.find('-') + 2:]
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
                (id, name, img, price, t, color))

con.commit()
con.close()
