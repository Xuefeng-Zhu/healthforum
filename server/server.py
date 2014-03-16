#!/usr/bin/python

from flask import Flask
app = Flask(__name__)

@app.route("/")
def index_page():
	return "HELLO WORLD"


if __name__ == "__main__":
	app.run("0.0.0.0",8080,debug=True)