#!/usr/bin/python

from bs4 import BeautifulSoup
import requests
import json
import re
from descriptionCrawler import desCrawl
from PriceCrawler import priceCrawl

'''
name="xanax"


url="http://www.drugs.com/price-guide/%s"%(name).strip()
print url
r=requests.get(url)
data=r.text
soup=BeautifulSoup(data)
sbody=soup.body

dstring=[]
for string in sbody.stripped_strings:
	if "$" in string:
		try:
			dstring.append(str(string))
		except:
			continue

dstring.pop(0)
print dstring
'''

drugs=desCrawl()

priceCrawl()