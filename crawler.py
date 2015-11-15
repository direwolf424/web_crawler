import requests
import sys
import re
from bs4 import BeautifulSoup
from queue import *
from urllib.parse import urlparse

# for searching and downloading the photo to phot folder




def func(q,url,url_list,count):
    q.put(url)
    cntr = 0
    level = 0
    while not q.empty():
        url = q.get()
        check_key = url_list.get(url)
        if type(check_key) == str:
            continue
        url_list[url] = level
        html = requests.get(url)
        print(url)
        html.encoding = 'utf-8'
        html = html.content
        soup = BeautifulSoup(html,'html.parser')
        url1 = urlparse(url)
        netloc = url1.netloc
        scheme = url1.scheme
        for link in soup.find_all('a'):
            s= link.get('href')
            parsed = urlparse(s)

            if cntr >= count:
                break
            if len(parsed.netloc) != 0 :
                q.put(s)
                cntr+=1
                print(s)
            else:                   #for relative path
                if type(s) == str:
                    if s[0]=='/':
                        q.put(scheme +'://'+ netloc + s)
                        cntr+=1
                        print(scheme + '://' + netloc + s)
        level += 1
        url = q.get()
        if cntr >= count:
            break


def main():
    q = Queue(maxsize=0)
    url_list = {}
    url = input('enter the url to scrape')
    count = input('enter the number of pages to visit')
    count = int(count)
    func(q,url,url_list,count)
    print('-----------------------------links visited-------------------------------------')
    for links in url_list.keys():
        print(url_list[links])



if __name__ == "__main__":
    main()




