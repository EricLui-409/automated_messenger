import os
import redis
import main
import config as cf
from functools import wraps
from flask import Flask, jsonify, request, Response
from rq import Queue, Connection

app = Flask(__name__)

# keep trying to connect to redis until success
while True:
	try:
		redis_url = cf.REDIS_URL
		conn = redis.from_url(redis_url)
		break
	except redis.ConnectionError:
		pass

q = Queue(cf.REDIS_QUEUE_NAME, connection=conn)

def requires_token(f):
	@wraps(f)
	def decorator(*args, **kwargs):
		response_object = {
			"status": cf.API_FAILED,
			"message": cf.API_AUTH_FAILED
		}
		if "Authorization" in request.headers:
			token = request.headers.get("Authorization")
			if token == "Token token=" + cf.TOKEN:
				return f(*args, **kwargs)
			return jsonify(response_object), 401
		return jsonify(response_object), 403
	return decorator

# server health check
@app.route(cf.HEALTH_CHECK_ROUTE, methods=["GET"])
def health_check():
	resp = Response(cf.API_PONG)
	resp.headers["Content-Type"] = "text/html"
	return resp

@app.route(cf.WHATSAPP_CHECK_ROUTE, methods=["POST"])
@requires_token
def wtsapp_check(phone_number, ret_url):
	service_type = cf.WHATSAPP_CHECK
	arg_list = [phone_number]
	task = q.enqueue(
		main.run_task, 
		service_type, 
		ret_url, 
		arg_list, 
		result_ttl=5000
		)

	response_object = {
		"status": cf.API_SUCCESS,
		"data": {
			"task_id": task.get_id(),
			"task_name": service_type
		}
	}
	return jsonify(response_object), 202

@app.route(cf.WHATSAPP_MESSAGE_ROUTE, methods=["POST"])
@requires_token
def wtsapp_message(phone_number, message, ret_url):
	service_type = cf.WHATSAPP_MESSAGE
	arg_list = [phone_number, message]
	task = q.enqueue(
		main.run_task, 
		service_type, 
		ret_url, 
		arg_list, 
		result_ttl=5000
		)

	response_object = {
		"status": cf.API_SUCCESS,
		"data": {
			"task_id": task.get_id(),
			"task_name": service_type
		}
	}
	return jsonify(response_object), 202

@app.route(cf.WHATSAPP_LOGIN_ROUTE, methods=["POST"])
@requires_token
def wtsapp_login(ret_url):
	service_type = cf.WHATSAPP_LOGIN
	arg_list = []
	task = q.enqueue(
		main.run_task, 
		service_type, 
		ret_url, 
		arg_list, 
		result_ttl=5000
		)

	response_object = {
		"status": cf.API_SUCCESS,
		"data": {
			"task_id": task.get_id(),
			"task_name": service_type
		}
	}
	return jsonify(response_object), 202

@app.route(cf.WHATSAPP_LOGOUT_ROUTE, methods=["POST"])
@requires_token
def wtsapp_logout(ret_url):
	service_type = cf.WHATSAPP_LOGOUT
	arg_list = []
	task = q.enqueue(
		main.run_task, 
		service_type, 
		ret_url, 
		arg_list, 
		result_ttl=5000
		)

	response_object = {
		"status": cf.API_SUCCESS,
		"data": {
			"task_id": task.get_id(),
			"task_name": service_type
		}
	}
	return jsonify(response_object), 202

@app.route("/'", methods=["GET", "POST"], defaults={'path': ''})
@app.route("/<string:path>", methods=["GET", "POST"])
@app.route("/<path:path>", methods=["GET", "POST"])
@requires_token
def catch_all(path):
	return cf.API_INVALID_PATH, 404
