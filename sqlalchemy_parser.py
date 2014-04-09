#!/usr/bin/python
# SQLAlchemy version 0.9.3
from flask import Flask
from datetime import datetime
from healthcode import app
import simplejson
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import mysql
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, types
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.types import TypeDecorator, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from logging import getLogger
loggers = [app.logger, getLogger('SQLAlchemy')]

app = Flask(__name__)
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
	# Probably want a drug description here later

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

# I'm not sure where this Resources class came from, actually
# SRM: included here for development only. Most of this is meant to be split off/incorporated into server.py and 
#      some is for loading data into mysql database.

class Resources():

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
		self.engine = create_engine('mysql://bbe6adb0b555dc:488c7e4d@us-cdbr-east-05.cleardb.net/heroku_5f9923672d3888a', echo=True, convert_unicode=True)
		Session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
		self.session = Session()

	def setup_tables(self):
		db.create_all(self.engine)

	def process(self):
		data = simplejson.load(open("drug_sideeffect_retResults.json", "r")) # Maybe use json.loads("drug_sideeffect_retResults.json") ?
		# Not sure what the simplejson class is doing
		# SRM: loads json sample into python dict, which is parsed out to the database in for loop below
		#      json.loads looks simpler than simplejson. I'll look into the differences tomorrow

		manager.create_api(User, methods=['GET'],['POST'],['DELETE'])
		manager.create_api(Drugs, methods=['GET'],['POST'],['DELETE'])
		manager.create_api(SideEffects, methods=['GET'],['POST'],['DELETE'])
		manager.create_api(SideEffectsDetails, methods=['GET'],['POST'],['DELETE'])


		"""
			data =  [{
				"drugName":"some drug",
				"sideEffect":"some side effect",
				"retrievedObjects":
					[{
						"url":"http://www.some.url.om",
						"forumId":"5",
						"title":"some title1",
						"content":"content 1"
					}]
			}]

		"""

	for i, dr in enumerate(data['drugName']):
		drug = Drugs(dr)
		self.session.add(drug)

			for se in data['sideEffect']:
				side_effect = SideEffects(se)
				self.session.add(side_effect)

				for j, reO in data['retrievedObjects'][i]:
					side_effects_details = SideEffectsDetails(reO)

					url = data['retrievedObjects'][j]['url']
					self.session.add(url)

					forumid = data['retrievedObjects'][j]['forumId']
					self.session.add(forumid)

					title = data['retrievedObjects'][j]['title']
					self.session.add(title)

					content = data['retrievedObjects'][j]['content']
					self.session.add(content)

		self.session.commit()

