import re
import json
from datetime import datetime

class ItemSneakers:
    def __init__(self, item):
        self.item = item
        self.name = self.__get_brand()[0]
        self.price = self.__get_price()
        self.article = self.__get_article()
        self.sizelist = self.__get_size_list()
        self.brand = self.__get_brand()[1]
        self.imgs = self.__get_imgs().copy()
        self.date = self.__get_date()
    

    def __get_name(self):
        title = self.item['title']
        try:
            part = title.split('\n')
        except:
            print(*title.split('\n'))
        name = ''
        if len(part) > 4:
            for i in range(1, len(part)-2):
                name += part[i]
        else:
            name = part[1]
        txt = self.__clear_text(name)
        return txt


    def __get_article(self):

        artstr = self.item['title'].split('\n')[-1]

        syms = []
        for sym in artstr:
            if sym < '⵿':
                syms.append(sym)
            else:
                syms.append(' ')
        clearstr = ''.join(syms).strip()
        
        art = clearstr.split('#')

        lenght = len(re.findall('\S+', art[0]))
        if lenght == 0:
            article = art[1].strip()
        else:
            if art[0].find(':') != -1 or art[0].find(';') != -1:
                article = art[0].replace(':', '').replace(';', '').strip()
            else:
                article = art[0].strip()
        tart = '-'.join(article.split())
        return tart


    def __get_price(self):
        title = self.item['title']
        part = title.split('\n')
        price = re.findall('\d+', part[0])[0]
        return price
    

    def __get_size_list(self):
        sizestr = self.item['title'].split('\n')[-2]
        syms = []

        for sym in sizestr:
            if sym < '⵿':
                syms.append(sym)
            else:
                syms.append(' ')

        clearsizelist = ''.join(syms)

        if clearsizelist.find(':') != -1 or clearsizelist.find(';') != -1:
            sizes = clearsizelist.replace(';','').replace(':', '')
        else:
            sizes = clearsizelist
        sizelist = sizes.split()
        
        newsl = []
        for size in sizelist:
            if size.find('.') == -1 and len(size) > 2:
                patt = size[2:]
                newsl.append(size.replace(patt, '.5'))
            else:
                newsl.append(size)

        return newsl


    def __clear_text(self, title):
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


    def __get_brand(self):
        title = self.__get_name()
        arr = []
        with open('bc/brands_sneakers.json', 'r', encoding='utf8') as file:
            brands = json.load(file)
        for brand in brands:
            for i in range(len(brands[f'{brand}'])):
                for j in range(len(brands[f'{brand}'][i])):
                    sub = brands[f'{brand}'][i][j]
                    if len(re.findall(sub, title.lower())) > 0:
                        if brand == 'MSCHF':
                            title = ' '.join(re.findall('\w+', title))
                        if i == 0 and j > 0:
                            arr.append(re.sub(brands[f"{brand}"][i][j], brand+' ', title, 1))
                            arr.append(f'{brand}')
                        elif i == 0 and j == 0:
                            arr.append(f'{title}')
                            arr.append(f'{brand}')
                        elif i == 1:
                            sec = re.findall(sub, title)[0]
                            arr.append(re.sub(f"{sub}", f"{brand} {sec}", title, 1))
                            arr.append(f'{brand}')
                        return arr
        return [f'{title}', 'Другое']


    def __get_imgs(self):
        srcimgs = self.item['imgsSrc']
        return srcimgs


    def __get_date(self):
        _time = self.item['time']

        if _time.find('Hour') != -1:
            date = datetime.today().strftime("%Y/%m/%d")
        elif len(_time.split('/')) == 3:
            date = _time
        else:
            date = f'{datetime.today().year}/{_time}'

        return date