from healthcode import app
from flask import request
from flask import render_template

@app.route("/")
def index():
    # template engine, hard.
    return render_template('index.html',  )


@app.route("/client/test", methods=['GET', 'POST'])
def index_page():
	if request.method=='POST':
		return "hi"
	else:
		return "hiya"
