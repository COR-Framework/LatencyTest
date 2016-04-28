import threading

import time

from cor.api import CORModule, Launcher
from cor.comm import TCPSocketNetworkAdapter
from test_pb2 import Request, Reply


class Responder(CORModule):

	def respond(self, message):
		reply = Reply()
		reply.data = "Hi"
		self.messageout(reply)
		print(message.data)

	def __init__(self, network_adapter=None, *args, **kwargs):
		super().__init__(network_adapter, *args, **kwargs)
		self.register_type("Reply", Reply)
		self.register_type("Request", Request)
		self.add_topic("Request", self.respond)


responder = Launcher()
responder.launch_module(Responder, network_adapter=TCPSocketNetworkAdapter(hostport="127.0.0.1:6091"))
responder.link_external("Reply", "127.0.0.1:6090")
