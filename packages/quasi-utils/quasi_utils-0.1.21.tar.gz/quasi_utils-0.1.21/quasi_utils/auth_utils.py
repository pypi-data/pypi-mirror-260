import json
import os
from http.cookies import SimpleCookie

import jwt
from jwt.exceptions import InvalidSignatureError, DecodeError, ExpiredSignatureError

ACAO = 'Access-Control-Allow-Origin'


def validate_jwt(encoded_jwt, secret):
	try:
		return 200, jwt.decode(encoded_jwt, secret, algorithms='HS256')
	except InvalidSignatureError as e:
		return 401, str(e)
	except DecodeError as e:
		return 403, str(e)
	except ExpiredSignatureError as e:
		return 406, str(e)


def read_cookie(cookie, cookie_name):
	cookie = SimpleCookie(cookie)
	
	return cookie[cookie_name].value


def origin_verification(headers):
	allowed_origins = ['http://localhost:5173', 'https://stockemy.in']
	
	if headers['origin'] not in allowed_origins:
		code, message, origin = 403, 'Invalid origin', '*'
	else:
		code, message, origin = 200, 'Valid origin', headers['origin']
	
	return code, message, origin


def request_verification_flow(headers):
	code, message, origin = origin_verification(headers)
	if code != 200:
		return {'statusCode': code, 'body': json.dumps({'message': message}), 'headers': {ACAO: origin}}
	
	try:
		jwt_token = read_cookie(headers.get('cookie') or headers.get('Cookie'), 'jwt_token')
	except KeyError:
		code, message = 500, 'Missing jwt_token in cookie'
		return {'statusCode': code, 'body': json.dumps({'message': message}), 'headers': {ACAO: origin}}
	
	code, message = validate_jwt(jwt_token, secret=os.environ['JWT_KEY'])
	if code != 200:
		return {'statusCode': code, 'body': json.dumps({'message': message}), 'headers': {ACAO: origin}}
	
	return message, origin
