from flask import Flask 
from flask.ext.sqlalchemy import SQLAlchemy
import json
# mysql://bbe6adb0b555dc:488c7e4d@us-cdbr-east-05.cleardb.net/heroku_5f9923672d3888a

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://halin2_guest:helloworld@engr-cpanel-mysql.engr.illinois.edu/halin2_sample'
db = SQLAlchemy(app)

# NOTE: Shows up in database as users, NOT Users
class Users(db.Model):
	user_id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(30))
	last_name = db.Column(db.String(30))
	dob = db.Column(db.DateTime)
	weight_lbs = db.Column(db.Integer)
	height_inches = db.Column(db.Integer)
	gender = db.Column(db.CHAR(1))

	def __init__(self, resource):
		self.first_name = resource['first_name']
		self.last_name = resource['last_name']
		self.dob = resource['dob']
		self.weight_lbs = resource['weight_lbs']
		self.height_inches = resource['height_inches']
		self.gender = resource['gender']

	# There's probably an easier way to do this....
	def __str__(self):
		output = dict()
		output["first_name"] = self.first_name
		output["last_name"] = self.last_name
		output["dob"] = self.dob
		output["weight_lbs"] = self.weight_lbs
		output["height_inches"] = self.height_inches
		output["gender"] = self.gender
		return json.dumps(output)
"""
	def __repr__(self):
		return '<User %s %s>' % (self.first_name, self.last_name)
"""
"""
# NOTE: Shows up in database as drugs, NOT Drugs
class Drugs(db.Model):
	drug_id = db.Column(db.Integer, primary_key=True)
	drug_name = db.Column(db.String(50), unique=True)
	# Probably want a drug description here later

	def __init__(self, resource):
		self.drug_name = resource['drugName']

	def __repr__(self):
		return '<Drug %s>' % self.drug_name

# NOTE: Shows up in database as side_effects
class SideEffects(db.Model):
	side_effects_id = db.Column(db.Integer, primary_key=True)
	side_effect = db.Column(db.String(150))

	drug_id = db.Column(db.Integer, db.ForeignKey('drugs.drug_id'))
	drug = db.relationship('drugs', backref=db.backref('posts', lazy='dynamic'))

	def __init__(self, resource):
		self.side_effect = resource['sideEffect']

	def __repr__(self):
		return '<Side Effect %r>' % self.side_effect

# NOTE: Shows up in database as side_effects_details
class SideEffectsDetails(db.Model):
	side_effects_details_id = db.Column(db.Integer, primary_key=True)
#	side_effect = db.Column(db.String(150))
	url = db.Column(db.String(250), unique=True)
	title = db.Column(db.String(100))
	forum_id = db.Column(db.String(30), unique=True)
	content = db.Column(db.Text)

	side_effects_id = db.Column(db.Integer, db.ForeignKey('side_effects.side_effects_id'))
	side_effects = db.relationship('side_effects', backref=db.backref('posts', lazy='dynamic'))

	def __init__(self, resource):
		self.url = resource['url']
		self.title = resource['title']
		self.forum_id = resource['forumId']
		self.content = resource['content']

	def __repr__(self):
		return '<Side Effect Details %s>' % self.title
		"""
