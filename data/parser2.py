#!/usr/bin/python

import MySQLdb
import shlex


drugs_doct={}
drugs_pat={}
ctr=1
with open('drugs2.txt','r') as f:
	for line in f:
		if ":" in line:
			ctr+=1
			drug_name = line.split(' ')[2].replace(":","")
			if drug_name not in drugs_doct.keys() or drugs_pat:
				drugs_doct[drug_name] = []
				drugs_pat[drug_name] = []
		elif ctr==2:
			ctr+=1
			drugs_doct[drug_name].extend(shlex.split(line))
		elif ctr==3:
			ctr=1;
			drugs_pat[drug_name].extend(shlex.split(line))

#prints the 2nd line with doctor terms
print drugs_doct
#prints the 3rd line with patient terms
print drugs_pat