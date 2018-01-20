# -*- coding: utf-8 -*-
import scrapy
import json
import redis
from ..items import NewsArticleItem
from urllib.parse import urlparse,parse_qs
from bs4 import BeautifulSoup
# url = "https://stock-news.itiger.com/news/list?symbols=AAPL&pageCount=6&deviceId=web20170619_20316&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.0.0"
# url = "https://stock-news.itiger.com/news/list?symbols=AAPL"

#获得redis里存有的股票代码列表
def get_Dynamic_Symbols():
    client = redis.Redis(host='47.94.19.25', port=6379, db=6, password='root_db', decode_responses=True)
    codeset_400 = client.smembers("symbols400")
    codeset_temp = client.smembers("symbols.temp")
    codeset = codeset_400 | codeset_temp
    return list(codeset)
def get_All_Symbols():
    client = redis.Redis(host='47.94.19.25', port=6379, db=6, password='root_db', decode_responses=True)
    codeset_8000 = client.smembers("symbols8000")
    return list(codeset_8000)

#生成起始url列表
def get_start_urls(codes=get_All_Symbols()):
    for code in codes:
        try:
            # rediscache.set_redis(code,get_news_lasttime(code))
            baseurl = "https://stock-news.itiger.com/news/list?symbols={}".format(code)
            yield baseurl
        except:
            continue

class NewsItigerSpider(scrapy.Spider):
    name = "news_itiger"
    # allowed_domains = ["itiger.com"]
    # start_urls = [url]
    start_urls = get_start_urls()
    custom_settings = {

        'MONGODB_SERVER': 'dds-2ze641fbc7603b641871-pub.mongodb.rds.aliyuncs.com',
        'MONGODB_PORT':3717,
        'MONGODB_USER':'root',
        'MONGODB_PWD':'Ygkj@2017',
        'MONGODB_DB': 'newsdb',
        'MONGODB_COLLECTION': 'itiger_news_test',

        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': None,
            # 'data_scrapy_redis.middlewares.headers.xueqiu_headers_middlewares.UserAgentMiddleware': 100,
            # 'data_scrapy_redis.middlewares.cookies.xueqiu_cookies_middlewares.CookiesMiddleware': 101,
            # 'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
        },

        'ITEM_PIPELINES': {
            'news_itiger_scrapy.pipelines.MongoDBPipeline':100
            # 'dbf_scrapy_redis.pipelines.xueqiupipelines.MySQLStorePipeline_sec': 200,
        },
    }

    def parse_page(self,response):
        article = response.meta['article']
        html = response.body_as_unicode()

        soup = BeautifulSoup(html, 'lxml')

        header = soup.find('header')
        article_el = soup.find('article')

        try:
            original_url = header.find('a', text='查看原网页').get('href')
            article['source_url'] = original_url
        except:
            with open('err_url.txt','a',encoding='utf-8') as f:
                f.write(response.url+'\n')
        ps = article_el.find_all('p', recursive=False)
        ss = str()
        for p in ps:
            tmp = p.get_text()
            ss = ss + str(tmp).strip() + "\n"


        article['article_detail'] = ss

        print(article)
        return article

    def parse(self, response):
        url = response.url
        parms = parse_qs(urlparse(url).query, True)

        text = response.body_as_unicode()
        data_json = json.loads(text)
        totalSize = data_json['totalSize']
        totalPage = data_json['totalPage']
        pageCount = data_json['pageCount']
        pageSize = data_json['pageSize']
        items = data_json['items']

        # with open('data{}.txt'.format(pageCount), 'w',encoding='utf-8') as f:
        #     f.write(str(data_json))

        for item in items:
            article = NewsArticleItem()
            # 股票号
            article['symbol'] = item.get('symbol',"")
            # 股票名
            article['symbol_name'] = item.get('symbol_name', "")
            # 时间
            article['pub_time'] = item.get('pubTime',"")
            #发布时间戳
            article['pub_time_stamp'] = item.get('pubTimestamp', "")
            # 标题
            article['article_title'] = item.get('title',"")
            # 内容摘录
            article['article_summary'] = item.get('summary',"")
            # 老虎网址
            article['itiger_url'] = item.get('url',"")
            # 来源
            article['source_media'] = item.get('media',"")
            #内容是否为英语
            article['is_english'] = item.get('is_english', "")

            yield scrapy.Request(article['itiger_url'],meta={'article': article},callback=self.parse_page)

        if pageCount<totalPage:
            changePageUrl = "https://stock-news.itiger.com/news/list?symbols={symbols}&pageCount={page_count}".format(symbols=','.join(parms['symbols']).strip(),page_count=int(pageCount)+1)
            yield scrapy.Request(changePageUrl,
                                  callback=self.parse)