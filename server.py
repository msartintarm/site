import os.path
from tornado import ioloop, httpserver, web, websocket, template
from config import GameConfig

OS = os.path.dirname(__file__)
STATIC = os.path.join(OS, "static")
AUDIO = os.path.join(OS, "audio")
IMAGES = os.path.join(OS, "images")
GAME = os.path.join(OS, "html/game.html")
MISTAKE = os.path.join(OS, "html/error.html")

level_1 = GameConfig()

class TarmHandler(web.RequestHandler):

	def get(self):
		self.render(GAME, config = level_1)

	def write_error(self, code, **kwargs):
		self.render(MISTAKE)

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

#    {% module Template('config.html', config=config) %}



def start_server():

	tarm_app = web.Application(handlers=[
		(r"/", TarmHandler),
		(r"/socket", TarmSocket),
	    (r"/images/(.*)", web.StaticFileHandler, { "path": IMAGES }),
	    (r"/music/(.*)", web.StaticFileHandler, { "path": AUDIO })
	    ],
	    debug=True, gzip=True, static_path=STATIC)

	httpserver.HTTPServer(tarm_app).listen(8000)
	print("Starting server.")
	ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	start_server()
