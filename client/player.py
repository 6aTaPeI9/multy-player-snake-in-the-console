import threading
from snake import Snake

class Player(threading.Thread):
    def __init__(self, ip, port, con, start_pos: tuple, queue):
        super().__init__()
        self.con = con
        self.ip = ip
        self.port = port
        self.login = None
        self.uuid = None
        self.ex_count = 0
        self.snake = Snake(*start_pos)
        self.queue = queue
        self.last_turn = None


    def run(self):
        try:
            while True:
                data = self.con.recv(1024)
                if not data:
                    break

                data = data.decode()

                if not self.login:
                    self.login = data
                else:
                    self.last_turn = int(data)
        finally:
            self.con.close()
        pass
