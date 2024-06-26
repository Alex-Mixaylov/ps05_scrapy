# НАЧАЛО - ДОМАШНЯЯ РАБОТА

# написать spider для нахождения всех источников освещения с сайта divan.ru
# Нужно взять название источника освещения, цену и ссылку

import scrapy
import pandas as pd
from tkinter import Tk, filedialog


class DivannewparsSpider(scrapy.Spider):
    name = "divannewpars"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://www.divan.ru/category/svet"] # категория  истчников освещения на сайте divan.ru

    def __init__(self, *args, **kwargs):
        super(DivannewparsSpider, self).__init__(*args, **kwargs)
        self.light_list = []

    def parse(self, response):
        # Проверка на наличие ошибки 404. Используется при переборе номеров страниц в каталоге https://www.divan.ru/category/svet
        if response.status == 404:
            return

        # Парсинг товаров на текущей странице
        lights = response.css('div._Ud0k')
        for light in lights:
            item = {
                'name': light.css('div.lsooF span::text').get(),
                'price': light.css('div.pY3d2 span.ui-LD-ZU.KIkOH::text').get(),
                'price_old': light.css('div.pY3d2 span.ui-LD-ZU.ui-SVNym.bSEDs::text').get(default='0'),
                'sale': light.css('div.pY3d2 div.ui-JhLQ7::text').get(default='нет скидки'),
                'url': response.urljoin(light.css('a::attr(href)').get())
            }
            self.light_list.append(item)
            yield item #создание и передача экземпляр данных (в виде словаря, объекта Item или другого типа данных) обратно в Scrapy для дальнейшей обработки

        # Поиск номера текущей страницы
        current_page = response.url.split('-')[-1]
        if current_page.isdigit():
            next_page_number = int(current_page) + 1
        else:
            next_page_number = 2

        # Формирование URL следующей страницы
        next_page_url = f'https://www.divan.ru/category/svet/page-{next_page_number}'

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
            df = pd.DataFrame(self.light_list)
            df.to_excel(file_path, index=False)
# КОНЕЦ - ДОМАШНЯЯ РАБОТА
