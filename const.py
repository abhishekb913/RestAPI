SERVER = "localhost" # Database server name
USERNAME = "root" # MySQL user name
PASSWORD = "qwerty" # MySQL password
DATABASE_NAME = "db" # Database name
PORT = 8080 # port for http server

# All the rules must be present
def checkRuleALL(rule, data):
	if len(rule) != len(data):
		return False
	else:
		for key in rule.iterkeys():
			if not(key in data):
				return False
		return True

# Either of the rule could be present
def checkRuleEITHER(rule, data):
	if len(rule) < len(data):
		return False
	else:
		for key in data.iterkeys():
			if not(key in rule):
				return False
		return True