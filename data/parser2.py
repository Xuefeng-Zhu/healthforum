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
				drugs_doct[drug_name] = None 
				drugs_pat[drug_name] = None
		elif ctr==2:
			ctr+=1
			drugs_doct[drug_name] = shlex.split(line)
		elif ctr==3:
			ctr=1;
			drugs_pat[drug_name] = shlex.split(line)


# When testing
if False:
	db = MySQLdb.connect(host="engr-cpanel-mysql.engr.illinois.edu",
						 user="halin2_guest",
						 passwd="helloworld",
						 db="halin2_sample")

 For the actual server
else:
	db = MySQLdb.connect(host = "us-cdbr-east-05.cleardb.net",
						user = "bbe6abd0b555dc",
						passwd = "488c7e4d",
						db = "heroku_5f9923672d3888a")

# Side effects are now arranged in two dictionaries:
# drugs_doct and drugs_pat. All we need to do now is
# iterate through the drugs, and add the respective
# arrays to the database

cursor = db.cursor()

def quote(string):
	return '\"' + str(string) + '\"'

for drug in drugs_doct:
	try:
		drugInsert = "INSERT INTO drugs (name) VALUES (\"{0}\")".format(drug)
		cursor.execute(drugInsert)
		drug_id = cursor.lastrowid
		doctor = drugs_doct[drug]
		patient = drugs_pat[drug]
		for i in range(0, 15):
			effectInsert = "INSERT INTO side_effects (drug_id, patient_effect, doctor_effect) \
							VALUES (" + quote(drug_id) + ", " + quote(patient[i]) + ", " + quote(doctor[i]) + ")"
			cursor.execute(effectInsert)
		db.commit()
	except:
		print "Error: Unable to put the drug " + drug + " into the database."
		db.rollback()
			
