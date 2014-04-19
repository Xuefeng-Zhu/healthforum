#!/usr/bin/python

import subprocess 
import json

"""
This serves as a python file to test whether the data is running or not.

We simply try making GET, POST, DELETE, and UPDATE requests to the database
using the command line tool, curl.
"""

# Performs a query to return all the drugs in the database
def allDrugs():
	return curl("healthforum.herokuapp.com/drugs/all")


# Performs curl, given an argument string.
# Automatically parses the output using JSON. More, it ASSUMES that the output is
# a JSON output..... 
def curl(argstring):
	args = argstring.split(" ")
	args = ["curl"] + args
	print args
	data = subprocess.Popen(args, stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate()[0]
	return json.loads(data)


"""
if __name__ == "__main__":
	allDrugs()
	"""
