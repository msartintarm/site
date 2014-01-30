import os.path
from tornado import ioloop, httpserver, web, websocket, template
from config import GameConfig

OS = os.path.dirname(__file__)

def server_path(uri):
	return os.path.join(OS, uri)

def static_path(uri):
	return { "path": server_path("static/" + uri) }

level_1 = GameConfig()

class TarmHandler(web.RequestHandler):

	def get(self):
		self.render(server_path("html/game.html"), config = level_1)

	def write_error(self, code, **kwargs):
		self.render(server_path("html/error.html"))

class TarmSocket(websocket.WebSocketHandler):

	def open(self, *args):
		self.stream.set_nodelay(True)
		print("Socket opened.")

	def on_message(self, message):
		print("Message from browser:", message)
		if "load-config" in message:
			self.write_message(template.Loader('html').load('config.html').generate(config=level_1))

		elif "load-about" in message:
			self.write_message(template.Loader('html').load('about.html').generate())

		elif "load-audio" in message:
			self.write_message(template.Loader('html').load('audio.html').generate())

def start_server():

	tarm_app = web.Application(handlers=[
		(r"/", TarmHandler),
		(r"/socket", TarmSocket),
	    (r"/images/(.*)", web.StaticFileHandler, static_path("images")),
	    (r"/textures/(.*)", web.StaticFileHandler, static_path("textures")),
	    (r"/music/(.*)", web.StaticFileHandler, static_path("audio"))
	    ],
	    debug=True, gzip=True, static_path=server_path("static"))

	httpserver.HTTPServer(tarm_app).listen(8000)
	print("Starting server.")
	ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	start_server()
