#!/bin/env python


import requests
import re
from queue import *
from urllib.parse import urlparse
import urllib.request as urllib2
import time                                               # for calculating time 

def extract_href(html):                                   # function to extract links using regex
    list_href = re.findall('<a(.+?)href="(.+?)"',html)
    return list_href


def func(q , url , url_list ,count , start , total_time): # scraper function
    q.put(url)                                            # push starting url into queue
    cntr = 1                                   
    level = 0
    while not q.empty():                                   
        url = q.get()                                     # pop url from queue
        try:
            html = requests.get(url,timeout=1)            # get webpage using request 
        except requests.exceptions.RequestException as err:   #handling error 
            q.get()
            continue
        soup = extract_href(html.text)   #                # call extract_href function 
        html.encoding = 'utf-8'               
        html = html.content                              
        print(str(cntr) + ' --> ' +url)                   # print counter with url visited
        url1 = urlparse(url)                              
        netloc = url1.netloc
        scheme = url1.scheme
        f_write = open('page'+str(cntr)+'.html','wb')   
        f_write.write(html)                               # write the source code of webpage into a file
        f_write.close()
        if cntr >= count or (time.time() - start) >=total_time :          # conter and timer conditions to terminate crawler
            return
        cntr+=1
        for link in soup:
            s= link[1]
            parsed = urlparse(s)
            s_check = url_list.get(s)
            if type(s_check) == int:                                       #  checking if url is visited
                continue
            if (time.time() - start) >= total_time:
                return
            
            url_list[scheme +'://'+ netloc + '/' + parsed.path]=level      # add url of downloaded page to the dictionary

            if len(parsed.netloc) != 0 :                                   # if not a relative path push into the queue
                q.put(s)
            else:                  
                if type(s) == str:
                    if s[0]=='/':
                        q.put(scheme +'://'+ netloc + s)                  # make the path absolute and push into the queue 

        level += 1
        url = q.get()

def main():                                                     # main function
    q = Queue(maxsize=0)                                        # initialis queue
    url_list = {}                                               # dictionary to keep track of visited urls
    url=input('enter the page to start : ')                     # url to start scraping from
    url_list[url]=0     
    count = input('enter the number of pages to visit : ')      # no. of pages to download content of 
    count = int(count)
    total_time = input('enter the time in second : ')           # seconds the scraping should continue till
    total_time = int(total_time)      
    start = time.time()                                         # start time noted
    print('Please wait while the contents are being downloaded and written as page(1-n).html in your current directory\n')
    func(q , url , url_list , count , start , total_time)       # scraper function

if __name__ == "__main__":
    main()
