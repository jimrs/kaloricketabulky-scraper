import requests
import re
import unicodedata
import csv
import os
import json

def getPages(start=1, limit=20026):
    # posledni validni je page=20025
    url = 'https://www.kaloricketabulky.cz/tabulka-potravin'
    for i in range(start, limit):
        data = requests.get(url + '?page=' + str(i))
        print(data.url)

        with open('raw/tab' + str(i), 'w') as f:
            f.write(data.text)

def parseData():
    i = 0
    table = []
    for raw in os.scandir('raw'):
        with open(raw, 'r') as f:
            data = f.read()
            names = _parseNames(data)
            numbers = _parseNumbers(data)

            table = _addToTable(names, numbers, table)

        if i % 1000 == 0:
            print(i)
        i = i + 1
    
    _writeTable(table)


def _writeTable(table):
    with open('out/db.csv', 'w', newline='') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_ALL)
        header = ['Název', 'Energetická hodnota (kcal)', 'Bílkoviny (g)', 'Sacharidy (g)', 'Tuky (g)', 'Vláknina (g)']
        wr.writerow(header)
        wr.writerows(table)


def _addToTable(names, numbers, table):
    for index, item in enumerate(names):
        row = [item]
        for i in range (index * 5, (index * 5) + 5):
            row.append(numbers[i])
        table.append(row)

    # print(table)
    # print(len(table))
    return table


def _parseNames(raw_data):
    names = re.findall('(?<=reload>).+?(?=</a>)', raw_data)
    names = names[0:10]
    #print(names)
    if len(names) != 10:
        print("Warning: len of names doesn't equal 10.")
        print(names)
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
    if len(numbers_norm) != 50:
        print("Warning: len of numbers doesn't equal 10.")
        print(numbers_norm)
    return numbers_norm


def convertToJson(file):
    data = []
    with open(file, 'r') as f:
        for row in csv.DictReader(f):
            data.append(row)

    with open('out/db.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


if __name__ == '__main__':
    while True:
        act = input("Press 'g' to download the database from kaloricketabulky.cz, press 'c' to parse the raw data and create a CSV database, press 'j' to convert the DB to JSON. Press 'q' to quit.\n")

        if act == 'g':
            # TODO add input queries for start and limit
            getPages()
            print("Done!")
        elif act == 'c':
            print('Parsing the raw data and creating a CSV database ...')
            parseData()
            print("Done!")
        elif act == 'j':
            print("Converting to JSON ...")
            convertToJson('out/db.csv')
            print("Done!")
        elif act == 'q':
            print('Quitting.')
            quit()
        else:
            print("Wrong input.")