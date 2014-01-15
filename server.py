import os.path
import tornado.ioloop, tornado.httpserver, tornado.web, tornado.websocket
from config import GameConfig

OS = os.path.dirname(__file__)
STATIC = os.path.join(OS, "static")
AUDIO = os.path.join(OS, "audio")
IMAGES = os.path.join(OS, "images")
GAME = os.path.join(OS, "html/game.html")
MISTAKE = os.path.join(OS, "html/error.html")

level_1 = GameConfig()

class TarmHandler(tornado.web.RequestHandler):

	def get(self):
		self.render(GAME, config = level_1)

	def write_error(self, code, **kwargs):
		self.render(MISTAKE)

class TarmSocket(tornado.websocket.WebSocketHandler):

	def open(self, *args):
		self.stream.set_nodelay(True)

	def on_message(self, message):
		print("Message from browser:", message)


def start_server():

	tarm_app = tornado.web.Application(handlers=[
		(r"/", TarmHandler),
		(r"/websocket", TarmSocket),
	    (r"/images/(.*)", tornado.web.StaticFileHandler, { "path": IMAGES }),
	    (r"/music/(.*)", tornado.web.StaticFileHandler, { "path": AUDIO })
	    ],
	    debug=True, gzip=True, static_path=STATIC)

	tornado.httpserver.HTTPServer(tarm_app).listen(8000)
	print("Starting server.")
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	start_server()
