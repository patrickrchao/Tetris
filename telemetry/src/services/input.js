import Telemetry from './telemetry';

const ACTION_ENUM = {
	LEFT: 'left',
	RIGHT: 'right',
	R_CCW: 'ccw',
	R_CW: 'cw',
	SOFT: 'soft',
	HARD: 'hard',
	HOLD: 'hold'
};

const ACTION_MAP = {
	arrowleft: 	ACTION_ENUM.LEFT,
	arrowright: ACTION_ENUM.RIGHT,
	arrowup: 	ACTION_ENUM.R_CW,
	c: 			ACTION_ENUM.R_CW,
	z: 			ACTION_ENUM.R_CCW,
	shift: 		ACTION_ENUM.SOFT,
	' ': 		ACTION_ENUM.HARD,
	h:  		ACTION_ENUM.HOLD 
};

console.log(ACTION_MAP)

class Input {
	init() {
		this.input = {};
		this.attach();
	}

	attach() {
		console.log('input attaching listeners');
        window.addEventListener('keydown',	e => this.onKeydown(e)	);
        window.addEventListener('keyup',    e => this.onKeyup(e)	);
	}

	poll(key) {
		return this.input[key];
	}

	onKeydown(e) {
		const key = e.key.toLowerCase();
		if (key in ACTION_MAP) {
			this.input[key] = true;
			console.log(`keydown ${key}`);
			const action = ACTION_MAP[key];
			Telemetry.emit('action', { action })
		}
	}

	onKeyup(e) {
		const key = e.key.toLowerCase();
		if (key in ACTION_MAP) {
			this.input[key] = false;
			console.log(`keyup ${key}`);
			const action = ACTION_MAP[key];
			Telemetry.emit('end_action', { action })
		}
	}
}

export default new Input();