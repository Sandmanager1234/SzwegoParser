import re
import json
import time
from random import randint
from googletrans import Translator
# from translate import Translator

TRANS = Translator()

class ItemList:

    def __init__(self, itemlist: list):
        self.il = itemlist.copy()
        self.tr = self.__tr_items(self.il).copy()
    

    def __tr_items(self, itemlist):
        res = []
        listarr = []
        listr = ''
        if self.__count_symbs(itemlist) > 2379:
            newitems = self.__slice_list(itemlist)
            for new in newitems:
                tr = self.__tr_items(new)
                res.extend(tr)
        else:
            for item in itemlist:
                text = self.__get_str_without_price(item['title'])
                
                listarr.append(text)
            listr = '\n|\n'.join(listarr)
            tr = TRANS.translate(listr, dest='ru', src='zh-CN')
            res.extend(tr.text.split('\n|\n'))
            time.sleep(randint(1,3))
        return res


    def __count_symbs(self, itemlist):
        titlelist = []
        name = ''
        for item in itemlist:
            name = item['title'].strip()
            titlelist.append(name)
        titlestr = '\n'.join(titlelist)
        return len(titlestr)


    def __slice_list(self, itemlist):
        lenght = len(itemlist)
        new1 = []
        new2 = []
        res = []
        for i in range(lenght//2):
            new1.append(itemlist[i])

        for i in range(lenght//2, lenght):
            new2.append(itemlist[i])
        res.append(new1)
        res.append(new2)
        return res


    def __get_str_without_price(self, text: str):
        desc = ''
        if len(re.findall(r'💰\s?\d+', text)) != 0:
            desc = re.sub(r'💰\s?\d+', '', text, 1)
        else:
            desc = text
        return desc.strip().replace('(专柜精仿货)', '')



    