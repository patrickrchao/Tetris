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


LEFT= 'left',
RIGHT= 'right',
R_CCW= 'ccw',
R_CW= 'cw',
SOFT= 'soft',
HARD= 'hard',
HOLD= 'hold'


ACTION_MAP = {
	'arrowleft': 	LEFT,
	'arrowright': 	RIGHT,
	'arrowup': 		R_CW,
	'arrowleft': 	LEFT,
	'c': 			R_CW,
	'z': 			R_CCW,
	'shift': 		HOLD,
	' ': 			HARD,
	'arrowdown':  	SOFT
}


