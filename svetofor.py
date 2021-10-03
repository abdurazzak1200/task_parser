import requests
from bs4 import BeautifulSoup
import csv

def get_html(url):
    response = requests.get(url)
    return response.text
def get_all_links(html):
    links = []
    soup = BeautifulSoup(html, 'html.parser')
    divs = soup.find('div', class_='ty-pagination-container cm-pagination-container').find_all('div', class_='ty-column4')
    for phons in divs:
        phone_link = phons.find('div', class_='front').find('a').get('href')
        links.append(phone_link)
    return links


def get_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    divs = soup.find('div', class_='ty-product-block ty-product-detail')
    name_code = divs.find('h1', class_='ty-product-block-title').text
    price = divs.find('span', class_='ty-price-num')
    if price:
        price = price.text.strip()
    else:
        price = 'Предзаказ'

    description = divs.find('div', class_='ty-features-list')
    if description:
        description = description.text.strip()
    else:
        description = 'Нет описания'

    in_stock = divs.find('span', class_='ty-qty-out-of-stock ty-control-group__item').text
    buy = divs.find('a', class_='ty-btn ty-btn__text ty-add-to-compare cm-ajax cm-ajax-full-render text-button').get('href')
    data = {
        'name_code': name_code,
        'price': price,
        'description': description,
        'in_stock': in_stock,
        'buy': buy
    }
    return data

def write_csv(data):
    with open('phone.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow(
            (data['name_code'],
            data['price'],
            data['description'],
            data['in_stock'],
            data['buy'],
            )
        )




def main():
    for page in range(1,14):
        url = f'https://svetofor.info/gadzhety-i-umnyj-dom/page-{page}'
        html = get_html(url)
        phone_links = get_all_links(html)
        for link in phone_links:
            phons_html = get_html(link)
            data = get_data(phons_html)
            write_csv(data)

main()