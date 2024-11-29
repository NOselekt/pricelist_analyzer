import os
import json
from prettytable import PrettyTable

KEY_WORD = "price"
HEADERS_NAMES = (("название", "продукт", "товар", "наименование"),  # Допустимые названия для столбца с товаром
                 ("цена", "розница"),  # Допустимые названия для столбца с ценой
                 ("фасовка", "масса", "вес"))  # Допустимые названия для столбца с весом (в кг)


class PriceMachine():

    def __init__(self):
        self._data = []

    def load_prices(self, file_path: str ='.') -> list[tuple]:
        '''
        Сканирует указанный каталог. Ищет файлы со словом price в названии.
        В файле ищет столбцы с названием товара, ценой и весом.
        :param file_path: директория, в которой ищутся файлы
        :return: список кортежей с данными товаров
        '''

        directory = os.listdir(file_path)

        result = []

        for file_name in directory:
            if "price" in file_name:
                with open(file_name, 'r', encoding='utf-8') as file:
                    headers = file.readline().strip().split(',')
                    headers_numbers = self._search_product_price_weight(headers)
                    for line in file.readlines():
                        line = line.strip().split(',')
                        name = line[headers_numbers[0]]
                        price = float(line[headers_numbers[1]])
                        weight = float(line[headers_numbers[2]])
                        kg_price = round(float(line[headers_numbers[1]]) / float(line[headers_numbers[2]]), 2)
                        product = (name, price, weight, file_name, kg_price)
                        self._data.append(product)
                        result.append(product)
        return result

    def _search_product_price_weight(self, headers: list[str]) -> list[int]:
        '''
        Возвращает номера столбцов
        :param headers: список названий столбцов (должны идти в том же порядке, что и в файле)
        :return:
        '''

        indexes = [i for i in range(len(HEADERS_NAMES))]

        for index, header in enumerate(headers):
            for number, names in enumerate(HEADERS_NAMES):
                if header in names:
                    indexes[number] = index

        if all(map(lambda x: x is not None, indexes)):
            return indexes

        raise ValueError("Отсутствуют необходимые столбцы")

    def export_to_html(self, fname: str = 'output.html') -> None:
        '''
        Экспортирует данные в HTML-шаблон в виде таблицы
        :param fname: название HTML-шаблона
        :return: None
        '''
        result = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Позиции продуктов</title>
        </head>
        <body>
            <table>
                <thead>
                    <tr>
                        <th>Номер</th>
                        <th>Название</th>
                        <th>Цена</th>
                        <th>Фасовка</th>
                        <th>Файл</th>
                        <th>Цена за кг</th>
                    </tr>
                </thead>
                <tbody>
        '''
        for number, product in enumerate(self._data):
            result += f'''
                <tr>
                    <td>{number}</td>
                    <td>{product[0]}</td>
                    <td>{product[1]}</td>
                    <td>{product[2]}</td>
                    <td>{product[3]}</td>
                    <td>{product[4]}</td>
                </tr>
            '''

        result += '''
                </tbody>
            </table>
        </body>
        </html>
        '''

        with open(fname, 'w', encoding='utf-8') as file:
            file.write(result)

    def find_text(self, text: str) -> list[tuple]:
        '''
        Ищет в загруженных с помощью load_prices данных товары с названием, содержащем указанный текст.
        :param text: искомый текст
        :return: список кортежей с данными товаров
        '''
        text = text.lower()
        if text:
            result = []
            for product in self._data:
                if text in product[0].lower():
                    result.append(product)
            return result
        else:
            return self._data


pm = PriceMachine()

headers = ["№", "Наименование", "цена", "вес", "файл", "цена за кг"]

products = pm.load_prices()

table = PrettyTable(headers)

for number, product in enumerate(products):
    table.add_row((number,) + product)

print(table)

while True:
    text = input("Введите название товара: ")
    if text == "exit":
        break

    products = sorted(pm.find_text(text), key=lambda x: x[-1])

    table = PrettyTable(headers)
    for number, product in enumerate(products):
        table.add_row((number,) + product)
    print(table)

print('the end')
pm.export_to_html()
