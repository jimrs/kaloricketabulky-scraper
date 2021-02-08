import requests
import re
import unicodedata

def getPages(start=1, limit=20026):
    # posledni validni je page=20025
    url = 'https://www.kaloricketabulky.cz/tabulka-potravin'
    for i in range(start, limit):
        data = requests.get(url + '?page=' + str(i))
        print(data.url)

        with open('raw/tab' + str(i), 'w') as f:
            f.write(data.text)

def parseNames(raw):
    with open(raw, 'r') as f:
        data = f.read()
        names = re.findall('(?<=reload>).+?(?=</a>)', data)
        names = names[0:10]
        print(names)

def parseNumbers(raw):
    with open(raw, 'r') as f:
        data = f.read()
        numbers = re.findall('(?<=td md-cell hide-xs>)\s\d*?\s?,?\d*?(?=\s?</td>)', data)

        numbers_norm = []
        for item in numbers:
            item = item.strip()
            item_norm = item.replace(u'\xa0', u' ')
            numbers_norm.append(item_norm)

        print(numbers_norm)
        # can be used for testing, must always equal 50
        print(len(numbers_norm))

if __name__ == '__main__':
    # getPages(2164, 10001)
    parseNames('raw/tab1')
    parseNumbers('raw/tab1')