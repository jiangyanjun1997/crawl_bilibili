#coding:utf-8

"""
    描述: 爬虫(必应),根据搜索关键词爬取
    问题: 需要人工监控爬取图片是否是需要图片
"""

import os
import re
import time
import json
import urllib
import socket
import posixpath
import imghdr
import urllib.parse
import urllib.error
import urllib.request
from multiprocessing import Pool
import hashlib
import argparse
timeout = 5
socket.setdefaulttimeout(timeout)
# data_class = {'中国国旗':0,'美国国旗':1,'英国国旗':2,'法国国旗':3,'日本国旗':4,'韩国国旗':5,'德国国旗':6,'加拿大国旗':7,'意大利国旗':8,'俄国国旗':9,
#                 '习近平':'xijinping','李克强':'likeqiang','栗战书':'lizhanshu','汪洋':'wangyang'}

image_md5s = {}
class Crawler:
    __time_sleep = 0.1
    __amount = 0
    __start_amount = 0
    __counter = 0


    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    
    def __init__(self, t=0.1):
        self.time_sleep = t

    def __download(self,total_links_list,word):
        # if not os.path.exists("../" + str(word)):
        #     os.mkdir("../" + str(word))
        # self.__counter = len(os.listdir('../' + str(word))) + 1
        self.__counter = 1
        for link in total_links_list:
            command = 'youtube-dl ' + link
            os.system(command)
            # print('\n==> ',word,self.__counter,'ok')
            self.__counter += 1
            # break

    def __get_images(self, word,process_name):
        search = urllib.parse.quote(word)
        pn = self.__start_amount
        total_url_list = []
        page_num = 1
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        }
        
        while pn < self.__amount:
            # url = 'https://www.bing.com/images/async?q=' + search+ '&first=' + str(pn) + '&count=50' # default is 35 urls ,max is 150
            # url = 'https://www.bing.com/videos/search?q=' + search + '&first=' + str(pn)+ '&count=15'+ '&qft=+filterui:duration-short&FORM=VRFLTR'
            url = 'https://search.bilibili.com/all?keyword='+search+'&from_source=banner_search&order=totalrank&duration=1&tids_1=0'+'&page='+str(page_num)
            page_num += 1
            # print(url)
            time.sleep(self.time_sleep)
            req = urllib.request.Request(url, None, headers=self.headers)
            page = urllib.request.urlopen(req)
            rsp = page.read().decode('utf8')
            # print(rsp)
            # https://www.bilibili.com/video/av18629151
            # print(len(rsp.split('"arcurl":"')))
            for url_str in rsp.split('"arcurl":"')[1:]:
                av_id = url_str.split('","aid"')[0].split('\\u002F')[-1]
                # print(av_id)
                total_url_list.append('https://www.bilibili.com/video'+'/'+av_id)

            pn += 20
            page.close()
        print(len(total_url_list))
        # print(total_url_list)
        self.__download(total_url_list,word)
        return

    def start(self, word, spider_page_num=1, start_page=1,process_name='process'):
      
        self.__start_amount = (start_page - 1) * 20  
        self.__amount = spider_page_num * 20 + self.__start_amount
        self.__get_images(word,process_name)


def main():
    parser = argparse.ArgumentParser(description='Download')
    parser.add_argument('--num', default=2, type=float, help='leader num')
    args = parser.parse_args()
    crawler = Crawler(0.05)
    keyword_lines = open('./keywords.txt','r',encoding='utf-8').read().splitlines()
    keyword_list = []
    page_num = args.num
    start_page = 1
    num = 0
    for keyword in keyword_lines:
        print('\n==> Download start...\n')
        crawler.start(keyword,page_num,start_page,keyword)
    
        num += 1
    
    print("\n\n")
    print("===============================================")
    print('============All Download over!=================')
    print("===============================================")


if __name__ == '__main__':
    main()
