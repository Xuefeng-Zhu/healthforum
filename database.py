from math import ceil
from flask import Flask 
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restful import fields, marshal
from hashlib import sha224
from passlib.apps import custom_app_context as pwd_context
useHenry = False

# URLS for the databases. The default one is henryURI
# the clearDB database has been deleted! I commented out herokuURI for this reason.
#herokuURI = 'mysql://bbe6abd0b555dc:488c7e4d@us-cdbr-east-05.cleardb.net/heroku_5f9923672d3888a' # I think I accidentally deleted this....
henryURI = 'mysql://halin2_guest:helloworld@engr-cpanel-mysql.engr.illinois.edu/halin2_sample'
testURI = 'mysql://halin2_guest:helloworld@engr-cpanel-mysql.engr.illinois.edu/halin2_test'

URI = henryURI if useHenry else testURI

# In runserver.py, the code will not be able to access these global vars 
databaseApp = Flask(__name__)
databaseApp.config['SQLALCHEMY_DATABASE_URI'] = URI
db = SQLAlchemy(databaseApp)


# NOTE: Shows up in database as users, NOT Users
# TODO: We need more tables! Need a table for doctors as well as patients.
class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True, nullable = False)
	first_name = db.Column(db.String(30))
	last_name = db.Column(db.String(30))
	email = db.Column(db.String(50), unique = True, nullable = False)
	hashedPass = db.Column(db.String(132), nullable = False)
	isDoctor = db.Column(db.Boolean, nullable = False)

	def __init__(self, first, last, email, password, isDoctor):
		self.first_name = first
		self.last_name = last
		self.email = email
		self.hashedPass = Users.hash(password)
		self.isDoctor = isDoctor

	@staticmethod
	def hash(string):
		return pwd_context.encrypt(string)

	@staticmethod
	def verify(password, hashedPass):
		return pwd_context.verify(password, hashedPass)

	# Marshalling documentation:
	# http://flask-restful.readthedocs.org/en/latest/api.html
	# http://flask-restful.readthedocs.org/en/latest/fields.html
	@staticmethod
	def fields():
		users_fields = {
			'first_name': fields.String,
			'last_name': fields.String,
			'isDoctor': fields.Boolean,
			'email': fields.email
		}
		return users_fields
	
class Patients(db.Model):
	id = db.Column(db.Integer, primary_key = True, nullable = False)
	user_id = db.Column(db.Integer, unique = True, nullable = False)
	dob = db.Column(db.Date)
	weight_lbs = db.Column(db.SMALLINT)
	height_in = db.Column(db.SMALLINT)
	gender = db.Column(db.Enum('F', 'M'))

	def __init__(self, user_id, dob, weight, height_in, gender):
		if height_in >= 12:
			print "WARNING: height_in >= 12"
		self.user_id = user_id
		self.dob = dob
		self.height_in = height_in
		self.weight_lbs = weight
		self.gender = gender

	@staticmethod
	def fields():
		patient_fields = {
			'dob': fields.DateTime,
			'height_ft': fields.Integer,
			'height_in': fields.Integer,
			'gender': fields.String 
		}
		return patient_fields

class Doctors(db.Model):
	id = db.Column(db.Integer, primary_key = True, nullable = False)
	user_id = db.Column(db.Integer, unique = True, nullable = False)
	hospital = db.Column(db.String(100))
	specialization = db.Column(db.String(60))
	title = db.Column(db.String(52))

	def __init__(self, user_id, hospital, specialization, title):
		self.user_id = user_id
		self.hospital = hospital
		self.specialization = specialization
		self.title = title

	@staticmethod
	def fields():
		pass # TODO


# NOTE: Shows up in database as drugs, NOT Drugs
class Drugs(db.Model):
	id = db.Column(db.Integer, primary_key=True, nullable = False)
	name = db.Column(db.String(50), unique=True, nullable = False)
	info = db.Column(db.Text)
	price = db.Column(db.Integer)

	def __init__(self, name, info, price):
		self.name = name
		self.info = info
		self.price = ceil(price)

	@staticmethod
	def fields():
		drug_fields = {
			'id': fields.Integer,
			'name': fields.String, 
			'info': fields.String,
			'price': fields.Integer
		}
		return drug_fields


# NOTE: Shows up in database as side_effects
class SideEffects(db.Model):
	id = db.Column(db.Integer, primary_key=True, nullable = False)
	drug_id = db.Column(db.Integer, db.ForeignKey('drugs.id'), nullable = False)
	patient_effect = db.Column(db.String(150))
	doctor_effect = db.Column(db.String(150))
	# TODO: Add a rank to side effects

	# TODO: I got an error whenever I uncommented the below line. We should look into that.
	# I'll look into this documentation later:
	# https://pythonhosted.org/Flask-SQLAlchemy/models.html
	#	drug = db.relationship('drugs', backref=db.backref('posts', lazy='dynamic'))

	@staticmethod
	def fields(userType):

		if userType == "doctor":
			return {
				'id': fields.Integer,
				'drug_id': fields.Integer,
				'doctor_effect': fields.String
			}

		else:
			return {
				'id': fields.Integer,
				'drug_id': fields.Integer,
				'patient_effect': fields.String
			}

	def __init__(self, resource):
		self.side_effect = resource['sideEffect']

	def __repr__(self):
		if self.doctor_effect is not None:
			return str({
				'id': self.id,
				'drug_id': self.drug_id,
				'doctor_effect': self.doctor_effect
			})
			
		else:
			return str({
				'id': self.id,
				'drug_id': self.drug_id,
				'patient_effect': self.patient_effect
			})

# NOTE: Shows up in database as side_effects_details
class SideEffectsDetails(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	url = db.Column(db.String(250), nullable = False)
	title = db.Column(db.String(100), nullable = False)
	forum_id = db.Column(db.String(30))
	content = db.Column(db.Text, nullable = False)
	side_effect_id = db.Column(db.Integer, nullable = False)
	isDoctor = db.Column(db.Boolean)

	# NOTE: This is dead code
	def __init__(self, resource):
		self.url = resource['url']
		self.title = resource['title']
		self.forum_id = resource['forumId']
		self.content = resource['content']

	@staticmethod
	def fields():
		return {
			"url": fields.String,
			"title": fields.String,
			"content": fields.String,
		}

class Comments(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, nullable = False)
	drug_id = db.Column(db.String(250), nullable = False)
	content = db.Column(db.String(250), nullable = False)
	
	def __init__(self, user_id, drug_id, content):
		self.user_id = user_id
		self.drug_id = drug_id
		self.content = content

