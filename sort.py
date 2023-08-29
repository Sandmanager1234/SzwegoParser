import os
import re
import json

D = {}
#Nike regex r'\b[A-Z\d]{6}[-| ]\d{3}\b'
#adidas v1 \b[A-Z\d]{9}[-| ][A-Z\d]{3}\b
#adidas v2 \b[A-Z]{1}\d{5}\b
#adidas v3 \b[A-Z]{2}\d{4}\b
# NB v1 \b[A-Z]{8}\b ! warning
#NB v2 \b[A-Z]{7}\d\b
#NB v3 \b[A-Z]{4}\d[A-Z]{2}\d\b
#NB v4 \b[A-Z]{3}\d{2,3}[A-Z]{2}[A-Z\d]{0,1}\b
#NB v5 \b[A-Z]{2}\d{4}[A-Z][A-Z\d]\b
#NB v6 \b[A-Zl]{2}\d{3,4}[A-Z][A-Z\d]*\b
#NB v7 \b[A-Z]{2}\d[A-Z]{3}[A-Z\d]{0,2}\b
#NB v8 \b[A-Z]\d{3,4}[A-Z][A-Z\d]{1,3}\b
#NB v9 \b\d{2}-\d{2}-\d{4}-\d{3}\b
#NB v10 \b[A-Z]{2}-[A-Z\d]{4}-\d{3}\b

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
                    return re.sub(r'[- ]+', '-', list(articles)[0]), 1
                else:
                    return articles, 1
            else:
                return re.sub(r'[- ]+', '-', re.findall(pattern, title)[0]), 1
    if title.find('货号') != -1:
        after = re.split(r'货号 *\W*', title)[1]
        clear = re.split(r'[^a-zA-Z\d\(\)\- ]+', after)
        i = 0
        for clear_t in clear:
            if clear_t.strip() != '':
                article = re.sub(r'[SIZEsize]+', '', clear_t.strip())
                return re.sub(r'[- ]+', '-', article), 0
    return article, -1

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


def spliter(title: str):
    t_title = title.strip()
    rows = t_title.split('\n')
    if t_title != '':
        if is_article(title) == True:
            try:
                D[len(rows)] += 1
            except:
                D[len(rows)] = 1
            save_file(f'txts\\{len(rows)}.txt', t_title)
        else:
            save_file(f'txts\\none_{len(rows)}.txt', t_title)


def read_json(path):
    with open(path, 'r', encoding='utf8') as file:
        data = json.load(file)
    return data


def save_file(path, data):
    with open(path, 'a', encoding='utf8') as file:
        file.write(f'{data}\n')


def main():
    files = os.listdir('jsons')
    for i, file in enumerate(files):
        print(f'{i+1}/{len(files)}')
        data = read_json(f'jsons\\{file}')
        for item in data['result']['items']:
            title = item['title']
            if title.find('💰') != -1:
                clear_title = clear_text(title)
                if clear_title.strip() != '':
                    # spliter(title)
                    if is_article(title) == True:
                        article, code = get_article(title)
                        url = item['goods_id'] #link
                        # print(article)
                        price = get_price(item)
                        save_file('preview.txt', f'art: {article}, price: {price} file: {file}, code: {code}, url: {url}')
    print(D)

if __name__ == '__main__':
    main()
