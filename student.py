import MySQLdb
from const import *

class Student(object):
	def __init__(self):
		self.db = MySQLdb.connect(SERVER,USERNAME,PASSWORD,DATABASE_NAME)
		self.cursor = self.db.cursor()

	# Create student record
	def create(self, data):
		# Checking rules
		rule = {"name" : 1, "class" : 1, "section" : 1}
		if not(checkRuleALL(rule, data)):
			return {"status" : 400, "msg" : "Wrong input"}
		try:
			self.cursor.execute("INSERT INTO students (name, class, section) VALUES ('"+data["name"]+"', "+str(data["class"])+", '"+data["section"]+"')")
			self.db.commit()
			return {"status" : 200, "msg" : "OK"}
		except:
			self.db.rollback()
			return {"status" : 500, "msg" : "DB error"}

	# Update a student's record
	def update(self, studentID, data):
		# Checking rules
		rule = {"name" : 1, "class" : 1, "section" : 1}
		if not(checkRuleEITHER(rule, data)) or len(data) == 0:
			return {"status" : 400, "msg" : "Wrong input"}
		query = ""
		for key, value in data.items():
			if type(value) is int:
				query += key +"="+ str(value) +","
			else:
				query += key +"='"+ str(value) +"',"
		if query:
			query = query.rstrip(",")
		# Check if record exists
		result = self.cursor.execute("SELECT * FROM students WHERE id = "+str(studentID))
		if result == 0:
			return {"status" : 404, "msg" : "Record Not Found"}
		else:
			try:
				self.cursor.execute("UPDATE students SET "+query+" where id = "+str(studentID))
				self.db.commit()
				return {"status" : 200, "msg" : "OK"}
			except:
				self.db.rollback()
				return {"status" : 500, "msg" : "DB error"}

	# Delete student record
	def delete(self, studentID):
		try:
			result = self.cursor.execute("DELETE FROM students where id = "+str(studentID))
			self.db.commit()
			if result == 0:
				return {"status" : 404, "msg" : "Record Not Found"}
			else :
				return {"status" : 200, "msg" : "OK"}
		except:
			self.db.rollback()
			return {"status" : 500, "msg" : "DB error"}

	# Get student information
	def getDetails(self, studentID):
		result = self.cursor.execute("SELECT * FROM students WHERE id = "+str(studentID))
		if result == 0:
			return {"status" : 404, "msg" : "Record Not Found"}
		else:
			results = self.cursor.fetchall()
			response = {}
			for row in results:
				response["studentID"] = row[0]
				response["name"] = row[1]
				response["class"] = row[2]
				response["section"] = row[3]
			response["status"] = 200
			return response