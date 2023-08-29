#!/usr/bin/python3.9
import re
from classes.table import Table
from classes.itemlist import ItemList
from classes.item_watches import ItemWatches

id = 'watches'

def clear_text(title: str):
    syms = []
    for sym in title:
        if sym.isascii() == True:
            syms.append(sym)
        else:
            syms.append(' ')
    cleartitle = ''.join(syms)
    words = re.findall(r'\S+', cleartitle)
    res = []
    for word in words:
        lenght = len(re.findall(r'\W+', word))
        if lenght == 0 or len(re.findall(r'\W+', word)[0]) != len(word):
            res.append(word)
    return ' '.join(res).strip()


def is_price(item):
    title = item['title'].strip()
    arr = title.split('\n')
    pricestr = arr[0]

    if pricestr.find('💰') != -1:
        return True
    elif re.search(r'([pP🏅️]?\s?)?\d+[.,。，\n]?', pricestr) is not None:
        if re.search(r'([pP🏅️]?\s?)?\d+[.,。，\n]?', pricestr).span()[0] in [0, 1, 2]:
            return True
    else:    
        return False


def diff_price(title):
    res = 1000
    price_str = title.split('\n')[0]
    allprices = re.findall(r'[+➕]?\s?\d+', price_str)
    
    if len(allprices) > 1:
        fprice = allprices[0]
        sprice = allprices[1]
        if len(re.findall(r'20[12][0-9]', sprice)) != 0:
            return 2000
        if len(fprice) != len(sprice):
            return 1001
        findex = title.find(fprice)
        if fprice == sprice or fprice.find(sprice) != -1:
            return 1002
        sindex = title.find(sprice)
        res = sindex-findex-len(fprice)

    return res


def get_items(data):
    items = []
    for item in data['result']['items']:
        title = item['title']
        price = is_price(item)
        diff = diff_price(title)
        if 'tags' in item:
            if item['mark_code'] != '':
                if len(item['imgsSrc']) > 2:
                    if len(re.findall(r'[^\s0-9cmkLZPG_.:~\+\-\*\/\[#!]+', clear_text(title))) != 0:
                        if price == True:
                            if diff > 7 and diff != 0:
                                items.append(item)
    return items


def get_final_items(itemlist):
    imgs = dict()
    newlist = []
    val = []
    for it in itemlist:
        item = ItemWatches(it, id)
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


def get_description(text): 
        rustr = text.split('\n')
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
    

def new_product(item: ItemWatches, translation: str, table: Table):

    dic = dict()

    for i in range(1, 12):
        if i < len(item.imgs)+1:
            dic[f'Изображение товаров {i}'] = f'{item.imgs[i-1]}'
        else:
            dic[f'Изображение товаров {i}'] = ''

    data = {
        'Тип строки': 'product',
        'Наименование': f'{item.name}',
        'Наименование артикула': f'{item.item["mark_code"]}',
        'Код артикула': f'{item.article}',
        'Валюта': 'CNY',
        'Доступен для заказа': '1',
        'Видимость на витрине': '1',
        'Зачеркнутая цена': '0',
        'Закупочная цена': f'{item.price}',
        'Описание': f'{get_description(translation)}',
        'В наличии @Наличие в Москве': '0',
        'Статус': '1',
        'Выбор вариантов товара': '2',
        'Тип товаров': 'Часы',
        'Ссылка на витрину': f'{item.article}',
        'Бренд': f'{item.brand}',
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


def w_main(data, counter):

    table = Table((counter//100)+1, id)

    if counter == 1:
        table.create_table()
        table.new_category('Часы', 'watches')

    i = counter

    if i // 100 > 0 and i == i//100 * 100:
        count = i // 100
        table.num = count + 1
        table.create_table()
        table.new_category('Часы', 'watches')

    itemlist = get_items(data)
    if len(itemlist) != 0:
        final_itemlist = get_final_items(itemlist)
        items = ItemList(final_itemlist)
        for j in range(len(items.il)):
            it = ItemWatches(items.il[j], id)
            if it.name != '':
                if re.sub(r'\d', '', it.name) != '':
                    if re.sub(r'[ZPG]', '', it.name) != '':
                        if re.sub(r'[\sF0-9cCnN]', '', it.name) != '':
                            if re.sub(r'(\)/361)|(9100 CNC)|(\/\/\/316 P)', '', it.name) != '':
                                if re.sub(r'[\dm]+', '', it.name) != '':
                                    new_product(it, items.tr[j], table)
    # print(i)
    

def main():
    pass


if __name__ == '__main__':
    main()