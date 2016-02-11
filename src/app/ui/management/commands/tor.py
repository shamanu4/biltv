# -*- encoding: utf-8 -*-
__author__ = 'maxim'

import signal
import time

import tornado.httpserver
import tornado.ioloop

from django.core.management.base import BaseCommand, CommandError

from ui.tornado_main import application
from django.conf import settings


class Command(BaseCommand):
    args = '[port_number]'
    help = 'Starts the Tornado application for message handling.'

    def sig_handler(self, sig, frame):
        """Catch signal and init callback"""
        tornado.ioloop.IOLoop.instance().add_callback(self.shutdown)

    def shutdown(self):
        """Stop server and add callback to stop i/o loop"""
        self.http_server.stop()

        io_loop = tornado.ioloop.IOLoop.instance()
        io_loop.add_timeout(time.time() + 2, io_loop.stop)

    def handle(self, *args, **options):
        if len(args) == 2:
            try:
                port = int(args[1])
            except ValueError:
                raise CommandError('Invalid port number specified')
            try:
                address = str(args[0])
            except ValueError:
                raise CommandError('Invalid port number specified')
        else:
            port = int(settings.TORNADO_PORT)
            address = str(settings.TORNADO_IP)

        self.http_server = tornado.httpserver.HTTPServer(application, ssl_options={
            "certfile": "/etc/ssl/biltv/biltv.itim.net.crt",
            "keyfile":  "/etc/ssl/biltv/biltv.itim.net.key",
            "ca_certs":  "/etc/ssl/biltv/root_bundle.crt",
        })
        self.http_server.listen(port, address)

        # Init signals handler
        signal.signal(signal.SIGTERM, self.sig_handler)

        # This will also catch KeyboardInterrupt exception
        signal.signal(signal.SIGINT, self.sig_handler)

        tornado.ioloop.IOLoop.instance().start()