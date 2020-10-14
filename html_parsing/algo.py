#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'jevgeni17'

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = 'http://aliev.me/runestone/'
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')
links = []
for i in soup.select('.toctree-l1 > .reference'):
    href = urljoin(page.url, i.get('href'))
    links.append(href)
with open('file.txt', 'w') as file:
    for i in links:
        file.write(i + '\n')
    file.write(str(len(links)))
#print(links)