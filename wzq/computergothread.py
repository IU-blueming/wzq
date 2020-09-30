import threading

class ComputerGoThread(threading.Thread):
    '电脑下棋的线程'
    def __init__(self, engine, chessmanPC):
        super().__init__()
        self.engine = engine
        self.chessmanPC = chessmanPC

    # 执行子线程的方法
    def run(self):
        while True:
            #   1. 电脑wait
            self.chessmanPC.doWait()
            #   2. 电脑随机下棋
            self.engine.computerGo(self.chessmanPC)
            #   3. 电脑notify
            self.chessmanPC.doNotify()
