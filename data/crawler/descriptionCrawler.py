#!/usr/bin/python
from bs4 import BeautifulSoup	
import requests
import os


def drugList():
	f1=open('drugList.txt', 'w')
	with open('drugs2.txt','r') as f2:
		for line in f2:
			if ":" in line:
				drug_name = line.split(' ')[2].replace(":","")
				f1.write(drug_name+"\n")
		f1.close()

def isValid(dname):
	dname=str(dname)
	url="http://www.drugs.com/%s.html"%(dname).strip()
	r=requests.get(url)
	data=r.text
	soup=BeautifulSoup(data)
	line= soup.title.string
	line2= soup.find(itemprop="description")
	if "Page Not Found" in line:
		return False
	if line2 is None:
		return False
	else:
		return True
def isValidMTM(dname):
	dname=str(dname)
	url="http://www.drugs.com/mtm/%s.html"%(dname).strip()
	r=requests.get(url)
	data=r.text
	soup=BeautifulSoup(data)
	line= soup.title.string
	line2= soup.find(itemprop="description")
	if "Page Not Found" in line:
		return False
	if line2 is None:
		return False
	else:
		return True

def desCrawl():
	script_dir=os.path.dirname(os.path.abspath(__file__))
	dest_file = os.path.join(script_dir, 'descriptions')
	f3=open("notFound.txt","w")
	drug_desc={}
	drug_link={}
	with open("drugList.txt", "r") as f1:
		for line in f1:
			if isValid(line):
				url="http://www.drugs.com/%s.html"%(line).strip()
				print url
				drug_link[line]=url
				r=requests.get(url)
				data=r.text
				soup=BeautifulSoup(data)
				file_name="%s.txt"%(line)
				path=os.path.join(dest_file,file_name)
				f2=open(path,"w")
				drug_desc[line.strip("\n")]=str(soup.find(itemprop="description").string)
				f2.write(str(soup.find(itemprop="description").string))
				f2.close()
			elif isValidMTM(line):
				url="http://www.drugs.com/mtm/%s.html"%(line).strip()
				print url
				drug_link[line]=url
				r=requests.get(url)
				data=r.text
				soup=BeautifulSoup(data)
				file_name="%s.txt"%(line)
				path=os.path.join(dest_file,file_name)
				f2=open(path,"w")
				drug_desc[line.strip("\n")]=str(soup.find(itemprop="description").string)
				f2.write(str(soup.find(itemprop="description").string))
				f2.close()
			elif isValidMTM(line):
				url="http://www.drugs.com/mtm/%s.html"%(line).strip()
				print url
				drug_link[line]=url
				r=requests.get(url)
				data=r.text
				soup=BeautifulSoup(data)
				file_name="%s.txt"%(line)
				path=os.path.join(dest_file,file_name)
				f2=open(path,"w")
				f2.write(str(soup.find(itemprop="description").string))
				f2.close()
			else:
				f3.write(line)
	f3.close()
	return {"descriptions": drug_desc, "links": drug_link}


