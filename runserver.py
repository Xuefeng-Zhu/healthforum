#!/usr/bin/python
from healthcode import app
from flask import Flask
from flask.ext import restful
from flask.ext.restful import (reqparse, abort, fields, marshal_with, marshal)

app = Flask(__name__)
api = restful.Api(app)

DRUGS = [
	{ 'drug': 'drug a', 'drug a side effects': {'side effect': 'side effect a1', 'side effect': 'side effect a2' }},
	{ 'drug': 'drug b', 'drug b side effects': {'side effect': 'side effect b1', 'side effect': 'side effect b2' }},
	{ 'drug': 'drug c', 'drug c side effects': {'side effect': 'side effect c1', 'side effect': 'side effect c2' }}
]

#only output the .task. field
fields = {
	'drug': fields.String
}

# Drug
#   show a single drug item and lets you delete them
class Drug(restful.Resource):
	@marshal_with(fields)
	def get(self, drug_id):
		if not(len(DRUGS) > drug_id > 0) or DRUGS[drug_id] is None:
			abort(404, message="Drug {} doesn't exist".format(drug_id))
		return DRUGS[drug_id]

	def delete(self, drug_id):
		if not(len(DRUGS) > drug_id > 0):
			abort(404, message="Drug {} doesn't exist".format(drug_id))
		DRUGS[drug_id] = None
		return "", 204

# DrugList
#   shows a list of all drugs, and lets you POST to add new drugs
parser = reqparse.RequestParser()
parser.add_argument('drug', type=str)

class DrugList(restful.Resource):
	@marshal_with(fields)
	def get(self):
		return DRUGS

	def post(self):
		args = parser.parse_args()
		task = {'drug': args['drug']}
		DRUGS.append(task)
		return marshal(task, fields), 201

## Actually setup the Api resource routing here
api.add_resource(DrugList, '/drug')
api.add_resource(Drug, '/drug/<int:drug_id>')

if __name__ == '__main__':
	app.run(debug=True)
