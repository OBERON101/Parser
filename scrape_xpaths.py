from random import randint
import pandas
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time
import os
import logging


# Настройка логирования
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

begin_sleep_time = 5
html_pages_count = 5
time_between_clicks = 2
next_card_sleep_time = 4

driver = webdriver.Firefox()
driver.get("https://market.yandex.ru/catalog--noutbuki/26895412/list?hid=91013&local-offers-first=0")
time.sleep(begin_sleep_time)
title_name = "Ноутбуки"
print(driver.title)

try:
    assert title_name in driver.title
    logging.info("Сайт загружен успешно.")
    print("Сайт загружен успешно.")
except AssertionError:
    logging.error("Ошибка загрузки сайта. Заголовок не соответствует ожидаемому.")
    print("Ошибка загрузки сайта. Заголовок не соответствует ожидаемому.")

error_count = 0
links_count = 0
last_links_count = 0
max_not_scrolled_count = 5
not_scrolled_count = 0
with open('links.txt', 'w') as f:
    collected_links = set()
    while links_count < html_pages_count:
        links = driver.find_elements(By.XPATH, "//a[contains(@class, 'EQlfk Gqfzd')]")
        for link in links:
            href = link.get_attribute("href")
            if href not in collected_links:
                collected_links.add(href)
                links_count += 1
                print("Добавлена ссылка: " + href)
                f.write(href + "\n")

        if last_links_count == links_count:
            if not_scrolled_count == max_not_scrolled_count:
                break
            else:
                not_scrolled_count += 1
        else:
            last_links_count = links_count
            not_scrolled_count = 0
        logging.info(f'Текущее количество ссылок: {links_count}. Прокрутка вниз')
        print(f'Текущее количество ссылок: {links_count}. Прокрутка вниз')
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

logging.info(f'Сохранено {links_count} ссылок')
print(f'Сохранено {links_count} ссылок')

os.makedirs('html_files', exist_ok=True)
with open('links.txt', 'r') as f:
    logging.info('Загрузка html-страниц')
    print('Загрузка html-страниц')
    for index, link in enumerate(f, start=1):
        try:
            driver.get(link)
            all_specs_button = driver.find_element(By.XPATH, "//span[contains(@class,'_1_47u _2SUA6 _33utW IFARr _1A5yJ')]")
            all_specs_button.click()
            time.sleep(time_between_clicks)
            all_specs_button.click()
            time.sleep(next_card_sleep_time)
            # Получаем HTML-код страницы товара через Script
            response = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
            # Сохраняем HTML-код страницы в файл с уникальным именем
            with open(f'html_files/page_{index}.html', 'w', encoding='utf-8') as html_file:
                html_file.write(response)
                logging.error(f'Загрузка ссылки №{index}: {link}')
                print(f'Загрузка ссылки №{index}: {link}')
        except ElementClickInterceptedException:
            logging.error(f"Ошибка при загрузке страницы: {link}")
            print(f"Ошибка при загрузке страницы: {link}")

print("Загрузка завершена.")
logging.info("Загрузка завершена.")
driver.quit()