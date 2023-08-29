#!/usr/bin/python3.9
import re
import json
from classes.table import Table
from classes.itemlist import ItemList
from classes.item_sneakers import ItemSneakers

ID = 'sneakers'



def get_items(data): # Ищет нужные нам товары по условию: есть смайлик moneybag, есть артикул и картинок больше 2, там либо 9 либо 1 у повторов
    itemlist = []
    # print(len(data['result']['items']))
    for i in range(len(data['result']['items'])):
        if data['result']['items'][i]['title'].find("💰") != -1:
            if data['result']['items'][i]['title'].split('\n')[-1].find('#') != -1:
                if len(data['result']['items'][i]['imgsSrc']) > 2:
                    if len(data['result']['items'][i]['title'].split('\n')) > 3:
                        if len(re.findall('\D', clear_text(data['result']['items'][i]['title'].split('\n')[1]))) > 0:
                            itemlist.append(data['result']['items'][i])
    return itemlist


def clear_text(title):
    syms = []
    for sym in title:
        if sym < '⵿':
            syms.append(sym)
        else:
            syms.append(' ')
    cleartitle = ''.join(syms)
    words = re.findall('\S+', cleartitle)
    res = []
    # words = re.findall(r'\w+', title)
    for word in words:
        lenght = len(re.findall('\W+', word))
        if lenght == 0 or len(re.findall('\W+', word)[0]) != len(word):
            res.append(word)
    
    return ' '.join(res).strip()


def check_articles(art):
    dic = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    with open('bc/s_arts.json', 'r', encoding='utf8') as file:
        articles_dict = json.load(file)
    if art not in articles_dict:
        articles_dict[f'{art}'] = 0
        newart = art
    else:
        if articles_dict[f'{art}'] // 26 == 0: 
            i = articles_dict[f'{art}']
            articles_dict[f'{art}'] += 1
            newart = art + f'-{dic[i]}'
        else: 
            i = articles_dict[f'{art}'] // 26
            k = articles_dict[f'{art}'] % 26
            articles_dict[f'{art}'] += 1
            newart = art + f'-{dic[k]}{i}'
    with open('bc/s_arts.json', 'w', encoding='utf8') as file:
        json.dump(articles_dict, file, indent=4, ensure_ascii=False)

    return newart


def get_final_items(itemlist):
    imgs = dict()
    newlist = []
    val = []
    for it in itemlist:
        item = ItemSneakers(it)
        img = item.imgs
        price = item.price
        if img[0] not in imgs:
            val.append(price)
            imgs[f'{img[0]}'] = val.copy()
            newlist.append(it)
        elif price not in imgs[f'{img[0]}']:
            val.append(price)
            imgs[f'{img[0]}'] = val.copy()
            newlist.append(it)
        val.clear()
    return newlist


def new_product(item: ItemSneakers, translation: str, table: Table):

    sizes = item.sizelist
    article = check_articles(item.article)
    dic = dict()

    for i in range(1, 12):
        if i < len(item.imgs)+1:
            dic[f'Изображение товаров {i}'] = f'{item.imgs[i-1]}'
        else:
            dic[f'Изображение товаров {i}'] = ''

    data = {
        'Тип строки': 'product',
        'Наименование': f'{item.name} {article}',
        'Валюта': 'CNY',
        'Описание': f'{get_description(translation)}',
        'Статус': '1',
        'Выбор вариантов товара': '2',
        'Тип товаров': 'Обувь',
        'Ссылка на витрину': f'{article}',
        'Бренд': f'{item.brand}',
        'Размер EU': '<{}>',
        'Пол': 'Унисекс',
        'Изображения товаров 1': f'{dic.get("Изображение товаров 1")}',
        'Изображения товаров 2': f'{dic.get("Изображение товаров 2")}',
        'Изображения товаров 3': f'{dic.get("Изображение товаров 3")}',
        'Изображения товаров 4': f'{dic.get("Изображение товаров 4")}',
        'Изображения товаров 5': f'{dic.get("Изображение товаров 5")}',
        'Изображения товаров 6': f'{dic.get("Изображение товаров 6")}',
        'Изображения товаров 7': f'{dic.get("Изображение товаров 7")}',
        'Изображения товаров 8': f'{dic.get("Изображение товаров 8")}',
        'Изображения товаров 9': f'{dic.get("Изображение товаров 9")}',
        'Изображения товаров 10': f'{dic.get("Изображение товаров 10")}',
        'Изображения товаров 11': f'{dic.get("Изображение товаров 11")}',
        'Дата': f'{item.date}'
    }
    table.new_row(data)
    for size in sizes:
        new_variant(item, size, article, table)
    

def new_variant(item: ItemSneakers, size: str, article:str, table: Table):

    data = {
        'Тип строки': 'variant',
        'Наименование': f'{item.name} {article}',
        'Наименование артикула': f'{size}',
        'Код артикула': f'{article}-{size}',
        'Валюта': 'CNY',
        'Доступен для заказа': '1',
        'Видимость на витрине': '1',
        'Зачеркнутая цена': '0',
        'Закупочная цена': f'{item.price}',
        'В наличии @Наличие в Москве': '0',
        'Статус': '1',
        'Выбор вариантов товара': '2',
        'Тип товаров': 'Обувь',
        'Ссылка на витрину': f'{article}',
        'Размер EU': '<{'+str(size)+'}>'
    }
    table.new_row(data)


def get_description(trans):
    rustr = trans.split('.')
    findesc = []
    if len(rustr) > 1:
        findesc.append('<p>')
        for str in rustr:
            findesc.append('<span>')
            findesc.append(str)
            findesc.append('</span>')
        findesc.append('</p>')
    else:
        findesc.append('<p>')
        findesc.append('<span>')
        findesc.append(rustr[0])
        findesc.append('</span>')
        findesc.append('</p>')
    return ''.join(findesc)

    
def s_main(data, counter):

    table = Table((counter//100)+1, ID)

    if counter == 1:
        table.create_table()
        table.new_category('Обувь', 'shoes')
        table.new_subcategory('Кроссовки', 'sneakers')

    i = counter
    if i // 100 > 0 and i == i//100 * 100:
        count = i // 100
        table.num = count + 1
        table.create_table()
        table.new_category('Обувь', 'shoes')
        table.new_subcategory('Кроссовки', 'sneakers')

    itemlist = get_items(data)
    if len(itemlist) != 0:
        final_itemlist = get_final_items(itemlist)
        items = ItemList(final_itemlist)

        for j in range(len(items.il)):
            item = ItemSneakers(items.il[j])
            new_product(item, items.tr[j], table)
    # print(i)


def main():
    pass


if __name__ == '__main__':
    main()