import threading

import time

from cor.api import CORModule, Launcher
from cor.comm import TCPSocketNetworkAdapter
from test_pb2 import Request, Reply


class Requester(CORModule):

	def acknowledge(self, message):
		took = (time.time() - self.time_request) * 1000000
		print(took, "us")
		if self.average is None:
			self.average = took
		else:
			self.count += 1
			self.average = (self.average * self.count + took) / (self.count + 1)
		print("Average:", self.average, "us")
		print(message.data)

	def request_worker(self):
		while True:
			time.sleep(1)
			request = Request()
			request.data = "Hello"
			self.messageout(request)
			self.time_request = time.time()

	def __init__(self, network_adapter=None, *args, **kwargs):
		super().__init__(network_adapter, *args, **kwargs)
		self.add_topic("Reply", self.acknowledge)
		self.time_request = 0
		self.average = None
		self.count = 0
		self.register_type("Reply", Reply)
		self.register_type("Request", Request)
		t = threading.Thread(target=self.request_worker)
		t.start()

requester = Launcher()
requester.launch_module(Requester, network_adapter=TCPSocketNetworkAdapter())
requester.link_external("Request", "127.0.0.1:6091")
