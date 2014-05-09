#!/usr/bin/python
from colorama import *
import sys
import json
import MySQLdb

"""
Imports the drug side effects details into the database.
"""

dataList = json.load(open("forum_relations.json"))

# When testing
#db = MySQLdb.connect(host = "engr-cpanel-mysql.engr.illinois.edu",
#                                        user="halin2_guest",
#                                        passwd="helloworld",
#                                        db = "halin2_test")
#
# When not testing
db = MySQLdb.connect(host="engr-cpanel-mysql.engr.illinois.edu",
                                       user="halin2_guest",
                                       passwd="helloworld",
                                       db="halin2_sample")

cursor = db.cursor()

def quote(string):
	return '\"' + str(string) + '\"'

# Gets the drug's name from the database
def getDrugId(drugName):
	
	queryString = "select id from drugs where name='" + drugName + "'"
	cursor.execute(queryString)
	drug_id = cursor.fetchone()[0]
	return drug_id

#def getSideEffectId(sideEffect, drug_id):
#	queryString = "select id from side_effects where drug_id={0} and doctor_effect='{1}'".format(drug_id, sideEffect)
#	print "Querystring: " + queryString
#	cursor.execute(queryString)
#	side_effect_id = cursor.fetchone()[0]
#	return side_effect_id
#
def insertPost(post, drug_id, sideEffectId):
	if post["forumId"] is None or post["forumId"] == "":
		post["forumId"] = -1

	queryString = "insert into side_effects_details(url, title, forum_id, content, side_effect_id) values (\"{0}\", \"{1}\", {2}, \"{3}\", {4})" \
					.format(post["url"].encode("utf-8"), post["title"].encode("utf-8"), post["forumId"], post["content"].encode("utf-8"), sideEffectId)
	try:
		cursor.execute(queryString)
	except Exception as e:
		print "Error inserting post for the following query:"
		print queryString
		print "Error message: "+ str(e.message)
		print ""

def getSideEffectId(drug_id, sideEffectName, isDoctor):
	effect = "doctor_effect" if isDoctor else "patient_effect"
	queryString = "select id from side_effects where {0} = '{1}' and drug_id = {2}".format(effect, sideEffectName, drug_id)
	try:
		cursor.execute(queryString)
		side_effect_id = cursor.fetchone()[0]
		return side_effect_id
	except Exception as e:
		print "Error getting the side effect ID for the following query:"
		print queryString
		print "Error message: " + str(e.message) 
		print ""
		return None



numInserted = 0

for i, obj in enumerate(dataList):
	drugName = obj["drugName"]
	drug_id = getDrugId(drugName);

	sideEffectName = obj["sideEffect"]
	isDoctor = obj["isDrSERes"]
	sideEffectId = getSideEffectId(drug_id, sideEffectName, isDoctor)
	if sideEffectId is None:
		continue
		
	retrievedObjects = obj["retrievedObjects"]
	for post in retrievedObjects:
		insertPost(post, drug_id, sideEffectId)
		numInserted += 1
	db.commit()
		

print str(numInserted) + " rows inserted."

