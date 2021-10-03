import requests
from bs4 import BeautifulSoup
import csv

def get_html(url):
    respons = requests.get(url)
    return respons.text

def get_all_links(html):
    links = []
    soup = BeautifulSoup(html, 'html.parser')
    divs = soup.find('div', {'id':'content'}).find_all('div', class_='row')

    for karty in divs:
        part_link = karty.find('span', class_='prouct_name').find('a').get('href')
        name = karty.find('span', class_='prouct_name')
        full_link = 'https://enter.kg/videokarty_bishkek' + part_link
        links.append(full_link)
    return links
def get_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    divs = soup.find('div', class_='vm-product-container')
    name = divs.find('span', class_='prouct_name').text
    price = divs.find('span', class_='price').text
    arcticul = divs.find('span', class_='sku').find('span').text
    data = {
        'name': name,
        'price': price,
        'arcticul': arcticul 
    }
    return data
def write_csv(data):
    with open('videokarty.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow(
            (data['name'],
            data['price'],
            data['arcticul'],
            )
        )

def main():
    html = get_html('https://enter.kg/videokarty_bishkek')
    videokarty = get_all_links(html)
    for link in videokarty:
        videokarty_html = get_html(link)
        data = get_data(videokarty_html)
        write_csv(data)

main()