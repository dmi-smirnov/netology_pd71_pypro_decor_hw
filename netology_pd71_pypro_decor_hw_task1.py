# Доработать декоратор logger в коде ниже.
# Должен получиться декоратор, который записывает
# в файл 'main.log' дату и время вызова функции,
# имя функции, аргументы, с которыми вызвалась,
# и возвращаемое значение.
# Функция test_1 в коде ниже также должна отработать без ошибок.


import os
import time


def logger(old_function):
  def new_function(*args, **kwargs):
    def log(log_file_path, message):
      cur_datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
      new_log_row = f'{cur_datetime} {message}'

      with open(log_file_path, 'a') as log_file:
        log_file.write(f'{new_log_row}\n')
    
    log_file_dir_path = os.path.dirname(__file__)
    log_file_name = 'main.log'
    log_file_path = os.path.join(log_file_dir_path, log_file_name)

    log_message =\
      f'Вызвана функция {old_function.__name__} с аргументами {args} {kwargs}.'
    log(log_file_path, log_message)

    func_result = old_function(*args, **kwargs)

    log_message =\
      f'Функция {old_function.__name__} вернула {func_result}.'
    log(log_file_path, log_message)

    return func_result

  return new_function


def test_1():

  path = 'main.log'
  if os.path.exists(path):
    os.remove(path)

  @logger
  def hello_world():
    return 'Hello World'

  @logger
  def summator(a, b=0):
    return a + b

  @logger
  def div(a, b):
    return a / b

  assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
  result = summator(2, 2)
  assert isinstance(result, int), 'Должно вернуться целое число'
  assert result == 4, '2 + 2 = 4'
  result = div(6, 2)
  assert result == 3, '6 / 2 = 3'
  
  assert os.path.exists(path), 'файл main.log должен существовать'

  summator(4.3, b=2.2)
  summator(a=0, b=0)

  with open(path) as log_file:
    log_file_content = log_file.read()

  assert 'summator' in log_file_content, 'должно записаться имя функции'
  for item in (4.3, 2.2, 6.5):
    assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
  test_1()