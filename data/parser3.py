#!/usr/bin/python
import json
import MySQLdb

data = json.load(open("crawler/descriptions.json"))

# When testing
if True:
	db = MySQLdb.connect(host="engr-cpanel-mysql.engr.illinois.edu",
						 user="halin2_guest",
						 passwd="helloworld",
						 db="halin2_sample")

# For the actual server
else:
	db = MySQLdb.connect(host = "us-cdbr-east-05.cleardb.net",
						user = "bbe6abd0b555dc",
						passwd = "488c7e4d",
						db = "heroku_5f9923672d3888a")
cursor = db.cursor()

def quote(string):
	return '\"' + str(string) + '\"'

for drugname in data:
	try:
		updateDrug = "UPDATE drugs SET drugs.info = " + quote(data[drugname]) + " WHERE drugs.name = " + quote(drugname)
		cursor.execute(updateDrug)
		db.commit()
	except:
		print "Error: Unable to update the drug " + drugname + " into the database."
		db.rollback()
			
