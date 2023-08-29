#!/usr/bin/python3.9
import re
import json
from classes.table import Table
from classes.itemlist import ItemList
from classes.item_bags import ItemBags


CURR_SUBCATEGORY = ''
id = 'bags'

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



def get_items(data):
    items = []
    for item in data['result']['items']:
        title = item['title']
        if 'tags' in item:
            if title.find('💰') != -1:
                if len(item['imgsSrc']) > 2:
                    if len(re.findall(r'[^\scCm0-9:,.-]+', clear_text(title.split(":")[0]))) != 0:
                        if len(re.findall(r'([pP💰]\s?\d+)+', title)) < 2:
                            items.append(item)
    return items


def get_final_items(itemlist):
    imgs = dict()
    newlist = []
    val = []
    for it in itemlist:
        item = ItemBags(it, id)
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


def get_path_sub(subcat: str):
    with open('bc/path_clothes.json', 'r', encoding='utf8') as file:
        paths = json.load(file)
    result = 'None'
    for _sub in paths:
        if subcat == _sub:
            result = paths[f'{_sub}']
    return result
    

def new_product(item: ItemBags, translation: str, table: Table):
    global CURR_SUBCATEGORY

    sub_category = item.sub_category

    dic = dict()

    for i in range(1, 12):
        if i < len(item.imgs)+1:
            dic[f'Изображение товаров {i}'] = f'{item.imgs[i-1]}'
        else:
            dic[f'Изображение товаров {i}'] = ''

    if sub_category != CURR_SUBCATEGORY:
        CURR_SUBCATEGORY = sub_category
        table.new_subcategory(sub_category, get_path_sub(sub_category))

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
        'Тип товаров': f'Аксессуары',
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


def b_main(data, counter):
    
    global CURR_SUBCATEGORY

    table = Table((counter//100)+1, id)

    if counter == 1:
        table.create_table()
        table.new_category('Аксессуары', 'accessories')
    
    i = counter
    if i // 100 > 0 and i == i//100 * 100:
        count = i // 100
        table.num = count + 1
        CURR_SUBCATEGORY = ''
        table.create_table()
        table.new_category('Аксессуары', 'accessories')

    itemlist = get_items(data)
    if len(itemlist) != 0:
        final_itemlist = get_final_items(itemlist)
        items = ItemList(final_itemlist)

        for j in range(len(items.il)):
            item = ItemBags(items.il[j], id)
            new_product(item, items.tr[j], table)
    # print(i)


def main():
    pass


if __name__ == '__main__':
    main()