#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'jevgeni17'


from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import requests

links_list = ['rahvaraamat.ee/search/productList/en?offset=0&limit=10&searchTerm={}', 'bookvoed.ee/search?q={}&count=50#page-1', 'mnogoknig.ee/search/{}']

def createURL(keywordsList,urlExample): # returns a serach url with user keywords
    """ NOTICE!  white fang  - there is a book title example (which user will write in the form as a keyword)
        urlExample -             rahvaraamat.ee/search/productList/en?offset=0&limit=10&searchTerm={} - where {} there are search keywords
        function will return =>  rahvaraamat.ee/search/productList/en?offset=0&limit=10&searchTerm=мартин+иден  - instead of  {} will paste search keywords
                                 bookvoed.ee/search?q={}&count=50#page-1 =>  bookvoed.ee/search?q=white+fang
                                 mnogoknig.ee/search/{}  =>   mnogoknig.ee/search/white+fang
    """
    plusKeywords = '+'.join(keywordsList)
    url = 'https://' + urlExample.replace("{}",plusKeywords)
    return url

def item_url(page,class1,secondClass=None): # returns list of links for each item in search page.
    #.title > a.js-link-product     - rahvaraamat
    #.o-row > a.title               - bookvoed
    #.col-xs-8 > a                  - mnogoknig
    page = requests.get(page)
    soup = BeautifulSoup(page.content, 'html.parser')
    links = []
    
    if secondClass == None:
        string = f".{class1} > a"
    else:
        string = f".{class1} > a.{secondClass}"

    for a in soup.select(string):
        href = urljoin(page.url, a.get('href'))
        links.append(href)

    return links

def item_price(page,class1,secondClass=None): # returns list of prices for each item in search page
    # .meta > p.price - rahvaraamat
    # .buy > span     - bookvoed
    # .price          -mnogoknig
    page = requests.get(page)
    soup = BeautifulSoup(page.content, 'html.parser')
    prices = []
    if secondClass == None:
        string = f".{class1}"
    elif secondClass == 'span':
        string = f".{class1} > {secondClass}"
    elif secondClass == 'price':
        string = f".{class1} > p.{secondClass}"

    for p in soup.select(string):
        p =  p.get_text()
        prices.append(p)
    prices = [i.partition(' €')[0] for i in prices] # delete unnecessary symbols
    prices = [i.strip() for i in prices] # delete whitespaces
    prices = [i.replace('€','') for i in prices] # delete unnecessary symbols
    return prices

def clean_dict(dict1):
    copy = dict1.copy()
    for k, v in copy.items():    
        if v == 'Out of stock':
            del dict1[k]
        elif v == 'This product is not available on e-store':
            del dict1[k]
    return dict1


#name = request.POST.get("name")
name = "white fang"
user_keywords = name.split(" ") 

rahvaraamat_url = createURL(user_keywords,links_list[0]) 
bookvoed_url = createURL(user_keywords,links_list[1])
mnogoknig_url = createURL(user_keywords,links_list[2])

rahvaraamat_links = item_url(rahvaraamat_url,'title', 'js-link-product') # def item_url(page,class1,secondClass=None)
bookvoed_links = item_url(bookvoed_url,'o-row', 'title')
mnogoknig_links = item_url(mnogoknig_url,'col-xs-8')

rahvaraamat_prices = item_price(rahvaraamat_url, 'meta', 'price') # def item_price(page,class1,secondClass=None)
bookvoed_prices = item_price(bookvoed_url, 'buy', 'span')
mnogoknig_prices = item_price(mnogoknig_url, 'price')

rahvaraamat_dict =  dict(zip(rahvaraamat_links, rahvaraamat_prices)) # combine links-list and price-list to dictionary
rahvaraamat_dict = clean_dict(rahvaraamat_dict) # def clean_dict(dict1)
bookvoed_dict =  dict(zip(bookvoed_links, bookvoed_prices))
mnogoknig_dict =  dict(zip(mnogoknig_links, mnogoknig_prices))

rahvaraamat_dict.update(bookvoed_dict) #combine dictionaries
rahvaraamat_dict.update(mnogoknig_dict) #combine dictionaries

converted_to_num = dict((k, float(v)) for k,v in rahvaraamat_dict.items()) # convert dict values to float

lowest_price_url = min(converted_to_num, key=converted_to_num.get)
highest_price_url = max(converted_to_num, key=converted_to_num.get)

print(f'lowest price -> {lowest_price_url}')
print(f'highest price -> {highest_price_url}')
