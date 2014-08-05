import datetime
import json
import time
import urllib

import brukva
import tornado.httpclient
import tornado.ioloop
import tornado.web
import tornado.websocket

from django.conf import settings

c = brukva.Client()
c.connect()


class MainHandler(tornado.web.RequestHandler):
    def check_origin(self, origin):
        return True

    def get(self):
        self.set_header('Content-Type', 'text/plain')
        self.write('Hello. :)')


class MessagesHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        super(MessagesHandler, self).__init__(*args, **kwargs)
        self.client = brukva.Client()
        self.client.connect()
        self.channel = ""

    def check_origin(self, origin):
        return True

    def open(self, thread_id):
        self.channel = thread_id
        self.client.subscribe(self.channel)
        self.client.listen(self.show_new_message)

    def handle_request(self, response):
        pass

    def show_new_message(self, result):
        self.write_message(result.body)

    def on_close(self):
        try:
            self.client.unsubscribe(self.channel)
        except AttributeError:
            pass
        def check():
            if self.client.connection.in_progress:
                tornado.ioloop.IOLoop.instance().add_timeout(
                    datetime.timedelta(0.00001),
                    check
                )
            else:
                self.client.disconnect()
        tornado.ioloop.IOLoop.instance().add_timeout(
            datetime.timedelta(0.00001),
            check
        )

application = tornado.web.Application([
    (r"/", MainHandler),
    (r'/(?P<thread_id>.+)/', MessagesHandler),
])
