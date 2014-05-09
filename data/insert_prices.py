#!/usr/bin/python
from math import ceil
import json
import MySQLdb


data = json.load(open("prices.json"))

# When testing
if False:
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

for key in data:
	if data[key] != "None":
		priceStr = data[key].replace("$", "").split(".")[0]
		updateDrug = "UPDATE drugs SET drugs.price = {0} WHERE drugs.name = ".format(priceStr) + quote(key)
		cursor.execute(updateDrug)
		db.commit()

