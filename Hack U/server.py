import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.ioloop import PeriodicCallback

from tornado.options import define, options, parse_command_line

define("port", default = 8080, help = "run on the given port", type = int)

class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render("index.html")

class SendWebSocket(tornado.websocket.WebSocketHandler):
    #on_message -> receive data
    #write_message -> send data

    #index.htmlでコネクションが確保されると呼び出される
    def open(self):
        self.i = 0
        self.callback = PeriodicCallback(self._send_message, 400) #遅延用コールバック
        self.callback.start()
        print ("WebSocket opened")

    #クライアントからメッセージが送られてくると呼び出される
    def on_message(self, message):
        print (message)

    #コールバックスタートで呼び出しが始まる
    def _send_message(self):
        self.i += 1
        self.write_message(str(self.i%2))

    #ページが閉じ、コネクションが切れる事で呼び出し
    def on_close(self):
        self.callback.stop()
        print ("WebSocket closed")

app = tornado.web.Application([
    (r"/", IndexHandler),
    (r'/ws', SendWebSocket),
    (r'/(.*)', tornado.web.StaticFileHandler, {'path': ''})
])

if __name__ == "__main__":
    parse_command_line()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
