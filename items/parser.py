import requests
from bs4 import BeautifulSoup
import sqlite3

# <div class="market_listing_table_message">Ошибка поиска. Повторите попытку позднее.</div>
# <div class="market_listing_table_message"> Произошла ошибка при получении лотов для этого предмета. Пожалуйста, повторите попытку позже. </div>
main_link = 'https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_Tournament%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Type%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Exterior%5B%5D=tag_WearCategory0&appid=730#p1_popular_desc'
# main_link = 'https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_Tournament%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Type%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Exterior%5B%5D=tag_WearCategory0&appid=730#p2_popular_desc'

con = sqlite3.connect('db.sqlite3')
cur = con.cursor()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

full_page = requests.get(main_link, headers=headers)

soup = BeautifulSoup(full_page.content, 'html.parser')

convert = soup.findAll('a', {'class': "market_listing_row_link"})

s = ''.find(' 1x, ')
for id, i in enumerate(convert):
    name = i.findAll('span', {'id': f'result_{id}_name'})[0].text
    price = i.findAll('span', {'class': 'normal_price'})[1].text
    img_link = i.findAll('img', {'id': f'result_{id}_image'})[0].get('srcset')[i.findAll('img', {'id': f'result_{id}_image'})[0].get('srcset').find(' 1x, ') + 5:-3]
    color = i.findAll('span', {'id': f'result_{id}_name'})[0].get('style')[7:-1]
    img = requests.get(img_link, headers=headers).content
    print(img)
    print(color)
    print(img_link)
    print(f'{name}: {price}')
    # print(i)
    cur.execute('INSERT INTO items (id, name, img, price, color_name)'
                'VALUES (?, ?, ?, ?, ?)',
                (id + 1, name, img, price, color))

con.commit()
con.close()

# print(convert)