#!/usr/bin/python

from bs4 import BeautifulSoup
import requests
from descriptionCrawler import isValid
from descriptionCrawler import desCrawl
from descriptionCrawler import drugList





'''
name="alcohol"


url="http://www.drugs.com/%s.html"%(name).strip()
print url
r=requests.get(url)
data=r.text
soup=BeautifulSoup(data)
#print(soup.prettify())
#print soup.title.string
print soup.find(itemprop="description").string

'''

desCrawl()
