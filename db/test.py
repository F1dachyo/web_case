import requests
from bs4 import BeautifulSoup
import sqlite3

con = sqlite3.connect('database.sqlite')
cur = con.cursor()

img1 = requests.get('https://images.steamcdn.io/csgonet/cases/covert_2.png', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}).content
img2 = requests.get('https://images.steamcdn.io/csgonet/cases/sand-mining.png', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}).content
img3 = requests.get('https://images.steamcdn.io/csgonet/cases/water-mining.png', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}).content
img4 = requests.get('https://images.steamcdn.io/csgonet/cases/M4A1s-Case-Mycsgo.png', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}).content
img5 = requests.get('https://images.steamcdn.io/csgonet/cases/new_aug.png', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}).content

cur.execute('INSERT INTO cases (id, name, price, image_bytes, skins_ids)'
            'VALUES (?, ?, ?, ?, ?)',
            (1, 'Случайный AK-47', 0, img1, ', '.join(map(str, range(1, 38)))))

cur.execute('INSERT INTO cases (id, name, price, image_bytes, skins_ids)'
            'VALUES (?, ?, ?, ?, ?)',
            (2, 'Случайный AWP', 0, img2, ', '.join(map(str, range(38, 65)))))

cur.execute('INSERT INTO cases (id, name, price, image_bytes, skins_ids)'
            'VALUES (?, ?, ?, ?, ?)',
            (3, 'Случайный M4A4', 0, img3, ', '.join(map(str, range(65, 91)))))

cur.execute('INSERT INTO cases (id, name, price, image_bytes, skins_ids)'
            'VALUES (?, ?, ?, ?, ?)',
            (4, 'Случайный M4A1-S', 0, img4, ', '.join(map(str, range(91, 118)))))

cur.execute('INSERT INTO cases (id, name, price, image_bytes, skins_ids)'
            'VALUES (?, ?, ?, ?, ?)',
            (5, 'Случайный AUG', 0, img5, ', '.join(map(str, range(118, 146)))))

con.commit()
con.close()