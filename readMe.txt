My system has Python 2.7.9
Install MySQL module to access MySQL database

Import the sql dump file "db_2016-07-01.sql" to create tables in the desired database
Change the database credentials in file const.py appropriately to connect to your local database

Run listener.py script (A simple HTTP server starts)
PORT where the server listens is set 8080. Change it in const if you get error in creating socket at that port
Also change port from 8080 in the API calls you make if you had changed port in const

Use Postman(Chrome extension) to make API calls as it would be easy to set Basic Auth parameters required for authentication

Following functionality is provided by the service
1. Register
	Register a user

	API call(POST) - http://localhost:8080/register
	Raw data sent in body - {"name": "Abhishek", "phone" : "9468700066", "email" : "abhishekb913@gmail.com"}
	Sample Response - {"otp": "PLU71A", "phone": "9468700066", "msg": "OK"} if everything is fine
	Response - {"msg": "User Already registered"} if user already registered

	HTTP status codes are set appropriately

2. Generate OTP
	OTP is returned after register but a user may not login at that time. He cannot register again. OTP generation would be required every time user tries to login again

	API call(POST) - http://localhost:8080/generateOTP
	Raw data sent - {"phone" : "9468700068"}
	Sample Response - {"otp": "D1TLOO", "phone": "9468700066", "msg": "OK"} if everything is fine
	Response - {"msg": "User Not registered"} if user is not registered

3. Login
	A registered user can login providing his phone number and otp generated.

	API call(POST) - http://localhost:8080/login
	Raw data sent - {"phone" : "9468700066", "otp" : "D1TLOO"}
	Sample Response - {"msg": "OK", "auth": "ffjB89mlM87T3pJnV7EBErZ9w5gM32"}

	A new authentication token is generated everytime user logs in and it will be stored and sent in Basic Authentication to authenticate user. Authentication token is set only after user logs in not after he registers

Once a user has logged in he can perform following operations
For Authorization
In Authorization choose Basic Auth
Set username as phone number and password and auth value corresponding to a user

1. Create Student Record
	API call(POST) - http://localhost:8080/createStudent
	Raw data sent - {"name" : "abhishek", "class" : "5", "section" : "D"}
	Sample Response - {"msg": "OK"}

2. Get Student Details
	Get details of a student

	API call(GET) - http://localhost:8080/student?id=3 
	Here id represent the student record id whose details we are fetching

	Sample Response - {"section": "D", "studentID": 1, "name": "abhishek", "class": 5}
	Response - {"msg": "No record found"} if no record found

3. Delete student record
	API call(DELETE) - http://localhost:8080/student?id=4
	Sample Response - {"msg": "OK"} if record deleted
	Response - {"msg": "Record Not Found"} if record not found


