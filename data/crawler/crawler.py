#!/usr/bin/python

from bs4 import BeautifulSoup
from descriptionCrawler import desCrawl
from PriceCrawler import priceCrawl
import requests
import json


drugs=desCrawl()
drugs_links=drugs['links']
drugs_description=drugs['descriptions']
drug_price=priceCrawl()

f1=open("drugs_description.txt","w")
f2=open("drugs_links.txt","w")
f3=open("drugs_price.txt","w")
f1.write(json.dumps(drugs_description))
f2.write(json.dumps(drugs_links))
f3.write(json.dumps(drug_price))







