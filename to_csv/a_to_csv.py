#!/usr/bin/python3.9
import re
import os
import pandas as pd


def get_items(data): # Ищет нужные нам товары по условию: есть смайлик moneybag, есть артикул и картинок больше 2, там либо 9 либо 1 у повторов
    itemlist = []
    # print(len(data['result']['items']))
    for i in range(len(data['result']['items'])):
        if data['result']['items'][i]['title'].find("💰") != -1:
            if data['result']['items'][i]['title'].find('货号') != -1:
                itemlist.append(data['result']['items'][i])
    return itemlist

    
def get_price(item: dict):
    try:
        if item['itemNamePrice'] != 0:
            price = item['itemNamePrice']
        else:
            price = int(re.sub(r'\D+', ' ', item['title']).split()[0])
    except:
        price = int(re.sub(r'\D+', ' ', item['title']).split()[0])
    return price


def get_article(item: dict):
    title = item['title']
    after = re.split(r'货号 *:*', title)[1]
    clear = re.split(r'[^a-zA-Z\d\(\)\- ]+', after)
    article = ''
    i = 0
    length = len(clear)
    while article == '':
        article = clear[i].strip().replace(' ', '-')
        i += 1
        if i >= length:
            article = ''
            break
    if article == '':
        print(title)
        print(clear)
    return article

def a_main(data, counter):
    i = counter
    count = i // 100
    if os.path.exists(f'tables/articles-{count + 1}.csv') == False:
        df = pd.DataFrame(columns=['Артикул', 'Цена'])
    else:
        df = pd.read_csv(f'tables/articles-{count + 1}.csv', 
                        sep=';', 
                        encoding='cp1251', 
                        encoding_errors='ignore', 
                        lineterminator='\n'
                        )
    arr = []
    itemlist = get_items(data)
    if len(itemlist) != 0:
        for item in itemlist:
            article = get_article(item)
            if article == '':
                continue
            price = get_price(item)
            arr.append((article, price))
    df2 = pd.DataFrame(arr, columns=['Артикул', 'Цена'])
    new_df = pd.concat([df, df2], ignore_index=True)
    new_df.to_csv(
        f'tables/articles-{count + 1}.csv',
        sep=';',
        lineterminator='\n',
        encoding='cp1251',
        errors='ignore',
        index=False
    )          
    # print(i)


def main():
    pass


if __name__ == '__main__':
    main()