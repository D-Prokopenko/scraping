import asyncio

""" Запуск Django вне самого проекта """
import os, sys
import datetime as dt

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = 'scraping_service.settings'

import django
django.setup()

"""=================================================================="""
from django.contrib.auth import get_user_model
from django.db import DatabaseError
from scraping.parser import *
from scraping.models import Vacancy, Error, Url

User = get_user_model()

parsers = ((rabota, 'rabota'),
           (superjob, 'superjob')
           )

jobs, errors = [], []


def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_ls = set((q['city_id'], q['language_id']) for q in qs)
    return settings_ls


def get_urls(_settings):
    qs = Url.objects.all().values()
    url_dct = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []

    for pair in _settings:
        if pair in url_dct:
            tmp = {}
            tmp['city'] = pair[0]
            tmp['language'] = pair[1]
            tmp['url_data'] = url_dct[pair]
            urls.append(tmp)
    return urls


async def main(value):
    func, url, city, language = value
    job, err = await loop.run_in_executor(None, func, url, city, language)
    errors.extend(err)
    jobs.extend(job)

settings = get_settings()
url_list = get_urls(settings)

loop = asyncio.new_event_loop()
tmp_tasks = [(func, data['url_data'][key], data['city'], data['language'])
             for data in url_list
             for func, key in parsers]

tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])

loop.run_until_complete(tasks)
loop.close()
""" Сохранение данных в базу """

for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass

if errors:
    qs = Error.objects.filter(timestamp=dt.date.today())
    if qs.exists():
        err = qs.first()
        err.data.update({'errors': errors})
        err.save()
    else:
        er = Error(data=f'errors: {errors}').save()
