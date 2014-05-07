import os
import flask
from flask import Flask, request, Response
from flask import render_template, url_for, redirect, send_from_directory
from flask import send_file, make_response, abort


# Create the application.
APP = Flask(__name__, static_url_path='')


@APP.route('/')
def basic_pages(**kwargs):
	return make_response(open('index.html').read())



if __name__ == '__main__':
    APP.debug=True
    APP.run()