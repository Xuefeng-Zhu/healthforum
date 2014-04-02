#!/usr/bin/python
from flask import Flask
from datetime import datetime
from healthcode import app
import simplejson
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import mysql
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from logging import getLogger
loggers = [app.logger, getLogger('SQLAlchemy')]


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://bbe6adb0b555dc:488c7e4d@us-cdbr-east-05.cleardb.net/heroku_5f9923672d3888a'
db = SQLAlchemy(app)

class Users(db.Model):
	user_id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(30))
	last_name = db.Column(db.String(30))
	dob = db.Column(db.DateTime)
	weight_lbs = db.Column(db.Integer)
	height_inches = db.Column(db.Integer)
	gender = db.Column(db.Char(1))

	def __init__(self, resource):
		self.first_name = resource['first_name']
		self.last_name = resource['last_name']
		self.dob = resource['dob']
		self.weight_lbs = resource['weight_lbs']
		self.height_inches = resource['height_inches']
		self.gender = resource['gender']

	def __repr__(self):
		return '<User %s %s>' % (self.first_name, self.last_name)

class Drugs(db.Model):
	drug_id = db.Column(db.Integer, primary_key=True)
	drug_name = db.Column(db.String(50), unique=True)

	def __init__(self, resource):
		self.drug_name = resource['drugName']

	def __repr__(self):
		return '<Drug %s>' % self.drug_name

class SideEffects(db.Model):
	side_effects_id = db.Column(db.Integer, primary_key=True)
	side_effect = db.Column(db.String(150))

	drug_id = db.Column(db.Integer, db.ForeignKey('drug.drug_id'))
	drug = db.relationship('Drugs', backref=db.backref('posts', lazy='dynamic'))

	def __init__(self, resource):
		self.side_effect = resource['sideEffect']

	def __repr__(self):
		return '<Side Effect %r>' % self.side_effect

class SideEffectsDetails(db.Model):
	side_effects_details_id = db.Column(db.Integer, primary_key=True)
	side_effect = db.Column(db.String(150))
	url = db.Column(db.String(250), unique=True)
	title = db.Column(db.String(100))
	forum_id = db.Column(db.String(30), unique=True)
	content = db.Column(db.Text)

	side_effects_id = db.Column(db.Integer, db.ForeignKey('side_effects.side_effects_id'))
	side_effects = db.relationship('SideEffects', backref=db.backref('posts', lazy='dynamic'))

	def __init__(self, resource):
		self.url = resource['url']
		self.title = resource[' title']
		self.forum_id = resource['forumId']
		self.content = resource['content']

	def __repr__(self):
		return '<Side Effect Details %s>' % self.title

class Resources:

	def __init__(self):
		self.engine = None
		self.metadata = None # Collection of tables and their associated schema constructs
		self.session = None

		self.setup_connection()

		manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)

		self.setup_tables()
		self.process()

		app.run()

	def setup_connection(self):
		# set echo=False in production to avoid seeing SQLAlchemy logging
		self.engine = create_engine('mysql://bbe6adb0b555dc:488c7e4d@us-cdbr-east-05.cleardb.net/heroku_5f9923672d3888a', echo=True)
		Session = sessionmaker(bind=self.engine)
		self.session = Session()

	def setup_tables(self):
		db.create_all(self.engine)

	def process(self):
		# data = simplejson.load(urllib2.urlopen("http://api_url/drugs"))
		data = simplejson.load(open("drug_sideeffect_retResults.json", "r"))

		# Create API endpoints, which will be available at /api/<tablename> by
		manager.create_api(User, methods=['GET'],['POST'],['DELETE'])
		manager.create_api(Drugs, methods=['GET'],['POST'],['DELETE'])
		manager.create_api(SideEffects, methods=['GET'],['POST'],['DELETE'])
		manager.create_api(SideEffectsDetails, methods=['GET'],['POST'],['DELETE'])

		# populate the tables
		user = Users('first_name', 'last_name', 'dob','weight_lbs','height_inches','gender')
		drug = Drugs('drug_name')
		side_effect = SideEffects('side_effect')
		side_effect_details = SideEffectsDetails('url','title','forum_id','content')

"""
sample_json = [{"drugName":"some drug","sideEffect":"some side effect","retrievedObjects":[{"url":"http://www.some.url.om","forumId":"5","title":"some title1","content":"content 1"},{"url":"http://www.some.url.com","forumId":"3","title":"some title 2","content":"some content 2"}]

"""

		# TODO - may need to use JSONColumnParser below or some alternate solution
		for i, dr in enumerate(data['drugName']):
			drug = Drugs(dr) # create Drug object
			side_effects = [] # fill-up list of side effect objects
			for se in data['sideEffect'][i]:
				side_effects.append(SideEffects(se)) 
			drug.side_effects = side_effects 
			self.session.add(drug) 
			self.session.add(side_effect)

			# self.session.add(side_effect_details)
		self.session.commit()

# possible JSON solution
class JSONColumnParser(types.MutableType, types.TypeDecorator):
	impl = types.Unicode

	def process_bind_param(self, value, dialect):
		if value is json_null:
			value = None
		return simplejson.dumps(value)

	def process_result_value(self, value, dialect):
    if value is None:
			return None
		return simplejson.loads(value)

	def copy_value(self, value):
		return copy.deepcopy(value)
