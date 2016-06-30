from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
import json
from user import User
from student import Student

class MyRequestHandler (BaseHTTPRequestHandler) :

	def do_GET(self) :
		if self.path == "/student" :
			#send response code:
			self.send_response(200)
			#send headers:
			self.send_header("Content-type:", "text/html")
			self.end_headers()
			#send response:
			# json.dump(me, self.wfile)
		else :
			self.send_response(400)
			self.end_headers()
			json.dump({'msg': 'Bad Request'}, self.wfile)

	def do_POST(self) :
		data = self.rfile.read(int(self.headers['Content-Length']))
		data = json.loads(data)
		if self.path == "/register" :
			u = User()
			response = u.register(data)
		elif self.path == "/login" :
			u = User()
			response = u.login(data)
		elif self.path == "/createStudent" :
			# print self.headers.getheader('Authorization')
			s = Student()
			response = s.create(data)
		else :
			response = {"status" : 400, "msg" : "Bad Request"}
		self.send_response(response["status"])
		self.end_headers()
		json.dump(response, self.wfile)


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