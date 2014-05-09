#!/usr/bin/python
import unicodedata
from flask.ext.restful.types import date, url
from flask import send_file, make_response, abort
from flask import Flask
from flask.ext import restful
from flask.ext.restful import reqparse, marshal_with, marshal
from flask.ext.restful.utils import cors
from database import *
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth
from sqlalchemy.exc import IntegrityError
import MySQLdb
from contextlib import closing
auth = HTTPBasicAuth()

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

app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = URI
data = SQLAlchemy(app)

api = restful.Api(app)
api.decorators=[cors.crossdomain(origin='*')]


def openSession():
	if useHenry:
		return MySQLdb.connect(host = "engr-cpanel-mysql.engr.illinois.edu",
								user = "halin2_guest",
								passwd = "helloworld",
								db = "halin2_sample")

	else:
		return MySQLdb.connect(host = "engr-cpanel-mysql.engr.illinois.edu",
								user = "halin2_guest",
								passwd = "helloworld",
								db = "halin2_test")


###############################################
###############################################

class Drug_info_resource(restful.Resource):
	def get(self, drugname):
		druginfo = Drugs.query.filter_by(name = drugname).first()
		return {"name": druginfo.name, "concise": druginfo.info, \
				"price": druginfo.price}

api.add_resource(Drug_info_resource, "/drugs/info/<string:drugname>")

# Returns a list of all of the drugs in the database
class Drug_List_resource(restful.Resource):

	def get(self):
		try:
			drugs = Drugs.query.order_by(Drugs.name).all()
			return [{"name": drug.name, "concise": drug.info} for drug in drugs if drug.info != "None"]
		except:
			return "Error...", 500 

api.add_resource(Drug_List_resource, '/drugs/all')
# Given a drug's name and whether a user is a patient or doctor,
# return a list of side effects corresponding to the user
class Drug_Effect_resource(restful.Resource):

	def get(self, drugName, userType):
		drug = Drugs.query.filter_by(name = drugName.lower()).first()
		drugId = drug.id

		side_effects = SideEffects.query.filter_by(drug_id = drugId).all()


		output = dict()
		output["name"] = drugName
		output["sideEffects"] = []

		for effect in side_effects:
			sideEffect = dict()
			doc = 1 if userType.lower() == "doctor" else 0
			sideEffect["name"] = effect.doctor_effect if doc else effect.patient_effect
			sideEffect["posts"] = [marshal(post, SideEffectsDetails.fields()) \
				for post in SideEffectsDetails.query \
					.filter_by(side_effect_id = int(effect.id), isDoctor = doc) \
					.limit(3)]
			output["sideEffects"].append(sideEffect)
			
		return output


api.add_resource(Drug_Effect_resource, '/drugs/<string:drugName>/<string:userType>')

# Grabs the drugs that start with the given characters
class Drugs_Substr_resource(restful.Resource):

	def get(self, startChars):
		try:
			drugs = Drugs.query.filter(Drugs.name.startswith(startChars)).all()
			return [drug.name for drug in drugs]
		except:
			return "Drug not found", 404

api.add_resource(Drugs_Substr_resource, '/drugs/list/<string:startChars>')

# Grabs the drugs and their information that start with the given characters
class Drugs_Substr_Result_resource(restful.Resource):

	def get(self, startChars):
		drugs = Drugs.query.filter(Drugs.name.startswith(startChars)).all()
		return [{"name": drug.name, "concise": drug.info} for drug in drugs]

api.add_resource(Drugs_Substr_Result_resource, '/drugs/result/<string:startChars>')

################################################
################################################

