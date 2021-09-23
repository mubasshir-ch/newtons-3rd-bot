import jwt
import requests
import json
import datetime
from pytz import timezone
from time import time

UTC = timezone("Asia/Dhaka")

# Enter your API key and your API secret
API_KEY = 'BixyChqjQemIdJ-3Li3Qnw'
API_SEC = 'oNXbtJsnk0KkbJyYBlmMiwmnhYAHKnebwj7i'

# create a function to generate a token
# using the pyjwt library
def generateToken():
	token = jwt.encode(
		
		# Create a payload of the token containing
		# API Key & expiration time
		{'iss': API_KEY, 'exp': time() + 5000},
		
		# Secret used to generate token signature
		API_SEC,
		
		# Specify the hashing alg
		algorithm='HS256'
	)
	return token


# create json data for post requests
meetingdetails = {"topic": "PhO Class "+str(datetime.datetime.now(UTC).strftime("%D")),
				"type": 2,
				"start_time": str(datetime.datetime.now(UTC).strftime("%Y-%m-%dT%H: %M: %S")),
				"duration": "45",
				"timezone": "Asia/Dhaka", 
				"agenda": "test",

				"recurrence": {"type": 1,
								"repeat_interval": 1
								},
				"settings": {"host_video": "true",
							"participant_video": "true",
							"join_before_host": "False",
							"mute_upon_entry": "False",
							"watermark": "true",
							"audio": "voip",
							"auto_recording": "cloud"
							}
				}

# send a request with headers including
# a token and meeting details
def createMeeting():
	headers={'authorization': 'Bearer %s' %generateToken(),'content-type': 'application/json'}
	r = requests.post(f'https://api.zoom.us/v2/users/me/meetings',headers=headers,data=json.dumps(meetingdetails))
	# print("\n creating zoom meeting ... \n")
	y=json.loads(r.text)
	return y
	# join_URL = y["join_url"]
	# meetingPassword = y["password"]


# run the create meeting function
#createMeeting()


#print(meetingdetails["start_time"])
#print(meetingdetails["topic"])