import MySQLdb
import string
import random
from const import *

class User(object):
	# Setting db connection
	def __init__(self):
		self.db = MySQLdb.connect(SERVER,USERNAME,PASSWORD,DATABASE_NAME)
		self.cursor = self.db.cursor()

	# Register user. Takes phone, name, email
	# Generates OTP
	# Return OTP
	def register(self, data):
		# Checking rules
		rule = {"phone" : 1, "name" : 1, "email" : 1}
		if not(checkRuleALL(rule, data)):
			return {"status" : 400, "msg" : "Wrong input"}
		#checking if phone number already exists
		result = self.cursor.execute("SELECT * FROM user where phone = '"+data["phone"]+"'")
		if result == 0:
			otp = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
			try:
				# Storing registered user information
				self.cursor.execute("INSERT INTO user (name, phone, email, OTP) VALUES ('"+data["name"]+"', '"+data["phone"]+"', '"+data["email"]+"', '"+otp+"')")
				self.db.commit()
				return {'otp' : otp, 'phone' : data["phone"], "status" : 200, "msg" : "OK"}
			except:
				self.db.rollback()
				return {"status" : 500, "msg" : "DB error"}
		else :
			return {"status" : 400, "msg" : "User Already registered"}

	# Generate OTP if user logs out or did not log in after register.
	def generateOTP(self, data):
		# Checking rules
		rule = {"phone" : 1}
		if not(checkRuleALL(rule, data)):
			return {"status" : 400, "msg" : "Wrong input"}
		#checking if use registered
		result = self.cursor.execute("SELECT * FROM user where phone = '"+data["phone"]+"'")
		if result == 0:
			return {"status" : 400, "msg" : "User Not registered"}
		else:
			otp = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
			try:
				self.cursor.execute("UPDATE user SET OTP = '"+otp+"' WHERE phone = '"+data["phone"]+"'")
				self.db.commit()
				return {'otp' : otp, 'phone' : data["phone"], "status" : 200, "msg" : "OK"}
			except:
				self.db.rollback()
				return {"status" : 500, "msg" : "DB error"}

	# Login user. Takes phone and OTP
	def login(self, data):
		# Checking rules
		rule = {"phone" : 1, "otp" : 1}
		if not(checkRuleALL(rule, data)):
			return {"status" : 400, "msg" : "Wrong input"}
		# Checking if user registered
		result = self.cursor.execute("SELECT OTP FROM user where phone = '"+data["phone"]+"'")
		if result == 0 :
			return {"status" : 400, "msg" : "User Not Registered"}
		else :
			# Checking if OTP matches phone
			results = self.cursor.fetchall()
			for row in results:
				if row[0] != data["otp"]:
					return {"status" : 400, "msg" : "Wrong OTP"}
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

	# User authentication
	def authenticate(self, phone, auth):
		result = self.cursor.execute("SELECT * FROM user where phone = '"+phone+"' AND auth = '"+auth+"'")
		if result == 0:
			return False
		else:
			return True