loginParse = reqparse.RequestParser()
loginParse.add_argument("email", type=str)
loginParse.add_argument("password", type=str)
class Login_users_resource(restful.Resource):

	# Logging a user in	
	def post(self):
		args = loginParse.parse_args()
		email = args["email"]
		password = args["password"]

		db = openSession()
		with closing(db.cursor()) as cursor:

			queryString = "select first_name, id, hashedPass from users where email='{0}'" \
						.format(MySQLdb.escape_string(email))
			cursor.execute(queryString)
			first_name, id, hashedPass = cursor.fetchone()

			if Users.verify(password, hashedPass):
						
				return {"message": "Success", "first_name": first_name, "id": id },\
					201,\
					{'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "GET, POST"} 
			else:
				return {"message": "Error: Username or password is incorrect."}, 403, {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "GET, POST"}


api.add_resource(Login_users_resource, '/login/user')


createUserParser = reqparse.RequestParser()
createUserParser.add_argument("first", type=str, required=True)
createUserParser.add_argument("last", type=str, required=True)
createUserParser.add_argument("email", type=str, required=True)
createUserParser.add_argument("password", type=str, required=True)
createUserParser.add_argument("isDoctor", type=bool, required=True)
class Create_user_resource(restful.Resource):

	# Create a user account
	def post(self):
		try:
			args = createUserParser.parse_args()

			first = args['first']
			last = args['last']
			email = args["email"]
			password = args["password"]
			isDoctor = args['isDoctor']

			newUser = Users(first, last, email, password, isDoctor)
			data.session.add(newUser)
			data.session.commit()
			return {"message": "User with email {0} created".format(email), "user_id": newUser.id}, \
			201, \
			{'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "GET, POST"}
		except IntegrityError:
			return {"message": "Error: Email already exists" }, 403, {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "GET, POST"} 

api.add_resource(Create_user_resource, '/registration/user')


createDoctorParser = reqparse.RequestParser()
createDoctorParser.add_argument("user_id", type=int, required = True)
createDoctorParser.add_argument("hospital", type=str)
createDoctorParser.add_argument("specialization", type=str)
createDoctorParser.add_argument("title", type=str)
class Create_doctor_resource(restful.Resource):
	
	def post(self):
		args = createDoctorParser.parse_args()
		user_id = args["user_id"]
		hospital = args.get("hospital", None)
		specialization = args.get("specialization", None)
		title = args.get("title", None)
		newDoctor = Doctors(user_id, hospital, specialization, title)
		data.session.add(newDoctor)
		data.session.commit()
		return {"message": "Doctor created", "user_id": user_id}, 201, {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "GET, POST"} 

api.add_resource(Create_doctor_resource, '/registration/doctor')

createPatientParser = reqparse.RequestParser()
createPatientParser.add_argument("user_id", type=int, required = True)
createPatientParser.add_argument("dob", type = str)
createPatientParser.add_argument("weight_lbs", type=int)
createPatientParser.add_argument("height_in", type = int)
createPatientParser.add_argument("gender", type = str) 

class Create_patient_resource(restful.Resource):

	def post(self):
		args = createPatientParser.parse_args()
		user_id = args["user_id"]
		dob = args.get('dob', None)
		if dob is not None:
			dob = date(dob).date() 
		height_in = args.get('height_in', None)
		weight_lbs = args.get('weight_lbs', None)
		gender = args.get('gender', None)
		newPatient = Patients(user_id, dob, weight_lbs, height_in, gender)
		data.session.add(newPatient)
		data.session.commit()
		return {"message": "Patient created", "user_id": user_id}, 201, {'Access-Control-Allow-Origin': '*'} 

api.add_resource(Create_patient_resource, '/registration/patient')

###############################################
###############################################

createCommentsParser = reqparse.RequestParser()
createCommentsParser.add_argument("user_id", type=str, required = True)
createCommentsParser.add_argument("drug_id", type=int, required = True)
createCommentsParser.add_argument("content", type=str, required = True)

class Create_comments_resource(restful.Resource):

	def post(self):
		args = createCommentsParser.parse_args()
		user_id = args["user_id"]
		drug_id = args["drug_id"]
		content = args["content"]
		comment = Comments(user_id, drug_id, content)
		data.session.add(comment)
		data.session.commit()
		return {"message": "Comment created"}, 201, {'Access-Control-Allow-Origin': '*'} 
		
api.add_resource(Create_comments_resource, '/comments/create')
		
class Get_comments_resource(restful.Resource):

	def get(self, drug_id):
		db = openSession()		
		with closing(db.cursor()) as cursor:
			queryString = "select * from comments where drug_id = {0}".format(drug_id)
			cursor.execute(queryString)
			comments = cursor.fetchall()
			comments = [{"id": id, "user_id": user_id, \
							"drug_id": drug_id, "content": content} \
							for id, user_id, drug_id, content in comments]
			return comments, 201, {'Access-Control-Allow-Origin': '*'}
			
api.add_resource(Get_comments_resource, '/comments/get/<int:drug_id>', endpoint = "<int:drug_id>")


###############################################
###############################################

@app.route('/index.html')
def index(**kwargs):
	return basic_pages(* kwargs)

@app.route('/')
def basic_pages(**kwargs):
	return make_response(open('templates/index.html').read())

if __name__ == '__main__':
	app.run(debug=True)

