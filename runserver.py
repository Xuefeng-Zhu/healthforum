#!/usr/bin/python
from healthcode import app
from flask import Flask, jsonify
from flask import request
from flask.ext.restful import Api, Resource

app = Flask(__name__)
api = Api(app)

# TODO handle request to GET single drug resource by drug_name
# TODO return json containing list of side effects and associated data
class DrugAPI(Resource):
	def get(self, id):
		return self.response

	# TODO: Is this supposed to be a classmethod?
	def make_api(cls, response):
		cls.response = response
		return cls


class HealthforumApp():
	def __init__(self):
		self.app = Flask()
		app_api = Api(self.app)
		SideEffectsApi = DrugAPI.make_api({"key": "value"})
		app_api.add_resource(DrugApi, "/drug/<string:drug_name>", endpoint = 'drug')

	def run(self):
		self.app.run("0.0.0.0", 80, debug = True) # remove debug when putting in production


HealthforumApp().run()
