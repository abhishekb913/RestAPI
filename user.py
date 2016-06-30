import MySQLdb
import string
import random

class User(object):
	def __init__(self):
		self.db = MySQLdb.connect("localhost","root","qwerty","db")
		self.cursor = self.db.cursor()

	def register(self, data):
		#checking if phone number already exists
		result = self.cursor.execute("SELECT * FROM user where phone = '"+data["phone"]+"'")
		if result == 0:
			otp = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
			try:
				self.cursor.execute("INSERT INTO user (name, phone, email, OTP) VALUES ('"+data["name"]+"', '"+data["phone"]+"', '"+data["email"]+"', '"+otp+"')")
				self.db.commit()
				return {'otp' : otp, 'phone' : data["phone"], "status" : 200, "msg" : "OK"}
			except:
				self.db.rollback()
				return {"status" : 500, "msg" : "DB error"}
		else :
			otp = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
			results = self.cursor.fetchall()
			for row in results:
				if row[5] is not None:
					return {"status" : 400, "msg" : "User Already registered"}
			try:
				self.cursor.execute("UPDATE user SET OTP = '"+otp+"' WHERE phone = '"+data["phone"]+"'")
				self.db.commit()
				return {'otp' : otp, 'phone' : data["phone"], "status" : 200, "msg" : "OK"}
			except:
				self.db.rollback()
				return {"status" : 500, "msg" : "DB error"}

	def login(self, data):
		#Checking if OTP matches phone
		result = self.cursor.execute("SELECT * FROM user where phone = '"+data["phone"]+"' AND OTP = '"+data["otp"]+"'")
		if result == 0 :
			return {"status" : 400, "msg" : "Either phone or OTP is wrong"}
		else :
			try:
				#create auth
				auth = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits + str(hash(data["phone"] + data["otp"]))) for _ in range(30))
				#store auth
				self.cursor.execute("UPDATE user SET auth = '"+auth+"' WHERE phone = '"+data["phone"]+"'")
				self.db.commit()
				return {'auth' : auth, "status" : 200, "msg" : "OK"}
			except:
				self.db.rollback()
				return {"status" : 500, "msg" : "DB error"}

	def authenticate(self, userID, auth):
		result = self.cursor.execute("SELECT * FROM user where id = '"+userID+"' AND auth = '"+auth+"'")
		if result == 0:
			return False
		else:
			return True





