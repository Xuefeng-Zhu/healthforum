#!/usr/bin/python
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
	print "Found drug {0} with drug id {1}".format(drugName, drug_id)
	return drug_id

#def getSideEffectId(sideEffect, drug_id):
#	queryString = "select id from side_effects where drug_id={0} and doctor_effect='{1}'".format(drug_id, sideEffect)
#	print "Querystring: " + queryString
#	cursor.execute(queryString)
#	side_effect_id = cursor.fetchone()[0]
#	return side_effect_id
#
def insertPost(post, drug_id, effect):
	queryString = "insert into side_effects_details(url, title, forum_id, content, drug_id, general_effect) values (\"{0}\", \"{1}\", {2}, \"{3}\", {4}, \"{5}\")" \
					.format(post["url"].encode("utf-8"), post["title"].encode("utf-8"), post["forumId"], post["content"].encode("utf-8"), drug_id, effect.encode("utf-8"))
	cursor.execute(queryString)


numInserted = 0

for i, obj in enumerate(dataList):
	try:
		drugName = obj["drugName"]
		drug_id = getDrugId(drugName);
			
		retrievedObjects = obj["retrievedObjects"]
		for post in retrievedObjects:
			insertPost(post, drug_id, obj["sideEffect"])
			numInserted += 1
		db.commit()
		
	except Exception as e:
		print "Received an error with item number {0}, drug name {1} and side effect {2}".format(i, obj["drugName"], obj["sideEffect"])
		continue

"""
for data in data_dict:

	try:

		side_effect = data['sideEffect']
		isDr = data['isDrSERes']
		
		
		updateSEDId = "INSERT INTO side_effects_details(side_effects_id) SELECT id FROM side_effects WHERE patient_effect=" \
							+ quote(side_effect) + ";"
		cursor.execute(updateSEDId)

		updateSED = "INSERT INTO side_effects_details(effect, isDrSERes) VALUES (" 
							+ quote(side_effect) + "," + quote(isDr)  
							+ ") FROM side_effects WHERE patient_effect = " + quote(side_effect) + ";"
		cursor.execute(updateSED)


		for se in enumerate(data['retrievedObjects']):

			try:

				forumComments = se[0]['content']
				forumTitle = se[0]['title']
				forumId = se[0]['forum_id']

				updateSEDContent = "INSERT INTO side_effects_details(content,title,forum_id) VALUES(" + quote(forumComments) + "," + quote(forumTitle) + "," + quote(forumId) + ") FROM side_effects WHERE patient_effect=" + quote(side_effect) + ";"
				cursor.execute(updateSEDContent)

			except:
				e = sys.exc_info()
				print "Error: ? ", e

		db.commit()
	except:
		e = sys.exc_info()
		print "Error: ? ", e
		db.rollback()
		"""
