import csv
from datetime import datetime
from copy import deepcopy


def get_data(path_to_file: str) -> list:
    """
    :param path_to_file: path to file (str)
    :return: list of transactions (list)
    """
    answer = list()
    key_list = ['Дата операции', 'Сумма операции', 'Категория', 'Описание']
    with open(path_to_file, 'r') as file:
        in_data = csv.DictReader(file, delimiter=';')
        for el in in_data:
            operation = dict()
            for key, val in el.items():
                if key in key_list:
                    if key == 'Дата операции':
                        val = datetime.strptime(val, '%d.%m.%Y %H:%M')
                    elif key == 'Сумма операции':
                        val = float(val.replace(',', '.'))
                    operation[key] = val
            answer.append(operation)
        file.close()
    return answer


def get_data_by_period(path_to_file: str, date_1: str, date_2: str) -> list:
    """
    :param path_to_file: path to file (str)
    :param date_1: First date (str in format '01.02.2003')
    :param date_2: Second date (str in format '04.05.2006')
    :return: data_by_period (list of transactions between first date and second date)
    """
    date_1 = datetime.strptime(date_1 + ' 00:00:00', '%d.%m.%Y %H:%M:%S')
    date_2 = datetime.strptime(date_2 + ' 23:59:59', '%d.%m.%Y %H:%M:%S')
    answer = [el for el in get_data(path_to_file) if date_1 <= el['Дата операции'] <= date_2]
    return answer


def get_categories(input_data: list) -> list:
    """
    :param input_data: list of transactions (list)
    :return: categories (list)
    """
    categories = {val for el in input_data for key, val in el.items() if key == 'Категория'}
    categories = sorted(list(categories))
    return categories


def get_data_by_categories(input_data: list) -> dict:
    """
    :param input_data:  list of transactions (list)
    :return: dict (key = Category name, val = list of transactions for this category)
    """
    input_data_here = deepcopy(input_data)  # Just for non-traumatic deleting key_val from elements of data
    categories = {val for el in input_data_here for key, val in el.items() if key == 'Категория'}
    answer = dict()
    for category in categories:
        answer[category] = list()
    for operation in input_data_here:
        formatted_operation = operation
        category = formatted_operation['Категория']
        del formatted_operation['Категория']  # Deepcopy above has been needed for this operation
        answer[category].append(formatted_operation)
    return answer


def get_summary_by_categories(input_data: list) -> dict:
    """
    :param input_data: list (list of transactions)
    :return: dict (key = Category name, val = total of transactions for this category)
    """
    data_by_categories = get_data_by_categories(input_data)
    answer = dict()
    for category, operations in data_by_categories.items():
        total = 0
        for operation in operations:
            total += operation['Сумма операции']
        answer[category] = total
    answer = {key: val for key, val in sorted(answer.items())}
    return answer


def get_total(input_data: list) -> float:
    """
    :param input_data: list (list of transactions)
    :return: TOTAL of all transactions except categories ['Отели', 'Переводы', 'Пополнения', '']
    """
    answer = 0
    for el in input_data:
        if el['Сумма операции'] < 0:
            if el['Категория'] not in ['Отели', 'Переводы', 'Пополнения', '']:
                answer += el['Сумма операции']
    return round(answer, 2)


def get_my_salary(input_data: list) -> list:
    """
    :param input_data: list (list of transactions)
    :return: dict (key = data of "TrueConf" transaction, val = transaction amount)
    """
    data_by_categories = get_data_by_categories(input_data)
    answer = []
    for el in data_by_categories['Пополнения']:
        if el['Описание'] == 'Пополнение через Московский Филиал АО КБ "Модульбанк"':
            answer.append((el['Дата операции'], el['Сумма операции']))
    return answer


def print_categories(input_data: list):
    """
    :param input_data: list (list of transactions)
    """
    categories = get_categories(input_data)
    for category in categories:
        print(category)


def print_data_by_categories(input_data: list):
    """
    :param input_data: list (list of transactions)
    """
    data_by_categories = get_data_by_categories(input_data)
    for key in data_by_categories.keys():
        print('CATEGORY:', key)
        total = 0
        for el in data_by_categories[key]:
            print([val for key, val in el.items() if key != 'Дата операции'])
            total += el['Сумма операции']
        print('TOTAL:', round(total, 2))
        print()


def print_period_info(input_data: list):
    """
    :param input_data: list (list of transactions)
    """
    dates = []
    for el in input_data:
        dates.append(el['Дата операции'])
    d1 = min(dates).date()
    d2 = max(dates).date()
    diff = (d2 - d1).days
    print('Start period:', d1.strftime('%d.%m.%y'))
    print('End period:', d2.strftime('%d.%m.%y'))
    print('Period:', diff // 30, 'months and', diff % 30, 'days')


def print_salaries(input_data: list):
    """
    :param input_data: list (list of transactions)
    """
    salary = [[el[0], el[1]] for el in get_my_salary(input_data)[::-1]]
    for el in salary:
        print(el[0].strftime('%d.%m.%y'), ' --- ', el[1])
    ZP = [el[1] for el in salary]
    print()
    print(sum(ZP))




"""
FUNCTIONS:
* get_data(path_to_file: str) <<< returns list of transactions
* get_data_by_period(path_to_file: str, date_1: str, date_2: str) <<< returns data_by_period (list of transactions between first date and second date)
* get_categories(input_data: list) <<< returns categories (list)
* get_data_by_categories(input_data: list) <<< returns dict (key = Category name, val = list of transactions for this category)
* get_summary_by_categories(input_data: list) <<< returns dict (key = Category name, val = TOTAL of transactions for this category)
* get_total(input_data: list) <<< returns TOTAL of all transactions except categories ['Отели', 'Переводы', 'Пополнения', '']
* get_my_salary(input_data: list) <<< returns dict (key = data of "TrueConf" transaction, val = transaction amount)
* print_categories(input_data: list)
* print_data_by_categories(input_data: list)
* print_period_info (input_data: list)
* print_salaries (input_data: list)
"""

path = 'all_operations.csv'
data = get_data_by_period(path, '28.11.2022', '10.02.2023')

"""
data_by_categories = get_data_by_categories(data)
for key, val in data_by_categories.items():
    print()
    print('KEY: "' + key + '"')
    for el in val:
        date = datetime.strftime(el['Дата операции'], '%d.%m.%Y')
        amount = el['Сумма операции']
        description = el['Описание']
        print(date, amount, description)
"""
print_data_by_categories(data)
salary = get_my_salary(data)
print()
print('SALARY:')
for el in salary:
    print(el[1], '---', el[0].strftime('%d.%m.%y'))
