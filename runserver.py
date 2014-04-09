#!/usr/bin/python
import json
from flask import Flask
from flask.ext import restful
from flask.ext.restful import reqparse, abort, fields, marshal_with, marshal
from flask.ext.restful.utils import cors
from database import db, Users, Drugs
from flask.ext.sqlalchemy import SQLAlchemy

"""
More information about Flask RESTful:
http://flask-restful.readthedocs.org/en/latest/installation.html

More documentation on cors (cross origin resource sharing):
https://github.com/twilio/flask-restful/pull/131

More information on argument passing:
http://flask-restful.readthedocs.org/en/latest/reqparse.html

For the brave souls: To push this server onto heroku,
https://devcenter.heroku.com/articles/getting-started-with-python

"""

herokuURI = 'mysql://bbe6adb0b555dc:488c7e4d@us-cdbr-east-05.cleardb.net/heroku_5f9923672d3888a'
henryURI = 'mysql://halin2_guest:helloworld@engr-cpanel-mysql.engr.illinois.edu/halin2_sample'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = henryURI
db = SQLAlchemy(app)

api = restful.Api(app)
api.decorators=[cors.crossdomain(origin='*')]

################################################
################################################

# Parsing documentation
# http://flask-restful.readthedocs.org/en/latest/api.html#module-reqparse
drug_parser = reqparse.RequestParser()
drug_parser.add_argument('name', type = str)
drug_parser.add_argument('info', type = str)

# Allows drug data to be pulled and pushed to/from the database
class Drug_resource(restful.Resource):

	# $ curl localhost:5000/drugs/2
	@marshal_with(Drugs.field())
	def get(self, drugNum):
		drug = Drugs.query.filter_by(id=drugNum).first()
		return drug 

	def post(self):
		args = drug_parser.parse_args()
		name = args['name']
		info = args['info']
		drug = Drugs(name, info)

		db.session.add(drug)
		db.session.commit()

		return drug.id


api.add_resource(Drug_resource, '/drugs', endpoint="drugs")
api.add_resource(Drug_resource, '/drugs/<int:drugNum>')
		
################################################
################################################

# Added April 8th to test out querying database
class Users_list_resource(restful.Resource):

	def get(self):
		users = Users.query.all()
		return [marshal(user, Users.fields()) for user in users], 200

api.add_resource(Users_list_resource, '/users_list')

################################################
################################################

# Parsing documentation
# http://flask-restful.readthedocs.org/en/latest/api.html#module-reqparse
user_parser = reqparse.RequestParser()
user_parser.add_argument('first', type = str)
user_parser.add_argument('last', type = str)
user_parser.add_argument('dob', type = str)

class User_resource(restful.Resource):

	# $ curl http://localhost:5000/user -d "first=john" -d "last=smith" -X POST -v
	def post(self):
		args = user_parser.parse_args()
		first = args['first']
		last = args['last']
		dob = restful.types.date(args['dob'])
		user = Users(first, last, dob)

		db.session.add(user)
		db.session.commit()
		return user.id

api.add_resource(User_resource, '/user')


if __name__ == '__main__':
	app.run(debug=True)
