class Input:
    def init():
        Telemetry.subscribe('action', self.handle_action)
        Telemetry.subscribe('end_action', self.handle_end_action)
        self.input_state = {}
        self.action_callbacks = []

    def handle_action(self, data):
        if data in ACTION_MAP:
            self.input_state[data] = True

        for cb in self.action_callbacks:
            cb(data)

    def handle_end_action(self, data):
        if data == SOFT:
            self.input_state[SOFT] = False
        for cb in self.action_callbacks:
            cb(data)

    def subscribe(self, cb):
        self.action_callbacks.append(cb)

    def poll(action):
        return self.input_state[action]
    