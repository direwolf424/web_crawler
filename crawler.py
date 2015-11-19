import requests
import sys
import re
import os
from bs4 import BeautifulSoup
from queue import *
from urllib.parse import urlparse
import urllib.request as urllib2
import time                                 # for calculating time 

image = 0

# for searching and downloading the photo to photo folder
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


def func(q , url , url_list ,count , start , total_time):
    q.put(url)
    cntr = 0
    level = 0
    while not q.empty():
        url = q.get()
        html = requests.get(url)
        html.encoding = 'utf-8'
        html = html.content
        print(url + str(cntr))
        soup = BeautifulSoup(html ,'html.parser')
        url1 = urlparse(url)
        netloc = url1.netloc
        scheme = url1.scheme
        #f_write = open(netloc+url1.path+'.html','wb')
        f_write = open('page'+str(cntr),'wb')
        f_write.write(html)
        f_write.close()
        if cntr >= count or (time.time() - start) >=total_time :
            return
        cntr+=1
        for link in soup.find_all('a'):
            s= link.get('href')
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
    url=input('enter the page to start')# the ranking page of codeforces
    url_list[url]=0
    count = input('enter the number of pages to visit')
    count = int(count)
    total_time = input('enter the time in second')
    total_time = int(total_time)
    start = time.time()
    func(q , url , url_list , count , start , total_time)
    #print('-----------------------------links visited-------------------------------------')
    #for links in url_list.keys():
        #print(links)

if __name__ == "__main__":
    main()
