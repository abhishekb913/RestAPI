My system has Python 2.7.9
Install MySQL module to access MySQL database

Change the database credentials in file const.py appropriately to connect to your local database
Import the sql dump file "db_2016-07-01.sql" to create tables in the desired database

Run listener.py script (A simple HTTP server starts)
PORT where the server listens is set 8080. Change it in const.py if you get error in creating socket at that port
Also change port from 8080 in the API calls you make if you had changed port in const.py

Use Postman(Chrome extension) to make API calls as it would be easy to set Basic Auth parameters required for authentication

About the APIs
Rules are set on the input data. Some input require all input parameters mentioned in "Raw data sent in body" while some do not require all input parameters. It is mentioned which API require all input parameters and which can work without all being sent. You get {"msg": "Wrong input"} as response if rules are not followed for input data.
Input data is sent in body as raw input of normal text type
Change input data appropriately while making API calls.
Appropriate response is sent and HTTP status codes are set appropriately for any API call made

Following functionality is provided by the service
1. Register
	Register a user

	API call(POST) - http://localhost:8080/register
	Raw data sent in body(Require All) - {"name": "Abhishek", "phone" : "9468700066", "email" : "abhishekb913@gmail.com"}
	Sample Response - {"otp": "PLU71A", "phone": "9468700066", "msg": "OK"} if everything is fine
	Response - {"msg": "User Already registered"} if user already registered with given phone number

	You get an OTP which will be used to log in

2. Generate OTP
	OTP is returned after register but a user may not login at that time and leaves the app/site. He cannot register again. OTP generation would be required every time user tries to login again

	API call(POST) - http://localhost:8080/generateOTP
	Raw data sent in body(Require All) - {"phone" : "9468700068"}
	Sample Response - {"otp": "D1TLOO", "phone": "9468700066", "msg": "OK"} if everything is fine
	Response - {"msg": "User Not registered"} if user is not registered

3. Login
	A registered user can login providing his phone number and otp generated.

	API call(POST) - http://localhost:8080/login
	Raw data sent in body(Require All) - {"phone" : "9468700066", "otp" : "D1TLOO"}
	Sample Response - {"msg": "OK", "auth": "ffjB89mlM87T3pJnV7EBErZ9w5gM32"}
	Response - {"msg": "User Not registered"} if user is not registered
	Response - {"msg" : "Wrong OTP"} if OTP entered is wrong

	A new authentication token is generated everytime user logs in and it will be stored and sent in Basic Authentication to authenticate user. Authentication token is set only after user logs in and not after he registers

Once a user has logged in he can perform following operations

Before making any operation user requires authorization
To Set Authorization in API call
In Authorization choose Basic Auth (I am using Postman to make API calls and setting authorization appropriately)
Set username as phone number and password and auth value corresponding to a user

You get following response if authentication fails - {"msg" : "Authorization Failed"}

1. Create Student Record
	API call(POST) - http://localhost:8080/createStudent
	Raw data sent in body(Require All) - {"name" : "abhishek", "class" : "5", "section" : "D"}
	Sample Response - {"msg": "OK"}

2. Get Student Details
	Get details of a student

	API call(GET) - http://localhost:8080/student?id=3 
	Here id represent the student record id whose details we are fetching

	Sample Response(Does Not Require All) - {"section": "D", "studentID": 1, "name": "abhishek", "class": 5}
	Response - {"msg": "Record Not Found"} if no record found

3. Update Student Entry
	API call(PUT) - http://localhost:8080/updateStudent?id=3
	Here id represent the student record id whose details we are updating

	We can update either name or class or section or a combination of these
	Raw data sent - {"name" : "abhishek", "class" : "5", "section" : "D"}
	Sample Response - {"msg": "OK"} if everything is fine
	Response - {"msg": "Record Not Found"} if record not found


4. Delete student record
	API call(DELETE) - http://localhost:8080/student?id=4
	Sample Response - {"msg": "OK"} if record deleted successfully
	Response - {"msg": "Record Not Found"} if record not found


