#!/usr/bin/python
import MySQLdb
import json

db = MySQLdb.connect(host="127.0.0.1",
                     user="root",
                     passwd="password",
                     db="cs410")

drugName=input("Type a name of drug: ")


name = db.cursor() 
name.execute("SELECT * FROM drugs where name=\"%s\""%drugName)
for row in name.fetchall():
    drugid=row[0]
    #print "%s" % (row[1])
#print drugid
side_effect=[]
effect=db.cursor()
effect.execute("SELECT * FROM side_effects where id=\"%d\""%drugid)
for row in effect.fetchall():
	side_effect.append(row[1])

drugDictionary={"Drug": drugName , "SideEffects": side_effect}

#print drugDictionary

print json.dumps(drugDictionary)