import re

import json
from datetime import datetime



class ItemWatches:
    def __init__(self):
        self.id = ''
        self.name = ''
        self.price = ''
        self.article = ''
        self.brand = ''
        self.imgs = []
        self.date = ''
        self.item = {}


    def __init__(self, item: dict, id: str):
        self.item = item
        self.id = id
        self.name = self.__get_name()
        self.price = self.__get_price()
        self.article = self.__get_article()
        self.brand = self.__get_brand()
        self.imgs = self.__get_imgs().copy()
        self.date = self.__get_date()
        
    

    # Доработать
    def __get_name(self):
        name = ''
        name_str = self.get_description()
        if len(re.findall(r'[pP💰]?\s?\d+', name_str)) != 0:
            name = name_str.replace(re.findall(r'\d+', name_str)[0], '', 1)
        return self.__clear_text(name).strip()


    # Доработать
    def __get_price(self):
        price = ''
        price_str = self.get_description()
        if 'priceArr' in self.item:
            price = str(self.item['priceArr'][0]['value'])[:-2]
        elif len(re.findall(r'[Pp💰]?\s?\d+', price_str)) != 0:
            price = re.findall(r'[Pp💰]?\s?\d+', price_str)[0]
        else:
            price = 'none000'
        return re.findall('\d+', price)[0]



    def __get_article(self):
        code = self.item['mark_code']
        article = f'3-{code}-w'
        return article


    def __get_brand(self):
        resarr = []
        strarr = []
        res = 'Nan'
        with open(f'bc/brands_{self.id}.json', 'r', encoding='utf8') as file:
            brands = json.load(file)

        if 'tags' in self.item:
            tags = self.item['tags']

            if len(tags) == 0:
                words = re.findall(r'[a-zA-Z]+', self.__clear_text(self.item['title']))
                for i in range(2):
                    resarr.append(words[i])
                print('не нашёл www.szwego.com' + self.item['link'])
                return ' '.join(resarr)

            
            for tag in tags:
                for brand in brands:
                    for it in brands[f'{brand}']:
                        if tag['tagName'] == it:
                            res = brand
                            return res

        words = re.findall(r'[a-zA-Z]+', self.__clear_text(self.item['title']))
        if len(words) < 2:
            for i in range(len(words)):
                strarr.append(words[i])
        else:
            for i in range(2):
                strarr.append(words[i])

        str = ' '.join(strarr)
        for brand in brands:
            if str.lower().find(brand.lower()) != -1:
                res = brand
                return res
        res = str
        return res


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

    
    def __clear_text(self, title: str):
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


    def get_description(self):
        title = self.item['title']
        desc = ''
        if len(title.strip().split('\n')) > 14:
            if title.find('👉') != -1:
                desc = title.split('👉')[1].replace('。', '.', 1).split('。')[0]
        if desc != '':
            pass
        elif re.search('配置参数', title) is not None:
            desc = re.split('配置参数', title)[0]
        elif re.search('主要功能', title) is not None:
            desc = re.split('主要功能', title)[0]
        elif re.search('「羁绊」', title) is not None:
            desc = re.split('「羁绊」', title)[0]
        elif re.search('尺寸', title) is not None:
            desc = re.split('尺寸', title)[0]
        elif re.search('材料', title) is not None:
            desc = re.split('材料', title)[0]
        # elif re.search('。', title) is not None:
        #     desc = re.split('。', title)[0]
        else:
            desc = title
        return desc
