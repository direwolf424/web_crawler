#!/bin/env python


import requests
import re
from queue import *
from urllib.parse import urlparse
import urllib.request as urllib2
import time                                 # for calculating time 

def extract_href(html):
    list_href = re.findall('<a(.+?)href="(.+?)"',html)
    return list_href


def func(q , url , url_list ,count , start , total_time):
    q.put(url)
    cntr = 1
    level = 0
    while not q.empty():
        url = q.get()
        html = requests.get(url)
        soup = extract_href(html.text)   #calling the regex function to extarct the href attribute  
        html.encoding = 'utf-8'
        html = html.content
        print(str(cntr) + ' --> ' +url)
        url1 = urlparse(url)
        netloc = url1.netloc
        scheme = url1.scheme
        f_write = open('page'+str(cntr)+'.html','wb')
        f_write.write(html)
        f_write.close()
        if cntr >= count or (time.time() - start) >=total_time :
            return
        cntr+=1
        for link in soup:
            s= link[1]
            parsed = urlparse(s)
            s_check = url_list.get(s)
            if type(s_check) == int:          #checking if url is visited
                continue
            if (time.time() - start) >= total_time:
                return


            url_list[scheme +'://'+ netloc + '/' + parsed.path]=level


          #  print(s)
            if len(parsed.netloc) != 0 :
                q.put(s)
            else:                   #for relative path
                if type(s) == str:
                    if s[0]=='/':
                        q.put(scheme +'://'+ netloc + s)

        level += 1
        url = q.get()

def main():
    q = Queue(maxsize=0)
    url_list = {}
    url=input('enter the page to start---->')# the ranking page of codeforces
    url_list[url]=0
    count = input('enter the number of pages to visit---->')
    count = int(count)
    total_time = input('enter the time in second---->')
    total_time = int(total_time)
    start = time.time()
    print('Please wait while the contents are being downloaded and written as page(1-n).html in your current directory\n')
    func(q , url , url_list , count , start , total_time)

if __name__ == "__main__":
    main()
