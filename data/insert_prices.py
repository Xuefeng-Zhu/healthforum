#!/usr/bin/python
import json
import MySQLdb


data = json.load(open("prices.json"))

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

for key in data:
    try:
        updateDrug = "UPDATE drugs SET drugs.price = " + data[key] \
			+ " WHERE drugs.name = " + quote(key)
        cursor.execute(updateDrug)
        db.commit()
    except:
        print "Error: Unable to update the drug " + key + " into the database."
        db.rollback()

