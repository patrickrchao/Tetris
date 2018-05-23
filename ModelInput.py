from telemetry import Telemetry
from Model import Model
class ModelInput:
    def __init__(self,Model):
        #telemetry.subscribe('action', self.handle_action)
        #telemetry.subscribe('end_action', self.handle_end_action)
        #self.current_state = {}
        self.action_cbs = []
        self.end_action_cbs = []
        self.model = Model

    def get_next_input(self,board,piece_id,piece_origin):
        return {"action":Model.get_move(self.model,board,piece_id,piece_origin)}
    def handle_action(self, data):
        #self.input_state[data['action']] = True
        for cb in self.action_cbs:
            cb(data)

    def handle_end_action(self, data):
        #self.input_state[data['action']] = True
        for cb in self.end_action_cbs:
            cb(data)

    def subscribe(self, event_type, cb):
        if event_type == 'action':
            self.action_cbs.append(cb)
        elif event_type == 'end_action':
            self.end_action_cbs.append(cb)

    # def poll(self, action):
    #     if action in self.input_state:
    #         return self.input_state[action]
    #     return False
    # 