#!/usr/bin/python

from bs4 import BeautifulSoup
import requests
import json
import re
from descriptionCrawler import desCrawl
from PriceCrawler import priceCrawl

drugs=desCrawl()
drugs_links=drugs['links']
drugs_description=drugs['descriptions']
print drugs_links
print drugs_description

#priceCrawl()