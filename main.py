import requests
from bs4 import BeautifulSoup as bs
import csv


def get_all_districts():
    URL = 'https://www.agrobase.ru/selxozpredpriyatiya/rossiya'
    r = requests.get(URL)
    soup = bs(r.text, 'html.parser')

    wrapper = soup.find('ul', class_='sections')
    links = wrapper.select('li > a')

    districts = []
    for li in links:
        districts.append('https://www.agrobase.ru/' + li.get('href'))
    return districts


def get_all_cities(districts):
    cities = []

    for i in districts:
        URL = i
        r = requests.get(URL)
        soup = bs(r.text, 'html.parser')
        wrapper = soup.find('ul', class_='sections')
        links = wrapper.select('li > a')

        for li in links:
            cities.append('https://www.agrobase.ru/' + li.get('href'))
    return cities


def get_all_numbers(cities):
    info = []

    for i in cities:
        URL = i
        r = requests.get(URL)
        soup = bs(r.text, 'html.parser')
        data = soup.find_all('div', class_='ac-company')

        for company in data:
            name = company.find('p').getText()
            details = company.select('.ac-company__details')
            for detail in details:
                try:
                    label = detail.find('dt', text='Телефон:')
                    phone = label.next_sibling.text
                except AttributeError:
                    phone = ''
                info.append([name, phone])
    return info


def write_data(numbers):
    with open('agrobase.csv', 'w', encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter =';')
        writer.writerows(numbers)


def main():
    districts = get_all_districts()
    cities = get_all_cities(districts)
    numbers = get_all_numbers(cities)
    write_data(numbers)


if __name__ == '__main__':
    main()
