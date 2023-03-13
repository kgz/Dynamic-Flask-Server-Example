

from typing import TYPE_CHECKING
from flask import Response, jsonify

from .wrapper import register_api

if TYPE_CHECKING:
	from app import App
		
# Path: Api\test\test
@register_api
def test(app: 'App') -> Response:
	# can access things like app.database, app.config, etc...
	return jsonify({"test": "test"})

# Path: Api\test\test2
@register_api
def test2(app: 'App') -> Response:
	# can access things like app.database, app.config, etc...
	return jsonify({"test": "test2"})



