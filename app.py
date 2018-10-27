import os, sys
from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
	if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.challenge'):
		if not request.args.get('hub.verify_token') == 'hello':			
			return 'Verification tokem mismatch', 403
			print('dd')
		return request.args['hub.challenge'], 200
	return 'hello ', 200


@app.route('/', methods=['POST'])
def webhook():	
	data = request.get_json()		
	log(data)
	return "ok", 200


def log(message):
	print(message)
	sys.stdout.flush()


if __name__ == '__main__':
	app.run(debug=True, port=80)