import subprocess 
import json

"""
This serves as a python file to test whether the data is running or not.

We simply try making GET, POST, DELETE, and UPDATE requests to the database
using the command line tool, curl.

TODO: Possible method of refractoring: Use decorators to declare tests.
From the decorators, test.py can find which functions are tests are not
"""
heroku = "healthforum.herokuapp.com/"

# Performs a query to return all the drugs in the database
# Performs a simple test to see whether an array of at least length 100
# was pushed back
#
# Output:
# 0: The test passed
# 1: Something might be wrong with the data
# 2: Something's majorly wrong with the database.

def allDrugsTest():
	drugs = curl(heroku + "drugs/all")
	try:
		if len(drugs) < 100:
			return 1
		return 0
			
	# If we go through this code, something's majorly wrong
	except:
		return 2

# tests all possible alpha chars at start of drug name
# this can return empty arrays if there are no drug names beginning with a letter
# an empty array is not a possible error at this point, if it is, adjust IF test accordingly
# NOTE: as long as an array is returned from the db for each letter, this passes
# actually, i'm not sure how to fail this (return 1), since nothing sets passed = 0, as long as one letter exists
# might have to do something other than length of the list? it'd be stupid to fail if a beginsWith letter is false
# HALP!

# Henry: Hmm.... Maybe in this case, we'd just want to check "specific" consistency in the data.
# For example, "clo" currently brings back 3 results. If this number changes, then
# raise a warning. Otherwise we're good to go.
# (You'd make siilar tests for different substrings)
def alphaStartTest():
	alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
	try:
		for i in alphabet:
			drugs = curl(heroku + "drugs/result/" + i )
			if not len(drugs) >= 0:
				return 1
		return 0
	except:
		return 2

# locate dummy data
# alternatively, use this to locate other key words or phrases
#
# Henry: So actually, this function is going to return true everytime, because a lot of drugs have the following concise field:
# "Hello world. This is somee information."
def dummyData():
	dummyText = ['hello world', 'add more dummy data from concise as element', 'avoid single words that could be in real entries']
	drugs = curl(heroku + "drugs/all")
	dummyTextExists = 0

	# Henry: You might want to practice iterating upon the items in the list, not the
	# indices of the list
	# Python's special in that sense. Aim to write pythonic code!
	# I'll let you try writing code that doesn't use indices. Have a go at it.
	try:
		for i in range (0, len(drugs)):
			for j in range (0, len(dummyText)):
				if dummyText[j].lower() in drugs[i]["concise"].lower():
					return 1
					# we could return 99 here if we're just looking for the existence of dummy text instead of testing all data
					# but we may want to log which arrays/data have dummy text so we can fix it

		return 0
	except:
		return 2

# is patient side effect per drug empty
def patientData():
	drugs = curl(heroku + "drugs/all")
	drugNames = []
	passed = 1

	try:
		for i in range (0, len(drugs)):
			# get a list of all drug names in the db
			drugNames.append (drugs[i]["name"])
		
		# Again, you don't have to iterate through the indices of the list, just the elements themselves.
		for j in range (0, len(drugNames)):
			# list of patient data per drug
			pData =  curl(heroku + "drugs/" + drugNames[j] + "/patient")
			if len(pData["effects"]) == 0:
				# there is a zero array for drug i
				passed = 0
			
			if passed == 1:
				# all drugs have patient data
				return 0
			return 1
	except:
		return 2

# is doctor side effect per drug empty
def doctorData():
	drugs = curl(heroku + "drugs/all")
#	drugNames = []
	passed = 1

	try:
#	for i in range (0, len(drugs)):
#			# get a list of all drug names in the db
#			drugNames.append (drugs[i]["name"])

		# More pythonic code - this time throwing something functional in there
		drugNames = [drug["name"] for drug in drugs]
		
		for j in range (0, len(drugNames)):
			# list of doctor data per drug
			pData =  curl(heroku + "drugs/" + drugNames[j] + "/doctor")
			if len(pData["effects"]) == 0:
				# there is a zero array for drug i
				passed = 0
			
			if passed == 1:
				# all drugs have doctor data
				return 0
			return 1
	except:
		return 2


# Performs curl, given an argument string.
# Automatically parses the output using JSON. More, it ASSUMES that the output is
# a JSON output..... 
def curl(argstring):
	args = argstring.split(" ")
	args = ["curl"] + args
	data = subprocess.Popen(args, stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate()[0]
	return json.loads(data)
