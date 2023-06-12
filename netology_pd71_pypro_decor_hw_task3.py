# Применить написанный логгер к приложению из любого предыдущего д/з.

# httprequests_hw_task3
# Нужно написать программу, которая выводит все вопросы за последние
# два дня и содержат тэг 'Python'. Для этого задания токен не требуется.

import requests
import time

from netology_pd71_pypro_decor_hw_task2 import logger


@logger('netology_pd71_pypro_decor_hw_task3.log')
def get_stackoverflow_questions(tag: str = None, days: int = None):
  api_version = '2.3'
  api_url = 'https://api.stackexchange.com/' + api_version + '/'
  api_method = 'questions'
  req_url = api_url + api_method

  req_params = {
    'site': 'stackoverflow',
    'sort': 'creation',
    'todate': int(time.time())
  }
  if isinstance(tag, str):
    req_params['tagged'] = tag
  if isinstance(days, int):
    req_fromdate = int(time.time()) - (60 * 60 * 24 * days)
    req_params['fromdate'] = req_fromdate
  
  resp = requests.get(req_url, params=req_params)

  req_status_code = resp.status_code
  if req_status_code != 200:
    print(f'Error: HTTP request status code is {req_status_code}')
    return

  questions_list = resp.json()['items']
  for question in questions_list:
    q_creation_datetime = time.strftime('%Y-%m-%d %H:%M:%S',
      time.gmtime(question['creation_date']))
    print(f'Question creation date: {q_creation_datetime}')
    print(f'Question title: {question["title"]}\n')
  print(f'Questions amount: {len(questions_list)}')

get_stackoverflow_questions('Python', 2)