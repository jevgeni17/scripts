#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class Parser:

    def __init__(self, url):
        self.url = url
        self.links = []

    def parse(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')
        for i in soup.select('.toctree-l1 > .reference'):
            href = urljoin(page.url, i.get('href'))
            self.links.append(href)
        return self.links
    
    def save_result_to_file(self):
        with open('output.txt', 'w') as file:
            for i in self.links:
                file.write(i + '\n')

obj = Parser('http://aliev.me/runestone/')
obj.parse()
obj.save_result_to_file()



