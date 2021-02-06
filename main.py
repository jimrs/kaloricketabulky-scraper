import requests

def getPages(start=1, limit=20026):
    # posledni validni je page=20025
    url = 'https://www.kaloricketabulky.cz/tabulka-potravin'
    for i in range(start, limit):
        data = requests.get(url + '?page=' + str(i))
        print(data.url)

        with open('out/tab' + str(i), 'w') as f:
            f.write(data.text)

if __name__ == '__main__':
    getPages(2164, 10001)