# -*- coding: utf-8 -*-

import re
import logging

def delete_double_spaces(string):
    while '  ' in string:
        string = string.replace('  ', ' ')
    return string

def get_attribute_values(tree):
    try:
        return list(map(lambda span: delete_double_spaces(span.text.replace('\n', '').strip().replace('  ', ' ')), tree.xpath('//span[contains(@class, "YwVL7 _2SUA6 _3kbFf IFARr _1A5yJ")]/child::span')))
    except IndexError:
        logging.warning()
        return None

def get_attribute_names(tree):
    try:
        return int(filter(lambda h3: '&thinsp;' in h3.text, tree.xpath('//h3[contains(@data-auto, "snippet-price-current")]'))[0].text.replace('&thinsp;', ''))
    except IndexError:
        logging.warning()
        return None


def get_attributes_of_product(tree):
    try:
        attribute_names = get_attribute_names(tree)
        attribute_values = get_attribute_values(tree)
        attributes = {}
        for i in range(len(attribute_names)):
            attributes[attribute_names[i]] = attribute_values[i]
        return attributes
    except IndexError:
        logging.warning()
        return None
