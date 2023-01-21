import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import time
import json


def get_link():
    headers = Headers(os='win', browser='chrome')
    hh_ru = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&page=1'
    res = requests.get(hh_ru, headers=headers.generate())
    soup = BeautifulSoup(res.content, 'lxml')
    return soup


def get_data(page):
    soup = get_link()
    page_count = int(
        soup.find("div", attrs={"class": "pager"}).find_all("span", recursive=False)[-1].find("a").find("span").text)
    data = []
    for page in range(1, page_count):
        headers = Headers(os='win', browser='chrome')
        hh_ru = f'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&page={page}'
        res = requests.get(hh_ru, headers=headers.generate())
        soup = BeautifulSoup(res.content, 'lxml')
        for jobs in soup.find_all('div', attrs={'class': 'g-user-content'}):
            if 'Flask' in jobs.text and 'Django' in jobs.text:
                title = soup.find(attrs={'class': 'serp-item__title'}).text
                salary = soup.find('span', attrs={'class': 'bloko-header-section-3'}).text.replace('\u202f', '')
                company = soup.find(attrs={'class': 'bloko-link bloko-link_kind-tertiary'}).text.replace('\xa0', '')
                link = soup.find(attrs={'class': 'serp-item__title'})['href']
                city = soup.find(attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text.replace(',', '')
                city_filt = city.split()
                hh_data = {
                    'title': title,
                    'salary': salary,
                    'city': city_filt[0],
                    'company': company,
                    'link': link
                }
                time.sleep(1)
                data.append(hh_data)
    return data


def load_file(file_name):
    with open(file_name, 'w', encoding='utf8') as f:
        json.dump(get_data(40), f, indent=4, ensure_ascii=False)




if __name__ == '__main__':
    load_file('hh_ru.json')

















































