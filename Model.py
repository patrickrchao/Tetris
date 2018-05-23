from collections import deque
class Model():
    move_queue = deque()

    def get_move(self,board,piece_id,piece_origin):
        if len(Model.move_queue) == 0:
            self.get_move_queue(board,piece_id,piece_origin)
        return Model.move_queue.pop()
        
    def get_move_queue(board,piece_id,piece_origin):
        raise NotImplementedError
