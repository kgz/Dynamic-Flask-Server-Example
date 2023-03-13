

import random
from typing import TYPE_CHECKING, Tuple, Union

from flask import Response, jsonify, request
from .wrapper import register_api
import requests  # this is just for example please do not actually use requests in a flask app

if TYPE_CHECKING:
	from app import App


@register_api
def get(app: 'App') -> Response:
	"""
	@method GET
	"""
	return jsonify(app.config)

# this will only work on post requests, if you try in the browser it will not work
@register_api
def set(app: 'App') -> Union[Response, Tuple[Response, int]]:
	"""
	@method POST
	"""
	# get config from request
	if not request.json:
		return jsonify({"error": "No config provided"}), 400
	# set config
	app.config = request.json
	return jsonify(app.config)

# used to mimic the above function, but with a post request
@register_api
def mimic_post(app: 'App') -> Response:
	"""
	@method GET
	"""
	dummy_config = {
		"hello": "world" + str(random.randint(100, 10000))
	}
	
	requests.post("http://localhost:5000/api/config/set", json=dummy_config)
	return jsonify(app.config)

@register_api
def routes(app: 'App') -> Response:
	"""
	@method GET
	"""
	return jsonify(app.server.api_list)
