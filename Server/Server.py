import inspect
import os
import re
from typing import TYPE_CHECKING, List
from flask import Flask, render_template
from Api import api_list
if TYPE_CHECKING:
	from app import App


def index(app:'App') -> str:
	return render_template("index.html", app=app)


class Server(Flask):
	"""."""
	
	def __init__(self, name, app,  *args, **kwargs) -> None:
		super().__init__(name, *args, **kwargs)

		self.api_list: List = []
		self.endpoint_factory: List = []

		self.secret_key = os.urandom(24)
		self.debug = True
		self.app = app
		# self.add_url_rule("/<path:_>/", "index", index)
		self.add_url_rule("/", "index", index, defaults={'app': app})
		# # self.add_url_rule("/notFound", "fourofour", api_fourofour)
		# self.add_url_rule("/api/<_>/<path>", "api_fourofour", api_fourofour)
		# self.add_url_rule("/api/<path>", "api_fourofour", api_fourofour)
		# # self.register_error_handler(500, Exception)
		# self.before_request(self.before)
		# self.after_request(self.after)

	
		self.setupApis()


		# self.login_manager = LoginManager()
		# self.login_manager.init_app(self)
		# self.login_manager.user_loader(self.load_user)
		# self.login_manager.anonymous_user = AnonymousUser


	def setupApis(self) -> None:

		for _api, func in api_list.items():
			# api_list keys are module + function name, we just want func name
			api = _api[len(func.__module__) + 1 :]
			# setup defaults.
			requireAdmin = False
			requireLogin = False
			if not func.__doc__:
				func.__doc__ = ""

			# remove base module name
			module = func.__module__[4:]

			# search for @admin in docstring
			adminsearch = re.search("@admin(?:\s*)(.*)", func.__doc__)
			if adminsearch and adminsearch.group(1).strip() != "false":
				requireAdmin = True

			# search for @login in docstring
			loginsearch = re.search("@login(?:\s*)(.*)", func.__doc__)
			if loginsearch and loginsearch.group(1).strip() != "false":
				requireLogin = True

			# search for @methods in docstring
			methods = ["GET", "POST", "PUT", "DELETE"]
			methodsSearch = re.search("@method(?:s*) (.*)", func.__doc__)
			if methodsSearch and len(methodsSearch.groups()) > 0:
				methods = [x.upper().strip() for x in methodsSearch.group(1).split(",")]
			# # if @admin or @login pass route through middleware funcion to check login/admin status
			# if requireAdmin or requireLogin:
			# 	self.add_url_rule(
			# 		"/api/" + module + "/" + api,
			# 		api,
			# 		self.loginPassthrough,
			# 		defaults={"func": func, "app": self.app, "admin": requireAdmin},
			# 		methods=methods,
			# 	)
			# else just add as a normal route
			print("Adding route: /api/" + module + "/" + api + " with methods: " + str(methods) + " and admin: " + str(requireAdmin))
			self.add_url_rule(
				"/api/" + module + "/" + api,
				module + "." + api,
				func,
				defaults={"app": self.app}, #add any default argument you want to pass throught to jinja here
				methods=methods,
			)

			self.api_list.append(
				{
					"url": "/api/" + module + "/" + api,
					"admin": requireAdmin,
					"logged_in": requireLogin or requireAdmin,
					"methods": methods,
					"module": module,
					"func": api,
					"debugUrl": "vscode://file/"
					+ inspect.getfile(func)
					+ ":"
					+ str(inspect.getsourcelines(func)[1])
					+ ":"
					+ "0",
					"module": func.__module__
					# 'annotations': func.__annotations__
				}
			)


	# def loginPassthrough(self, func, admin, *args, **kwargs) -> callable:
	# 	if admin and not current_user.admin:
	# 		return "Not Authorised", 403
	# 	if not current_user.is_authenticated():
	# 		return "Not Authorised", 403
	# 	try:
	# 		return func(*args, **kwargs)
	# 	except Exception as e:
	# 		return error(e)

	# def before(self)->BeforeRequestCallable:
	# 	#!DEBUGGING ONLY PLEASE REMOVE
	# 	if not current_user.is_authenticated():
	# 		login_user(self.load_user(0))
	# 	g.request_start_time = time.time()
	# 	g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)
	# 	totest = request.path.strip("/")
	# 	if totest.startswith("admin"):
	# 		if not current_user.is_authenticated() or not current_user.admin:
	# 			return redirect("/not_logged_in")

	# def after(self, response: AfterRequestCallable) -> AfterRequestCallable:
	# 	#TODO - if response is greater then x then log.
	# 	if g:
	# 		response.headers["X-Response-Time"] = g.request_time()
	# 	# response.headers.add("Access-Control-Allow-Origin", "*")
	# 	try:
	# 		self.app.database.insert(
	# 			"INSERT INTO access_log (remote_address, path, method, status, request_time, endpoint, browser, language, platform, version) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
	# 			(request.remote_addr, request.path, request.method,  response.status_code, g.request_time(), request.endpoint, request.user_agent.browser, request.user_agent.language, request.user_agent.platform, request.user_agent.version))
	# 	except Exception as e:
	# 		Error(e)

		# return response

