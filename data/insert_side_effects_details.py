#!/usr/bin/python
import sys
import json
import MySQLdb

"""
Imports the drug side effects details into the database.
"""

data_dict = json.load(open("topic_good_drugSideEffects.json"))

# When testing
db = MySQLdb.connect(host = "engr-cpanel-mysql.engr.illinois.edu",
                                        user="halin2_guest",
                                        passwd="helloworld",
                                        db = "halin2_test")

# When not testing
#db = MySQLdb.connect(host="engr-cpanel-mysql.engr.illinois.edu",
#                                       user="halin2_guest",
#                                       passwd="helloworld",
#                                       db="halin2_sample")

cursor = db.cursor()

def quote(string):
	return '\"' + str(string) + '\"'


"""
	data =  [{
		"drugName":"some drug",
		"sideEffect":"some side effect",
		"isDrSERes":"True/False"
		"retrievedObjects":
			[
				{
					"url":"http://www.some.url_1.om",
					"forumId":"1",
					"title":"some title_1",
					"content":"content_1"
				}
				{
					"url":"http://www.some.url_2.om",
					"forumId":"2",
					"title":"some title_2",
					"content":"content_2"
				}				
			]
		}]
"""


for data in data_dict:

	try:

		side_effect = data['sideEffect']
		isDr = data['isDrSERes']

		updateSEDId = "INSERT INTO side_effects_details(side_effects_id) SELECT id FROM side_effects WHERE patient_effect=" + quote(side_effect) + ";"
		cursor.execute(updateSEDId)

		updateSED = "INSERT INTO side_effects_details(effect,isDrSERes) VALUES (" + quote(side_effect) + "," + quote(isDr)  + ") FROM side_effects WHERE patient_effect = " + quote(side_effect) + ";"
		cursor.execute(updateSED)


		for se in enumerate(data['retrievedObjects'])

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
