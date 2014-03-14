#!/usr/bin/python
import MySQLdb

db = MySQLdb.connect(host="127.0.0.1",
                     user="root",
                     passwd="password",
                     db="cs410")
"""
cur = db.cursor() 
cur.execute("SELECT * FROM drugs")


for row in cur.fetchall():
    print "%s %s" % (row[0], row[1])

"""
#-------

"""
cur = db.cursor()
cur.execute("SELECT name, side_effect FROM drugs, side_effects WHERE id = drug_id")
for row in cur.fetchall():
    print "%s %s" % (row[0], row[1])
"""

#Parsing the Forum Drug Side Effects
drugs={}
with open('drugs.txt','r') as f:
	for line in f:
		if "topic" in line:
			drug_name = line.split(' ')[2]
			if drug_name not in drugs.keys():
				drugs[drug_name] = []
		else:
			drugs[drug_name].extend(line.strip().replace('"','').split(' '))

#Storing into Database
cur=db.cursor()
for key in drugs.keys():
	try:
		query = "INSERT INTO drugs (name) VALUES (\"%s\")" % (key)
		cur.execute(query)
		get_drug_id = "SELECT id from drugs WHERE name = \"%s\"" % (key)
		cur.execute(get_drug_id)
		for row in cur.fetchall():
			drug_id = row[0]
		for side_effect in drugs[key]:
			val= "INSERT INTO side_effects (id, side_effect) VALUES (\"%d\", \"%s\")" % (drug_id, side_effect)
			cur.execute(val)
		db.commit()
	except:
		db.rollback()
db.close()
