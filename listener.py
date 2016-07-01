from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
import re
import json
from user import User
from student import Student

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

	def do_GET(self) :
		if re.match("/student\?.*", self.path):
			response = {"status" : 401}
			if self.authenticate():
				params = self.path.split("/student?", 1)[1]
				params = dict(qc.split("=") for qc in params.split("&"))
				if 'id' in params:
					s = Student()
					response = s.getDetails(params['id'])
				else:
					response = {"status" : 400 , "msg" : "Bad Request"}
			self.send_response(response["status"])
			self.end_headers()
			json.dump(response, self.wfile)
		else :
			self.send_response(400)
			self.end_headers()
			json.dump({'msg': 'Bad Request'}, self.wfile)

	def do_POST(self) :
		data = self.rfile.read(int(self.headers['Content-Length']))
		data = json.loads(data)
		u = User()
		if self.path == "/register" :
			response = u.register(data)
		elif self.path == "/login" :
			response = u.login(data)
		elif self.path == "/createStudent" :
			response = {"status" : 401}
			if self.authenticate():
				s = Student()
				response = s.create(data)
		else :
			response = {"status" : 400, "msg" : "Bad Request"}
		self.send_response(response["status"])
		self.end_headers()
		json.dump(response, self.wfile)

	def do_DELETE(self) :
		if re.match("/student\?.*", self.path):
			response = {"status" : 401}
			if self.authenticate():
				params = self.path.split("/student?", 1)[1]
				params = dict(qc.split("=") for qc in params.split("&"))
				if 'id' in params:
					s = Student()
					response = s.delete(params['id'])
				else:
					response = {"status" : 400 , "msg" : "Bad Request"}
			self.send_response(response["status"])
			self.end_headers()
			json.dump(response, self.wfile)
		else :
			self.send_response(400)
			self.end_headers()
			json.dump({'msg': 'Bad Request'}, self.wfile)


server = HTTPServer(("localhost", 8000), MyRequestHandler)
print "server started"
server.serve_forever()



# import MySQLdb

# # Open database connection
# db = MySQLdb.connect("localhost","root","qwerty","localCashboss" )

# # prepare a cursor object using cursor() method
# cursor = db.cursor()

# print cursor.execute("SELECT * FROM cm_brand")

# db.close()