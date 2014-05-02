#!/usr/bin/python
import json
import MySQLdb

"""
Imports the drug descriptions into the database.
"""


data = json.load(open("crawler/descriptions.json"))

# When testing
if True:
	db = MySQLdb.connect(host = "engr-cpanel-mysql.engr.illinois.edu",
						user="halin2_guest",
						passwd="helloworld",
						db = "halin2_test")

# When not testing
else:
	db = MySQLdb.connect(host="engr-cpanel-mysql.engr.illinois.edu",
						user="halin2_guest",
						passwd="helloworld",
						db="halin2_sample")
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
			
