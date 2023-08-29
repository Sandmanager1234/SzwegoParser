#!/usr/bin/python3.9
import re
import os
import pandas as pd


def get_items(data): # Ищет нужные нам товары по условию: есть смайлик moneybag, есть артикул и картинок больше 2, там либо 9 либо 1 у повторов
    itemlist = []
    # print(len(data['result']['items']))
    for i, item in enumerate(data['result']['items']):
        title = item['title']
        if title.find('💰') != -1:
            clear_title = clear_text(title)
            if clear_title.strip() != '':
                if is_article(title) == True:
                    itemlist.append(data['result']['items'][i])
    return itemlist

    
def is_article(title):
    patterns = [
        r'\b[A-Z\d]{6}[- ]\d{3}\b',
        r'\b[A-Z\d]{9}[- ][A-Z\d]{3}\b',
        # r'\b[A-Z]{8}\b',
        r'\b\d{8}\b',
        r'\b\d{7}[ACac]\b',
        r'\b\d{6}[ACMamc]*\b',
        r'\b\d{1}[A-Z]{2}\d{3}\b',
        r'\b\d{1}[A-Z]{1}\d{3}\b',
        r'\b[A-Z]{7}\d\b',
        r'\b[A-Z]{4}\d[A-Z]{2}\d\b',
        r'\b[A-Z]{3}\d{2,3}[A-Z]{2}[A-Z\d]{0,1}\b',
        r'\b[A-Z]{3}\d{3}[A-Z]*\b',
        r'\b[A-Z]{2}\d{4}[A-Z][A-Z\d]\b',
        r'\b[A-Z]{2}\d{4,5}[CcMAma]*\b',
        r'\b[A-Zl]{2}\d{3,4}[A-Z][A-Z\d]*\b',
        r'\b[A-Z]{2}\d[A-Z]{3}[A-Z\d]{0,2}\b',
        r'\b[A-Z]{2}\d{4}\b',
        r'\b[A-Z]{1}\d{4,5}[ACacMm]*\b',
        r'\b[A-Z]{1}\d{5}\b',
        r'\b[A-Z]\d{3,4}[A-Z][A-Z\d]{1,3}\b',
        r'\b\d{2}-\d{2}-\d{4}-\d{3}\b',
        r'\b[A-Z]{2}-[A-Z\d]{4}-\d{3}\b'
    ]
    if title.find('货号') != -1:
        return True
    for pattern in patterns:
        if len(re.findall(pattern, title)) != 0:
            return True
    return False


def get_article(title):
    article = ''
    patterns = [
        r'\b[A-Z\d]{6}[- ]\d{3}\b',
        r'\b[A-Z\d]{9}[- ][A-Z\d]{3}\b',
        # r'\b[A-Z]{8}\b',
        r'\b\d{8}\b',
        r'\b\d{7}[ACac]\b',
        r'\b\d{6}[ACMamc]*\b',
        r'\b\d{1}[A-Z]{2}\d{3}\b',
        r'\b\d{1}[A-Z]{1}\d{3}\b',
        r'\b[A-Z]{7}\d\b',
        r'\b[A-Z]{4}\d[A-Z]{2}\d\b',
        r'\b[A-Z]{3}\d{2,3}[A-Z]{2}[A-Z\d]{0,1}\b',
        r'\b[A-Z]{3}\d{3}[A-Z]*\b',
        r'\b[A-Z]{2}\d{4}[A-Z][A-Z\d]\b',
        r'\b[A-Z]{2}\d{4,5}[CcMAma]*\b',
        r'\b[A-Zl]{2}\d{3,4}[A-Z][A-Z\d]*\b',
        r'\b[A-Z]{2}\d[A-Z]{3}[A-Z\d]{0,2}\b',
        r'\b[A-Z]{2}\d{4}\b',
        r'\b[A-Z]{1}\d{4,5}[ACacMm]*\b',
        r'\b[A-Z]{1}\d{5}\b',
        r'\b[A-Z]\d{3,4}[A-Z][A-Z\d]{1,3}\b',
        r'\b\d{2}-\d{2}-\d{4}-\d{3}\b',
        r'\b[A-Z]{2}-[A-Z\d]{4}-\d{3}\b'
    ]
    for pattern in patterns:
        if len(re.findall(pattern, title)) != 0:
            if len(re.findall(pattern, title)) > 1:
                articles = set(re.findall(pattern, title))
                if len(articles) == 1:
                    return re.sub(r'[- ]+', '-', list(articles)[0])
                else:
                    return articles
            else:
                return re.sub(r'[- ]+', '-', re.findall(pattern, title)[0])
    if title.find('货号') != -1:
        after = re.split(r'货号 *\W*', title)[1]
        clear = re.split(r'[^a-zA-Z\d\(\)\- ]+', after)
        i = 0
        for clear_t in clear:
            if clear_t.strip() != '':
                article = re.sub(r'[SIZEsize]+', '', clear_t.strip())
                return re.sub(r'[- ]+', '-', article)
    return article


def get_price(item: dict):
    try:
        if item['itemNamePrice'] != 0:
            price = item['itemNamePrice']
        else:
            price = int(re.findall('💰\s*\d+', item['title'])[0][1:].strip())
    except:
        try: 
            price = int(re.findall('💰\s*\d+', item['title'])[0][1:].strip())
        except:
            price = -1
    return price


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

def a2_main(data, counter):
    i = counter
    count = i // 100
    if os.path.exists(f'tables/articles-{count + 1}.csv') == False:
        df = pd.DataFrame(columns=['Артикул', 'Цена', 'Ссылка'])
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
            url = 'https://a201908281438457360129101.szwego.com' + item['link']
            article = get_article(item['title'])
            if article == '':
                continue
            price = get_price(item)
            arr.append((article, price, url))
    df2 = pd.DataFrame(arr, columns=['Артикул', 'Цена', 'Ссылка'])
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