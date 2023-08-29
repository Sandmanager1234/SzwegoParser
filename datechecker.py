#!/usr/bin/python3.9
import datetime
import re


m30 = ['04', '06', '09', '10']


async def check_date(inp_date: str, msg):
    if inp_date == '0':
        return True
    if re.match(r'^\d{4}-\d{2}-\d{2}$', inp_date) is None:
        return False
    arr = inp_date.split('-')
    if int(arr[0]) >= 2002 and int(arr[0]) <= datetime.date.today().year:
        if int(arr[0]) == datetime.date.today().year:
            if int(arr[1]) > 0 and int(arr[1]) <= datetime.date.today().month:
                if int(arr[1]) == datetime.date.today().month:
                    if int(arr[2]) > 0 and int(arr[2]) <= datetime.date.today().day:
                        return True
                    else:
                        return False
                elif arr[1] == '02':
                    if int(arr[2]) > 0 and int(arr[2]) < 29:
                        return True
                    else:
                        return False
                elif arr[1] in m30:
                    if int(arr[2]) > 0 and int(arr[2]) < 31:
                        return True
                    else:
                        return False
                else:
                    if int(arr[2]) > 0 and int(arr[2]) < 32:
                        return True
                    else:
                        return False
            else:
                return False
        else:
            if int(arr[1]) > 0 and int(arr[1]) < 13:
                if arr[1] == '02':
                    if int(arr[2]) > 0 and int(arr[2]) < 29:
                        return True
                    else:
                        return False
                elif arr[1] in m30:
                    if int(arr[2]) > 0 and int(arr[2]) < 31:
                        return True
                    else:
                        return False
                else:
                    if int(arr[2]) > 0 and int(arr[2]) < 32:
                        return True
                    else:
                        return False
    else:
        await msg.answer('Вы написали бред.')
        return False


def main():
    print(check_date('2022-12-11'))

if __name__ == '__main__':
    main()
