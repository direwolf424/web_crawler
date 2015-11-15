import requests
import sys
import re
import os
from bs4 import BeautifulSoup
from queue import *
from urllib.parse import urlparse
import urllib.request as urllib2

# for searching and downloading the photo to phot folder
image = 0

def image_search(soup):
    global image
    for link in soup.find_all('img'):
        check_photo = link.get('src')
        check = re.search('/userphoto/',check_photo)
        if check is not None :
            username = re.search('title/(.+?)/photo.jpg',check_photo)
            username = username.group(1)
            img = urllib2.urlopen(check_photo)
            localfile = open(os.getcwd()+'/photo/'+username+'.jpg' , 'wb')
            localfile.write(img.read())
            localfile.close()
            print(username +' '+str(image))
            image += 1

    return


def func(q,url,url_list,count):
    q.put(url)
    cntr = 0
    level = 0
    while not q.empty():
        url = q.get()
        html = requests.get(url)
        html.encoding = 'utf-8'
        html = html.content
        soup = BeautifulSoup(html ,'html.parser')
        url1 = urlparse(url)
        netloc = url1.netloc
        scheme = url1.scheme
        image_search(soup)  # for searching
        for link in soup.find_all('a'):
            s= link.get('href')
            parsed = urlparse(s)
            s_check = url_list.get(s)
            if type(s_check) == int:          #checking if url is visited
                continue


            url_list[urlparse(s).path]=level

            s_regex = re.search('/profile/',s)
            s_regex1 = re.search('/ratings/page/',s)


            if s_regex is None and s_regex1 is None:
                continue

            print(s)
            if cntr >= count:
                break
            if len(parsed.netloc) != 0 :
                q.put(s)
                cntr+=1
            else:                   #for relative path
                if type(s) == str:
                    if s[0]=='/':
                        q.put(scheme +'://'+ netloc + s)
                        cntr+=1

        level += 1
        url = q.get()
        if cntr >= count:
            break



def main():
    q = Queue(maxsize=0)
    url_list = {}
    #url = input('enter the url to scrape')
    url='http://codeforces.com/profile/tourist'
    url_list[urlparse(url).path]=0
    #count = input('enter the number of pages to visit')
    count=1000
    count = int(count)
    func(q,url,url_list,count)
    print('-----------------------------links visited-------------------------------------')
    for links in url_list.keys():
        print(url_list[links])



if __name__ == "__main__":
    main()