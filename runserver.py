#!/usr/bin/python
from healthcode import app
from flask import Flask
from flask.ext import restful
from flask.ext.restful import reqparse, abort, fields, marshal_with, marshal
from flask.ext.restful.utils import cors

"""
More information about Flask RESTful:
http://flask-restful.readthedocs.org/en/latest/installation.html

More documentation on cors (cross origin resource sharing):
https://github.com/twilio/flask-restful/pull/131

More information on argument passing:
http://flask-restful.readthedocs.org/en/latest/reqparse.html
"""

app = Flask(__name__)
api = restful.Api(app)
api.decorators=[cors.crossdomain(origin='*')]

# Note this is a list of dictionaries.
# Each dictionary has
# 1. A string called "name"
# 2. A list of side effects (strings) called "side effects"
drugsTable = [
	{ 'name': 'oxygen', 'side effects': ['side effect a1', 'side effect a2']},
	{ 'name': 'humira', 'side effects': ['nausea', 'death']},
	{ 'name': 'mcdonalds', 'side effects': ['irregular sleep habits', 'hysteria', 'uncontrollable shivering', 'vomiting', 'gaining weight']}
]

# Generic function that aborts the call if the
# queried index is not in the input list
def assertInList(inputList, index):
	if not(len(inputList) > index >= 0) or inputList[index] is None:
		abort(404, message = "ERROR! Item doesn't exist in table.")

# Drug
# show a single drug item and lets you delete them
class Drug(restful.Resource):

	# $ curl localhost:5000/drugs/2
	def get(self, drugNum):
		assertInList(drugsTable, drugNum)	
		return drugsTable[drugNum]

	# $ curl localhost:5000/drugs/1 -X DELETE
	def delete(self, drugNum):
		assertInList(drugsTable, drugNum)	
		drugsTable[drugNum] = None
		return "Successfully killed.", 204

api.add_resource(Drug, '/drugs/<int:drugNum>')


# Allows the input URI to be parsed
# We can theoretically use this for the above class, but we didn't
parser = reqparse.RequestParser()
parser.add_argument('name', type = str)
parser.add_argument('side_effects', type = str, action = "append")	# Creates array

# DrugList
# shows a list of all drugs, and lets you POST to add new drugs
class DrugList(restful.Resource):

	# Gets the current list
	# $ curl localhost:5000/drugs
	def get(self):
		return drugsTable

	# Adding a new drug and side effects list
	# $ curl http://localhost:5000/drugs -d "name=advil" -d "side_effect=nausea" -d "side_effect=dying" -X POST -v
	# Interesting note: When formulating your post request, don't have a space before
	def post(self):

		# Parse the arguments from the post request
		args = parser.parse_args()
		name = args["name"]				# name = "advil"
		effects = args["side_effect"] 	# effects = ["nausea", "dying"] 
	
		# Create the dictionary that we're going to put into the table
		drugDict = dict()
		drugDict["name"] = name
		drugDict["side effects"] = effects

		# Add this to the table and send its index to the client
		drugsTable.append(drugDict)
		drugNum = len(drugsTable) - 1
		return drugNum, 201

## Actually setup the Api resource routing here
api.add_resource(DrugList, '/drugs')

if __name__ == '__main__':
	app.run(debug=True)
