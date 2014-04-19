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

########################################
# TODO FOR CASSANDRA
# Write a test similar to the one above.
#######################################



# Performs curl, given an argument string.
# Automatically parses the output using JSON. More, it ASSUMES that the output is
# a JSON output..... 
def curl(argstring):
	args = argstring.split(" ")
	args = ["curl"] + args
	data = subprocess.Popen(args, stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate()[0]
	return json.loads(data)


