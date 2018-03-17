class Telemetry:
	def __init__(self):
		self.name = 'hello'

	def bind_socket(self, socket):
		print('binding socekt')
		self.socket = socket;

	def emit(self, event, payload):
		self.socket.emit(event, payload)

Telemetry = Telemetry()