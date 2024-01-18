import requests
from bs4 import BeautifulSoup


def save_local_html():
    url = 'https://www.takzdorovo.ru/db/nutritives/'
    req = requests.get(url)
    src = req.text
    with open('apps/scripts/index.html', 'w') as file:
        file.write(src)


def get_data():
    save_local_html()
    with open('index.html') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    product_names = soup.find_all('th')
    product_calories = soup.find_all('a', id='calories')
    data = []
    for i in range(len(product_names)):
        name = product_names[i].text
        calories = product_calories[i].text
        data.append([name, calories])
    return data
