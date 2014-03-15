#!/usr/bin/python

"""
Code that will start and run the webserver.

Resources:

Server
http://docs.python.org/3/library/http.server.html
http://fragments.turtlemeat.com/pythonwebserver.php
http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html

Other
http://docs.python.org/2/library/os.html
http://docs.python.org/2.7/library/cgi.html

"""

import string, cgi, time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

# Request codes
OKAY = 200
NOT_FOUND = 404
MOVED = 301

# Other stuff
contype = "Content-type"
thtml = "text/html"

# Defines a class that handles server requests.
# Extends the base HTTP request handler, seems like this is the only way.
class reqHandler(BaseHTTPRequestHandler):

	# Fires off an event when a GET request is made
	def do_GET(self):
		try:
			# Fetches html documents on the server
			if self.path.endswith(".html"):

				# Opens and closes a file
				filepath = curdir + sep + ".." + sep + "client" + self.path
				with open(filepath) as file:
					print "Opening file: " + filepath
					file = open(filepath)
					self.send_response(OKAY)
					self.send_header(contype, thtml)
					self.end_headers()
					self.wfile.write(file.read())

		except IOError:
			self.send_error(NOT_FOUND, "File not found: " + self.path)

	# Fires off this function when a POST request is made	
	def do_POST(self):
		pass
"""	
		try:
			(ctype, pdict) = cgi.parse_header(self.headers.getheader(contype))
			if ctype == "multipart/form-data":
				query = cgi.parse_multipart(self.rfile, pdict)
			self.send_response(MOVED)
			self.end_headers()
			upfilecontent = query.get("upfile")
			print "filecontent", upfilecontent[0]
			self.wfile.write("<html>POST WAS OKAY =D<br><br>");
			self.wfile.write(upfilecontent[0]);
		except:
			pass
"""
# Starts the webserver
def main():
	try:
		host = ""
		protocol = 8080	# Invokes TCP protocol
		server = HTTPServer((host, protocol), reqHandler)
		print "Started http server. Going to run forever."
		server.serve_forever()
	except KeyboardInterrupt:
		print "^C received. Shutting down..."
		server.socket.close()

if __name__ == "__main__":
	main()



