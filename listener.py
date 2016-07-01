from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
import re
import json
from user import User
from student import Student
from const import *

class MyRequestHandler (BaseHTTPRequestHandler) :

	def authenticate(self):
		auth = False
		u = User()
		if self.headers.getheader('Authorization') is not None :
				authParams = self.headers.getheader('Authorization').split()
				if len(authParams) == 2 and authParams[0] == "Basic" :
					userPassword = (authParams[1].decode("base64")).split(":")
					if userPassword[0] and userPassword[1]:
						auth = u.authenticate(userPassword[0], userPassword[1])
		return auth

	# Routing get requests
	# Default Bad request
	def do_GET(self) :
		if re.match("/student\?.*", self.path):
			response = {"status" : 401, "msg" : "Authorization Failed"}
			if self.authenticate():
				# getting get url parameters
				params = self.path.split("/student?", 1)[1]
				params = dict(qc.split("=") for qc in params.split("&"))
				if 'id' in params:
					s = Student()
					response = s.getDetails(params['id'])
				else:
					response = {"status" : 400 , "msg" : "Bad Request"}
			# Setting http response
			self.send_response(response["status"])
			# Removing status value from response
			response.pop("status", None)
			self.end_headers()
			# Writing response
			json.dump(response, self.wfile)
		else :
			# Default
			self.send_response(400)
			self.end_headers()
			json.dump({'msg': 'Bad Request'}, self.wfile)

	# Routing post requests
	# Default Bad request
	def do_POST(self) :
		# Getting body data
		data = self.rfile.read(int(self.headers['Content-Length']))
		data = json.loads(data)
		u = User()
		if self.path == "/register" :
			response = u.register(data)
		elif self.path == "/login" :
			response = u.login(data)
		elif self.path == "/generateOTP" :
			response = u.generateOTP(data)
		elif self.path == "/createStudent" :
			response = {"status" : 401, "msg" : "Authorization Failed"}
			if self.authenticate():
				s = Student()
				response = s.create(data)
		else :
			# Default
			response = {"status" : 400, "msg" : "Bad Request"}
		# Setting http response
		self.send_response(response["status"])
		# Removing status value from response
		response.pop("status", None)
		self.end_headers()
		# Writing response
		json.dump(response, self.wfile)

	# Routing post requests
	# Default Bad request
	def do_PUT(self):
		if re.match("/updateStudent\?.*", self.path):
			response = {"status" : 401, "msg" : "Authorization Failed"}
			if self.authenticate():
				# getting get url parameters
				params = self.path.split("/updateStudent?", 1)[1]
				params = dict(qc.split("=") for qc in params.split("&"))
				if 'id' in params:
					data = self.rfile.read(int(self.headers['Content-Length']))
					data = json.loads(data)
					s = Student()
					response = s.update(params['id'], data)
				else:
					response = {"status" : 400 , "msg" : "Bad Request"}
			# Setting http response
			self.send_response(response["status"])
			self.end_headers()
			# Removing status value from response
			response.pop("status", None)
			# Writing response
			json.dump(response, self.wfile)
		else :
			# Default
			self.send_response(400)
			self.end_headers()
			json.dump({'msg': 'Bad Request'}, self.wfile)

	# Routing delete requests
	# Default Bad request
	def do_DELETE(self) :
		if re.match("/student\?.*", self.path):
			response = {"status" : 401, "msg" : "Authorization Failed"}
			if self.authenticate():
				# getting get url parameters
				params = self.path.split("/student?", 1)[1]
				params = dict(qc.split("=") for qc in params.split("&"))
				if 'id' in params:
					s = Student()
					response = s.delete(params['id'])
				else:
					response = {"status" : 400 , "msg" : "Bad Request"}
			# Setting http response
			self.send_response(response["status"])
			self.end_headers()
			# Removing status value from response
			response.pop("status", None)
			# Writing response
			json.dump(response, self.wfile)
		else :
			# Default
			self.send_response(400)
			self.end_headers()
			json.dump({'msg': 'Bad Request'}, self.wfile)


server = HTTPServer(("localhost", PORT), MyRequestHandler)
print "server started"
server.serve_forever()
