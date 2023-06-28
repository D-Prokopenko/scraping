import requests
import codecs
from bs4 import BeautifulSoup as BS
from random import randint



__all__ = ("rabota", "superjob")

headers = [{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) Chrome/114.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
            },
           {
               'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
           },
           {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
            }
           ]


def rabota(url, city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://spb.rabota.ru/'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        # проверка ответа
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', attrs={'class': 'r-serp'})
            if main_div:
                div_list = main_div.find_all('div', attrs={'class': 'r-serp__item r-serp__item_vacancy'})
                for div in div_list:
                    title = div.find('h3')
                    href = title.a['href']
                    content = div.find('div', attrs={'class': 'vacancy-preview-card__short-description'})
                    company = 'No name'
                    logo = div.find('img')
                    if logo:
                        company = logo['alt']

                    jobs.append({'title': title.text, 'url': domain + href,
                                 'description': content.text, 'company': company,
                                 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': 'Div does not exists'})

        else:
            errors.append({'url': url, 'title': 'Page not response', 'code': resp.status_code})
    return jobs, errors


def superjob(url, city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://spb.superjob.ru/'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        # проверка ответа
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', attrs={'class': 'QLXR1 _3NNyT _2qBHz'})
            if main_div:
                div_list = main_div.find_all('div', attrs={'class': 'f-test-search-result-item'})
                for div in div_list:
                    title = div.a
                    if title:
                        href = title['href']
                        content = div.find('span', attrs={'class': '_2HZhY _16BIl _1wutB _2ZnQY _2Hx5_'})
                        company = 'No name'
                        logo = div.find('span', attrs={'class': 'f-test-text-vacancy-item-company-name'})
                        if logo:
                            company = logo.a.text
                        if content:
                            jobs.append(
                                {'title': title.text, 'url': domain + href,
                                 'description': content.text, 'company': company,
                                 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': 'Div does not exists'})

        else:
            errors.append({'url': url, 'title': 'Page not response', 'code': resp.status_code})
    return jobs, errors


if __name__ == '__main__':
    url = ''
    jobs, errors = superjob(url)
    with codecs.open('rabota.txt', 'w', 'utf-8') as h:
        h.write(str(jobs))
