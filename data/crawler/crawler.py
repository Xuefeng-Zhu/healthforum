#!/usr/bin/python

from bs4 import BeautifulSoup
import requests
import json
from descriptionCrawler import isValid
from descriptionCrawler import desCrawl
from descriptionCrawler import drugList





'''
name="macrolide"


url="http://www.drugs.com/dict/%s.html"%(name).strip()
print url
r=requests.get(url)
data=r.text
soup=BeautifulSoup(data)
print(soup.prettify())
#print soup.title.string
print soup.findall("Definition")

#desCrawl()
'''

desCrawl()
f=open('description_json.txt', 'w')
descriptions=desCrawl()
f.write(json.dumps(descriptions))
f.close()

