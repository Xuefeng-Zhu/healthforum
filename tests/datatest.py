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
def alphaStartTest():
	alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
	for i in alphabet:
		drugs = curl(heroku + "drugs/result/" + i )
		try:
			if len(drugs) >= 0:
				return 0 # this is only going to check whether the query for 'a' works
			return 1
		except:
			return 2

# locate hello or dummy data
def dummyData():
	dummyText = ['hello']
	drugs = curl(heroku + "drugs/all")

# drugs is going to return an array of medicine objects / dictionaries
# You could access the medicine objects as such:
# drugs[i]["concise"], drugs[i]["name"]
# etc

	druglength = len(drugs)
	for i in range (0, druglength):
		if 'zyrtec' in drugs[i]: print drugs[i] # Not sure if this line would compile





# Performs curl, given an argument string.
# Automatically parses the output using JSON. More, it ASSUMES that the output is
# a JSON output..... 
def curl(argstring):
	args = argstring.split(" ")
	args = ["curl"] + args
	data = subprocess.Popen(args, stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate()[0]
	return json.loads(data)


