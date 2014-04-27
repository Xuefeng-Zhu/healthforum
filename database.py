from flask import Flask 
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restful import fields, marshal
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
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(30))
	last_name = db.Column(db.String(30))
	email = db.Column(db.String(50), unique = True)
	password_hash = db.Column(db.String(132))
	isDoctor = db.Column(db.Boolean)

	def __init__(self, first, last, email, password, isDoctor):
		self.first_name = first
		self.last_name = last
		self.email = email
		self.password_hash = hash(password)
		self.isDoctor = isDoctor

	@staticmethod
	def hash(string)
		return pwd_context.encrypt(string)

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
	id = db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.Integer)
	dob = db.Column(db.Date)
	weight_lbs = db.Column(db.SMALLINT)
	height_in = db.Column(db.SMALLINT)
	gender = db.Column(db.Enum('F', 'M'))

	def __init__(self, dob, weight, height_ft, height_in, gender):
		if height_in >= 12:
			print "WARNING: height_in >= 12"
		self.dob = dob
		self.weight_lbs = weight
		self.height_in = height_ft * 12 + height_in
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
	id = db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.Integer)
	hospital = db.Column(db.String(100))
	specialization = db.Column(db.String(60))
	title = db.Column(db.String(52))

	def __init__(self, user_id, hospital, specialization, title):
		self.user_id = user_id
		self.hospital = hospital
		self.specialization = specialization
		self.title = title


# NOTE: Shows up in database as drugs, NOT Drugs
class Drugs(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), unique=True)
	info = db.Column(db.Text)

	def __init__(self, name, info):
		self.name = name
		self.info = info

	@staticmethod
	def fields():
		drug_fields = {
			'id': fields.Integer,
			'name': fields.String, 
			'info': fields.String
		}
		return drug_fields


# NOTE: Shows up in database as side_effects
class SideEffects(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	drug_id = db.Column(db.Integer, db.ForeignKey('drugs.id'))
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
	effect = db.Column(db.String(150))
	url = db.Column(db.String(250), unique=True)
	title = db.Column(db.String(100))
	forum_id = db.Column(db.String(30), unique=True)
	content = db.Column(db.Text)

	side_effects_id = db.Column(db.Integer, db.ForeignKey('side_effects.id'))

	# TODO: I got an error whenever I uncommented the below line. We should look into that.
	# I'll look into this documentation later:
	# https://pythonhosted.org/Flask-SQLAlchemy/models.html
#side_effects = db.relationship('side_effects', backref=db.backref('posts', lazy='dynamic'))

	def __init__(self, resource):
		self.url = resource['url']
		self.title = resource['title']
		self.forum_id = resource['forumId']
		self.content = resource['content']

	def __repr__(self):
		return '<Side Effect Details %s>' % self.title
