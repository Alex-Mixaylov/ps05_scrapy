# import scrapy
#
#
# class DivannewparsSpider(scrapy.Spider):
#     name = "divannewpars"
#     allowed_domains = ["https://divan.ru"]
#     # start_urls - это та ссылка, от которой начинается парсинг
#     start_urls = ["https://divan.ru/category/divany-i-kresla"]
#
#
#
#     def parse(self, response):
#         divans = response.css('div._Ud0k')
#         for divan in divans:
#             yield {
#                 'name': divan.css('div.lsooF span::text').get(),
#                 'price': divan.css('div.pY3d2 span::text').get(),
#                 'url': divan.css('a::attr(href)').get()
#             }
#
# #Вариант с сохранением данных в exel файл
#
# import scrapy
# import pandas as pd
# from tkinter import Tk, filedialog
#
# class DivannewparsSpider(scrapy.Spider):
#     name = "divannewpars"
#     allowed_domains = ["divan.ru"]
#     start_urls = ["https://divan.ru/category/divany-i-kresla"]
#
# #Функция __init__ является конструктором класса в Python и используется для инициализации объекта класса
# # *args позволяет передать функции произвольное количество неименованных аргументов. Аргументы собираютяс в кортеж
# # **kwargs позволяет передать произвольное количество именованных аргументов. Аргументы собираются в словарь
#     def __init__(self, *args, **kwargs):
#         super(DivannewparsSpider, self).__init__(*args, **kwargs)
#         self.divan_list = []
#
#     def parse(self, response):
#         divans = response.css('div._Ud0k')
#         for divan in divans:
#             item = {
#                 'name': divan.css('div.lsooF span::text').get(),
#                 'price': divan.css('div.pY3d2 span::text').get(),
#                 'url': divan.css('a::attr(href)').get()
#             }
#             #  создание и передача экземпляр данных (в виде словаря, объекта Item или другого типа данных)
#             # обратно в Scrapy для дальнейшей обработки.
#             self.divan_list.append(item)
#             yield item
#
#     def closed(self, reason):
#         # Запрос имени файла и пути для сохранения
#         root = Tk()
#         root.withdraw()  # Скрыть главное окно
#         file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
#
#         # Сохранение данных в Excel файл
#         if file_path:
#             df = pd.DataFrame(self.divan_list)
#             df.to_excel(file_path, index=False)
#

#Вариант с сохранением данных в exel файл и обработкой всех страницы в категории https://www.divan.ru/category/divany-i-kresla
# Страницы 01-37, 38 страница выдает  404 ошибку

import scrapy
import pandas as pd
from tkinter import Tk, filedialog


class DivannewparsSpider(scrapy.Spider):
    name = "divannewpars"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://www.divan.ru/category/divany-i-kresla"]

    def __init__(self, *args, **kwargs):
        super(DivannewparsSpider, self).__init__(*args, **kwargs)
        self.divan_list = []

    def parse(self, response):
        # Проверка на наличие ошибки 404
        if response.status == 404:
            return

        # Парсинг товаров на текущей странице
        divans = response.css('div._Ud0k')
        for divan in divans:
            item = {
                'name': divan.css('div.lsooF span::text').get(),
                'price': divan.css('div.pY3d2 span::text').get(),
                'url': divan.css('a::attr(href)').get()
            }
            self.divan_list.append(item)
            yield item

        # Поиск номера текущей страницы
        current_page = response.url.split('-')[-1]
        if current_page.isdigit():
            next_page_number = int(current_page) + 1
        else:
            next_page_number = 2

        # Формирование URL следующей страницы
        next_page_url = f'https://www.divan.ru/category/divany-i-kresla/page-{next_page_number}'

        # Переход на следующую страницу
        yield scrapy.Request(url=next_page_url, callback=self.parse)

    def closed(self, reason):
        # Запрос имени файла и пути для сохранения
        root = Tk()
        root.withdraw()  # Скрыть главное окно
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])

        # Сохранение данных в Excel файл
        if file_path:
            df = pd.DataFrame(self.divan_list)
            df.to_excel(file_path, index=False)

