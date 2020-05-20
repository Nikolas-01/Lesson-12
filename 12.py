# Используя HH API, рассчитать среднюю зарплату в Москве по запросу "Python"
import requests
url_currency = 'https://www.cbr-xml-daily.ru/daily_json.js'
response_currency = requests.get(url_currency)
# print(response_currency.status_code)
result_json_currency = response_currency.json()
koef_USD = result_json_currency['Valute']['USD']['Value']
koef_EUR = result_json_currency['Valute']['EUR']['Value']
print(f"Курс валют: {result_json_currency['Date']}")
print(f"USD = {koef_USD}")
print(f"EUR = {koef_EUR}")
data_whole = []
wage = 0
sum_n = 0
url = 'https://api.hh.ru/vacancies'
for page in range(100): # 100 вакансий
    params = {'text': 'Python', 'area':'1','per_page':'10', 'page':page}
    result = requests.get(url, params=params)
    result_json = result.json()
    data_whole.append(result_json)
for item in data_whole: # Перебор
    data = item['items']
    n = 0 # Кол-во вакансий и з.п.
    sum_zp = 0 # Сумматор зарплат
    for record in data: # Перебор вакансий
        if record['salary'] != None: # Есть ли з.п. вакансии
            salary = record['salary']
            if salary['from'] != None: # Есть ли инфо по минимальной зарплате
                n += 1
                # Учитываем курс валюты
                if salary['currency'] == 'USD':
                    koef = koef_USD
                elif salary['currency'] == 'EUR':
                    koef = koef_EUR
                else: koef = 1
                # диапазон з.п.
                if salary['to'] != None:  # Есть ли инфа по максимальной зарпоате в вакансии
                    sum_zp += koef*(salary['from'] + salary['to'])/2
                else:
                    sum_zp += koef*salary['from']
    wage += sum_zp
    sum_n += n
    print(f"Средняя з.п. в Мск {params['text']} составла {round(wage / sum_n, 2)} руб.")