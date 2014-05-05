#!/usr/bin/python
import unicodedata
from flask.ext.restful.types import date, url
from flask import Flask
from flask.ext import restful
from flask.ext.restful import reqparse, marshal_with, marshal
from flask.ext.restful.utils import cors
from database import Users, Drugs, SideEffects, URI, Doctors, Patients
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth
from sqlalchemy.exc import IntegrityError
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

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = URI
data = SQLAlchemy(app)

api = restful.Api(app)
api.decorators=[cors.crossdomain(origin='*'), api.representation("application/json")]


################################################
################################################
#
#class Drug_info_resource(restful.Resource):
#	def get(self, drugname):
#		try:
#			druginfo = Drugs.query.filter_by(name = drugname).first()
#			return {"name": druginfo.name, "concise": druginfo.info}
#		except:
#			data.session.rollback()
#			return "Error...", 500 
#
#api.add_resource(Drug_info_resource, "/drugs/info/<string:drugname>")
#
## Returns a list of all of the drugs in the database
#class Drug_List_resource(restful.Resource):
#
#	def get(self):
#		try:
#			drugs = Drugs.query.order_by(Drugs.name).all()
#			return [{"name": drug.name, "concise": drug.info} for drug in drugs]
#		except:
#			data.session.rollback()
#			return "Error...", 500 
#
#api.add_resource(Drug_List_resource, '/drugs/all')
#
## Given a drug's name and whether a user is a patient or doctor,
## return a list of side effects corresponding to the user
#class Drug_Effect_resource(restful.Resource):
#
#	def get(self, drugName, userType):
#		try:
#			effectType = "doctor_effect" if userType.lower() == "doctor" else "patient_effect"
#			drugId = Drugs.query.filter_by(name = drugName.lower()).first().id
#
#			# TODO: Learn how to do a f***** select statement in SQLAlchemy! There's code to be refractored 
#			queryEffects = SideEffects.query.filter_by(drug_id = drugId)
#			
#			# TODO: Stop being a noob and have less if statements
#			output = dict()
#			output["name"] = drugName
#			output["userType"] = userType
#			output["drugId"] = drugId
#			if userType == "doctor":
#				output["effects"] = [{"name": query.doctor_effect, "something": "hello"} for query in queryEffects]
#			else:
#				output["effects"] = [{"name": query.patient_effect, "something": "hello"} for query in queryEffects]
#				
#			return output
#		except:
#			data.session.rollback()
#			return "Error...", 500 
#
#
#api.add_resource(Drug_Effect_resource, '/drugs/<string:drugName>/<string:userType>')
#
## Grabs the drugs that start with the given characters
#class Drugs_Substr_resource(restful.Resource):
#
#	def get(self, startChars):
#		try:
#			drugs = Drugs.query.filter(Drugs.name.startswith(startChars)).all()
#			return [drug.name for drug in drugs]
#		except:
#			data.session.rollback()
#			return "Drug not found", 404
#
#api.add_resource(Drugs_Substr_resource, '/drugs/list/<string:startChars>')
#
## Grabs the drugs and their information that start with the given characters
#class Drugs_Substr_Result_resource(restful.Resource):
#
#	def get(self, startChars):
#		try:
#			drugs = Drugs.query.filter(Drugs.name.startswith(startChars)).all()
#			return [{"name": drug.name, "concise": drug.info} for drug in drugs]
#		except:
#			data.session.rollback() 
#
#api.add_resource(Drugs_Substr_Result_resource, '/drugs/result/<string:startChars>')
#
#################################################
#################################################
#
#loginParse = reqparse.RequestParser()
#loginParse.add_argument("email", type=str, required=True)
#loginParse.add_argument("password", type=str, required=True)
#class Login_users_resource(restful.Resource):
#
#	# Logging a user in	
#	def post(self):
#		args = loginParse.parse_args()
#		email = args["email"]
#		password = args["password"]
#
#		user = Users.query.filter_by(email = email).first()
#		if user is None or not Users.verify(password, user.hashedPass):
#			return {"message": "Error: Username or password is incorrect."}, 403, {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "GET, POST"} 
#			
#		return {"message": "Success"}, 201, {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "GET, POST"} 
#		# TODO: Return what user data?
#
#api.add_resource(Login_users_resource, '/login/user')
#
#
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

			# Checking uniqueness of user
			user = Users.query.filter_by(email = email).first()
			if user is not None:
				raise IntegrityError("Email already exists in database", email, "hello")

			newUser = Users(first, last, email, password, isDoctor)
			data.session.add(newUser)
			data.session.commit()
			return {"message": "User with email {0} created".format(email), "user_id": newUser.id}, \
			201, \
			{'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "GET, POST"} \
		except IntegrityError:
			return {"message": "Error: Email already exists" }, 403, {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "GET, POST"} 

api.add_resource(Create_user_resource, '/registration/user')

#
#createDoctorParser = reqparse.RequestParser()
#createDoctorParser.add_argument("user_id", type=int, required = True)
#createDoctorParser.add_argument("hospital", type=str)
#createDoctorParser.add_argument("specialization", type=str)
#createDoctorParser.add_argument("title", type=str)
#class Create_doctor_resource(restful.Resource):
#	
#	def post(self):
#		args = createDoctorParser.parse_args()
#		user_id = args["user_id"]
#		hospital = args.get("hospital", None)
#		specialization = args.get("specialization", None)
#		title = args.get("title", None)
#		newDoctor = Doctors(user_id, hospital, specialization, title)
#		data.session.add(newDoctor)
#		data.session.commit()
#		return {"message": "Doctor created", "user_id": user_id}, 201, {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "GET, POST"} 
#
#api.add_resource(Create_doctor_resource, '/registration/doctor')
#
#createPatientParser = reqparse.RequestParser()
#createPatientParser.add_argument("user_id", type=int, required = True)
#createPatientParser.add_argument("dob", type = str)
#createPatientParser.add_argument("weight_lbs", type=int)
#createPatientParser.add_argument("height_in", type = int)
#createPatientParser.add_argument("gender", type = str) 
#
#class Create_patient_resource(restful.Resource):
#
#	def post(self):
#		args = createPatientParser.parse_args()
#		user_id = args["user_id"]
#		dob = args.get('dob', None)
#		if dob is not None:
#			dob = date(dob).date() 
#		height_in = args.get('height_in', None)
#		weight_lbs = args.get('weight_lbs', None)
#		gender = args.get('gender', None)
#		newPatient = Patients(user_id, dob, weight_lbs, height_in, gender)
#		data.session.add(newPatient)
#		data.session.commit()
#		return {"message": "Patient created", "user_id": user_id}, 201, {'Access-Control-Allow-Origin': '*'} 
#
#
#api.add_resource(Create_patient_resource, '/registration/patient')
#
###############################################
###############################################
if __name__ == '__main__':
	app.run(debug=True)
