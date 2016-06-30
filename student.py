import MySQLdb

class Student(object):
	def __init__(self):
		self.db = MySQLdb.connect("localhost","root","qwerty","db")
		self.cursor = self.db.cursor()

	def create(self, data):
		try:
			self.cursor.execute("INSERT INTO students (name, class, section) VALUES ('"+data["name"]+"', '"+data["class"]+"', '"+data["section"]+"')")
			self.db.commit()
			return {"status" : 200, "msg" : "OK"}
		except:
			self.db.rollback()
			return {"status" : 500, "msg" : "DB error"}

	def delete(self, studentID):
		try:
			self.cursor.execute("DELETE FROM students where id = "+studentID)
			self.db.commit()
			return {"status" : 200, "msg" : "OK"}
		except:
			self.db.rollback()
			return {"status" : 500, "msg" : "DB error"}

	def getDetails(self, studentID):
		result = self.cursor.execute("SELECT * FROM students WHERE id = "+ studentID)
		if result == 0:
			return {"status" : 404, "msg" : "No record found"}
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