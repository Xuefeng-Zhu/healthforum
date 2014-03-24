#!/usr/bin/python
from flask import Flask
#import os

#tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '')
app = Flask(__name__)


import healthcode.views
"""
if __name__ == "__main__":
	app.run("0.0.0.0", 80, debug=True)
	"""
