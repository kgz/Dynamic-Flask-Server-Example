from typing import Callable

api_list: dict = {}
endpoint_factory:dict = {}

def register_api(func: Callable) -> Callable:
	api_list[func.__module__ + "." + func.__name__] = func
	return func