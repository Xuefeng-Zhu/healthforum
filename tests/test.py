#!/usr/bin/python
from datatest import *

# Executes all of the tests
#
# "Why not use python's unittest framework? I have no idea. I wanted 
# to write my own.
def main():
	tests = []
	tests.append(result(allDrugsTest, "allDrugsTest"))

########################################
# TODO FOR CASSANDRA
# Just like I did in line 10, call your test from datatest.py
# by passing it into the result() function.
#######################################

	# Iterates through all the tuples in the list
	numPass = 0
	numFailed = 0
	numWarning = 0
	for test in tests:
		if test[1] == 0:
			print test[0] + " has passed."
			numPass += 1

		elif test[1] == 1:
			print test[0] + " has indicated a database error."
			numWarning += 1

		else:
			print test[0] + " has completely failed..."
			numFailed += 1
	
	# TODO: Tabular library in python?
	print "\nRESULTS:"
	print "Passed:\t\t" + str(numPass)
	print "Warning:\t" + str(numWarning)
	print "Failed:\t\t" + str(numFailed)

	if numFailed == 0 and numWarning == 0:
		print "Congrats: The code completely passed!"

# Executes testFunc with the given args.
# (testFunc is a function, not an object)
#
# Returns a test tuple: ("function name", state)
# if state == 0: The test passed
# if state == 1: The test ran, but there might be output errors
# if state == 2: The test completely failed
#
# TODO: Find out a way to get the function name of testFunc
def result(testFunc, funcName, * args):
	
	# Note, this is untested
	if len(args) > 0:
		return (funcName, testFunc(args)) 
	return (funcName, testFunc())


if __name__ == "__main__":
	main()
