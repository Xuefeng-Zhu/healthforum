#!/usr/bin/python

import MySQLdb
import shlex

db = MySQLdb.connect(host="engr-cpanel-mysql.engr.illinois.edu",
                     user="halin2_guest",
                     passwd="helloworld",
                     db="halin2_sample")

#Parsing the Forum Drug Side Effects
drugs={}
with open('drugs.txt','r') as f:
	for line in f:
		if "topic" in line:
			drug_name = line.split(' ')[2]
			if drug_name not in drugs.keys():
				drugs[drug_name] = []
		else:
			drugs[drug_name].extend(shlex.split(line))

print drugs;


#Storing into Database
cur=db.cursor()
for key in drugs.keys():
#try:
	query = "INSERT INTO drugs (name) VALUES (\"%s\")" % (key)
	cur.execute(query)
	get_drug_id = "SELECT id from drugs WHERE name = \"%s\"" % (key)
	cur.execute(get_drug_id)
	for row in cur.fetchall():
		drug_id = row[0];
#drug_id = cur.fetchall()[0][0]
	for side_effect in drugs[key]:
		val= "INSERT INTO side_effects (drug_id, effect) VALUES (\"%d\", \"%s\")" % (drug_id, side_effect)
		cur.execute(val)
		db.commit()
#	except:
#		db.rollback()
#		print "Error: Unable to insert into database."
db.close()
