import io from 'socket.io-client';

class TelemetryService {
	init() {
		this.socket = io.connect('127.0.0.1:5000');
		this.socket.on('connect', () => { this.onConnect() });
	}

	onConnect() {
		console.log('socket connected');
	}

	emit(type, payload) {
		this.socket.emit(type, payload);
	}

	addListener(type, cb) {
		this.socket.on(type, cb);
	}
}

export default new TelemetryService();