import requests
import re

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
        match = re.findall('(?<=reload>).+?(?=</a>)', data)
        match = match[0:10]
        print(match)
        print(len(match))

if __name__ == '__main__':
    # getPages(2164, 10001)
    parseNames('raw/tab1')