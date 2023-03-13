from Server.Server import Server


class App:
	def __init__(self) -> None:

		# self.database = Database()
		# self.config = Config()
		# etc...
		self.config = {
			"hello": "world"
		}
		self.server = Server(__name__, self)
		

	def run(self) -> None:
		self.server.run('0.0.0.0', 5000, debug=False)


app = App()


def main() -> None:
	app.run()

if __name__ == "__main__":
	r = App()

	import hupper
	from waitress import serve
	h = hupper.start_reloader("app.main")
	h.watch_files(["/server", "/modules", "/Templates"])
	serve(r.server, host="0.0.0.0", port=80, threads=4) 