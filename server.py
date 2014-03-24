#!/usr/bin/python
from flask import Flask
from flask import request
from flask import render_template
import os

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '')
app = Flask(__name__, template_folder = tmpl_dir)


# Note to Self: Serving static content through Flask is not a good idea. host on actual webserver instead of app server

@app.route("/")
def index():
    # template engine, hard.
    return render_template('client/index.html',  )


@app.route("/client/test",methods=['GET', 'POST'])
def index_page():
	if request.method=='POST':
		return "hi"
	else:
		return "hiya"

if __name__ == "__main__":
	app.run("0.0.0.0", 80, debug=True)
