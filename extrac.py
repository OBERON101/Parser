# -*- coding: utf-8 -*-

import logging


def delete_double_spaces(string):
    while '  ' in string:
        string = string.replace('  ', ' ')
    return string


def get_attribute_values(tree):
    try:
        return list(map(lambda span: delete_double_spaces(span.text.replace('\n', '').strip().replace('  ', ' ')),
                        tree.xpath('//span[contains(@class, "YwVL7 _2SUA6 _3kbFf IFARr _1A5yJ")]/child::span')))
    except IndexError:
        logging.warning('Не удалось извлечь значения аттрибутов продукта')
        return None


def get_attribute_names(tree):
    try:
        return list(map(lambda span: delete_double_spaces(span.text.replace('\n', '').strip().replace('  ', ' ')),
                        tree.xpath('//span[contains(@class, "_1EbOn _2SUA6 _3kbFf IFARr _1A5yJ")]')))
    except IndexError:
        logging.warning('Не удалось извлечь наименования аттрибутов продукта')
        return None


def get_attributes_of_product(tree):
    try:
        attribute_names = get_attribute_names(tree)
        attribute_values = get_attribute_values(tree)
        attributes = {}
        for i in range(len(attribute_names)):
            attributes[attribute_names[i]] = attribute_values[i]
        attributes['price'] = get_price(tree)
        attributes['price_without_yandex_card'], attributes['price_without_discount'] = get_price_alternative(tree)
        return attributes
    except IndexError:
        logging.warning('Не удалось извлечь аттрибуты продукта')
        return None


def get_price(tree):
    try:
        return int(list(filter(lambda h3: 'Цена с картой' in h3.text_content(),
                               tree.xpath('//h3[contains(@data-auto, "snippet-price-current")]')))[0]
                   .text_content().replace('Цена с картой Яндекс Пэй:', '').replace(' ', '').replace(' ₽', ''))
    except IndexError:
        raise IndexError('Не удалось извлечь цену продукта')


def get_price_alternative(tree):
    try:
        return list(map(lambda x: int(x), filter(lambda x: x != '', map(lambda x: x.replace('\u2009', ''), tree.xpath(
            '//span[contains(@data-auto, "snippet-price-old")]')[0].text_content().replace('без:\xa0Вместо: ','').split('\u2009₽')))))
    except IndexError:
        raise IndexError('Не удалось извлечь цену продукта')
