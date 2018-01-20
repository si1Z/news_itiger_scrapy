#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/18 15:08
# @Author  : zhujinghui
# @File    : test.py
# @Software: PyCharm
import requests
from bs4 import BeautifulSoup
# url = "https://stock-news.itiger.com/news/list?symbols=JD"
# url = "http://stock-news.tigerbrokers.com/news/detail?id=9648369"
# rsp = requests.get(url)
# # print(rsp.text)
# text = rsp.text
#
# with open('tmp.txt','w',encoding='utf-8') as f:
#     f.write(text)
with open('tmp.txt','r',encoding='utf-8') as f:
    text = f.read()

def parse_page():
    soup = BeautifulSoup(text,'lxml')
    header = soup.find('header')
    article = soup.find('article')

    original_url = header.find('a',text='查看原网页').get('href')

    ps = article.find_all('p', recursive=False)
    ss = str()
    for p in ps:
        tmp = p.get_text()
        ss = ss + str(tmp).strip() + "\n"

parse_page()
