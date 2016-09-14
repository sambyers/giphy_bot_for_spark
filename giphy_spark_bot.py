import pyCiscoSpark
import giphypop
from flask import Flask, request
import re

spark_access_token = "NDI5OTU4YjYtY2VhYS00YTk0LWI5ZDQtNjI4NGQ2YjAzNzBlNDI0YmY5OTYtNzcw"

# RECEIVE WEBHOOK POST
app = Flask(__name__)

@app.route('/', methods=['GET' , 'POST'])
def index():
	if request.method == 'GET':
		return "GET successful."
	if request.method == 'POST':
		# We have to force true here because Spark isn't sending us Content-Type: application/json
		data = request.get_json(force=True)

		msg_id = data["data"]["id"]
		room_id = data["data"]["roomId"]
		person_email = data["data"]["personEmail"]

		if msg_id:
			# Get the message by ID from Spark
			spark_msg = pyCiscoSpark.get_message(spark_access_token,msg_id)
			spark_msg = spark_msg['text']
			spark_msg = re.sub('giphy ', '', spark_msg)
		if spark_msg:
			# Get a gif from Giphy with the terms found in the message
			term = spark_msg
			g = giphypop.Giphy()
			gif = g.translate(term)
			gif_media_url = gif.media_url

		if gif_media_url:
			# Post the gif file back to the Spark room the bot was mentioned in
			file_resp = pyCiscoSpark.post_file(spark_access_token,room_id,gif_media_url)
			print("GIF served up to " + person_email)
		return "200 OK"
	else:
		return "404 NOT FOUND"