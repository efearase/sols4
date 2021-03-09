import requests
from bs4 import BeautifulSoup
import unittest
import re

# При открытии файла, добавьте в функцию open необязательный параметр
# encoding='utf-8', его отсутствие в коде будет вызвать падение вашего
# решения на грейдере с ошибкой UnicodeDecodeError
path_to_file = '/Users/gosa/Desktop/инфа/sols4/wiki/Stone_Age'


def get_html(path_to_file):
    html = ''
    with open(path_to_file, 'r', encoding='utf-8') as file:
        html = file.read()
    return html


html = get_html(path_to_file)
soup = BeautifulSoup(html, "html.parser")
body = soup.find(id="bodyContent")


def img_parser(html=html, body=body):
    imgs = body.find_all('img')
    fit_imgs = len(
        [x for x in imgs if x.get('width') and int(x.get('width')) >= 200]
    )
    return fit_imgs


def header_parser(html=html, body=body):
    headers = body.find_all(re.compile('^h[1-6]$'))
    count = 0
    for header in headers:
        children = header.find_all(recursive=False)
        if children:
            children_content = [x.getText() for x in children if x.getText()]
            try:
                first_letter = children_content[0][0]
                if first_letter in 'ETC':
                    count += 1
            except IndexError:
                pass
        else:
            try:
                first_letter = header.getText()[0]
                if first_letter in 'ETC':
                    count += 1
            except IndexError:
                pass
    return count


def link_parser(html=html, body=body):
    max_count = 0
    all_links = body.find_all('a')
    for link in all_links:
        current_count = 1
        siblings = link.find_next_siblings()
        for sibling in siblings:
            if sibling.name == 'a':
                current_count += 1
                max_count = max(current_count, max_count)
            else:
                current_count = 0
    return max_count


def list_parser(html=html, body=body):
    count = 0
    all_lists = body.find_all(['ul', 'ol'])
    for tag in all_lists:
        if not tag.find_parents(['ul', 'ol']):
            count += 1
    return count


def parse(path_to_file):
    html = get_html(path_to_file)
    soup = BeautifulSoup(html, "html.parser")
    body = soup.find(id="bodyContent")
    return [img_parser(), header_parser(), link_parser(), list_parser()]


print(parse(path_to_file))