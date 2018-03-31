class Telemetry:
	def __init__(self):
		self.name = 'hello'

	def bind_socket(self, socket):
		print('binding socekt')
		self.socket = socket;

	def emit(self, event, payload):
		self.socket.emit(event, payload)

	def subscribe(self, event, cb):
		self.socket.on_event(event, cb)

Telemetry = Telemetry()


class Input:
	def init():
		Telemetry.subscribe('action', self.handle_action)
		self.input_state = {}
		self.action_callbacks = []

	def handle_action(self, data):
		if data == 'left':
			sefl.input_state[left] = true
		for cb in action_callbacks:
			cb(data)

	def subscribe(self, cb):
		self.action_callbacks.append(cb)

	def poll(action):
		return self.input_state[action]