from flask import Flask 
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restful import fields, marshal

# URLS for the databases. The default one is henryURI
herokuURI = 'mysql://bbe6abd0b555dc:488c7e4d@us-cdbr-east-05.cleardb.net/heroku_5f9923672d3888a'
henryURI = 'mysql://halin2_guest:helloworld@engr-cpanel-mysql.engr.illinois.edu/halin2_sample'

# In runserver.py, the code will not be able to access these global vars 
databaseApp = Flask(__name__)
databaseApp.config['SQLALCHEMY_DATABASE_URI'] = henryURI
db = SQLAlchemy(databaseApp)


# NOTE: Shows up in database as users, NOT Users
# TODO: We need more tables! Need a table for doctors as well as patients.
class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(30))
	last_name = db.Column(db.String(30))
	dob = db.Column(db.DateTime)
	weight_lbs = db.Column(db.Integer)
	height_inches = db.Column(db.Integer)
	gender = db.Column(db.CHAR(1))

	def __init__(self, first, last, dob):
		self.first_name = first
		self.last_name = last
		self.dob = dob

	# Marshalling documentation:
	# http://flask-restful.readthedocs.org/en/latest/api.html
	# http://flask-restful.readthedocs.org/en/latest/fields.html
	@staticmethod
	def fields():
		users_fields = {
			'first_name': fields.String,
			'last_name': fields.String,
			'dob': fields.DateTime,
			'weight_lbs': fields.Integer,
			'height_inches': fields.Integer,
			'gender': fields.Raw
		}
		return users_fields
	
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
