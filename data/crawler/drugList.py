#!/usr/bin/python

def drugList():
	f1=open('drugList.txt', 'w')
	with open('drugs2.txt','r') as f2:
		for line in f2:
			if ":" in line:
				drug_name = line.split(' ')[2].replace(":","")
				f1.write(drug_name+"\n")
		f1.close()

