# -*- coding: utf-8 -*-

import os
import json
import logging
from lxml import html

# Импорт функций для извлечения данных
from extrac import get_attributes_of_product

SAVE_DIR = 'html_files'  # Директория с сохранёнными HTML-файлами
OUTPUT_FILE = 'laptops.json'  # Имя JSON-файла для сохранения результатов

logging.basicConfig(
    filename='local_processing.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_html_page(file_path):
    """Загружает HTML-страницу и преобразует в lxml дерево."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        tree = html.fromstring(content)
        logging.info(f"Файл {file_path} успешно загружен.")
        return tree
    except Exception as e:
        logging.error(f"Ошибка загрузки файла {file_path}: {e}")
        return None

def process_html_files():
    """Обрабатывает HTML-файлы и сохраняет извлечённые данные в JSON-файл."""
    result = {}
    for file_name in os.listdir(SAVE_DIR):
        if file_name.endswith('.html'):
            file_path = os.path.join(SAVE_DIR, file_name)
            tree = load_html_page(file_path)

            if tree is not None:
                try:
                    # Извлечение данных о товаре
                    product_data = get_attributes_of_product(tree)
                    result[file_name] = product_data
                    logging.info(f"Данные из {file_name} успешно извлечены.")
                except Exception as e:
                    logging.error(f"Ошибка при извлечении данных из {file_name}: {e}")

    # Сохранение результатов в JSON
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    logging.info("Обработка завершена, данные сохранены в JSON-файл.")


process_html_files()