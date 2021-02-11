import requests
import re
import unicodedata
import csv

def getPages(start=1, limit=20026):
    # posledni validni je page=20025
    url = 'https://www.kaloricketabulky.cz/tabulka-potravin'
    for i in range(start, limit):
        data = requests.get(url + '?page=' + str(i))
        print(data.url)

        with open('raw/tab' + str(i), 'w') as f:
            f.write(data.text)

def parseData(raw):
    with open(raw, 'r') as f:
        data = f.read()
        names = _parseNames(data)
        numbers = _parseNumbers(data)

    # TODO cyklus pro projeti vsech souboru ve slozce raw
    # TODO do promenne table pridavat dalsi a dalsi hodnoty
    # TODO nasledne zapsat
    table = _createTable(names, numbers)
    _writeTable(table)


def _writeTable(table):
    with open('out/test.csv', 'w', newline='') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_ALL)
        header = ['Název', 'Energetická hodnota (kcal)', 'Bílkoviny (g)', 'Sacharidy (g)', 'Tuky (g)', 'Vláknina (g)']
        wr.writerow(header)
        wr.writerows(table)


def _createTable(names, numbers):
    table = []
    for index, item in enumerate(names):
        row = [item]
        for i in range (index * 5, (index * 5) + 5):
            row.append(numbers[i])
        table.append(row)

    # print(table)
    # len must always be 10
    # print(len(table))
    return table


def _parseNames(raw_data):
    names = re.findall('(?<=reload>).+?(?=</a>)', raw_data)
    names = names[0:10]
    #print(names)
    return names


def _parseNumbers(raw_data):
    numbers = re.findall('(?<=td md-cell hide-xs>)\s\d*?\s?,?\d*?(?=\s?</td>)', raw_data)

    numbers_norm = []
    for item in numbers:
        item = item.strip()
        item_norm = item.replace(u'\xa0', u' ')
        numbers_norm.append(item_norm)

    #print(numbers_norm)
    # can be used for testing, must always equal 50
    #print(len(numbers_norm))
    return numbers_norm


if __name__ == '__main__':
    # getPages(2164, 10001)
    parseData('raw/tab1')

    #TODO json