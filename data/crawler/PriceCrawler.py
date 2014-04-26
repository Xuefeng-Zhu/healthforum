#!/usr/bin/python
from bs4 import BeautifulSoup	
import requests
import os

def priceCrawl():
	script_dir=os.path.dirname(os.path.abspath(__file__))
	dest_file = os.path.join(script_dir, 'prices')
	drug_price={}
	f3=open("notFoundPrice.txt","w")
	with open("drugList.txt", "r") as f1:
		for line in f1:
			url="http://www.drugs.com/price-guide/%s"%(line).strip()
			print url
			r=requests.get(url)
			data=r.text
			soup=BeautifulSoup(data)
			sbody=soup.body
			file_name="%s.txt"%(line)
			path=os.path.join(dest_file,file_name)
			f2=open(path,"w")
			dstring=[]
			for string in sbody.stripped_strings:
				if "$" in string:
					try:
						dstring.append(str(string))
					except:
						continue
			dstring.pop(0)
			print line
			if 'jQuery' in dstring[0]:
				f2.write('None')
				drug_price[line.strip('\n')]="None"
			elif "$" in dstring[0]:
				f2.write(dstring[0]+"\n")
				drug_price[line.strip('\n')]=dstring[0]
				f2.write(url)
			else:
				f3.write(line)
			f2.close()
	f3.close()
	return drug_price
	


