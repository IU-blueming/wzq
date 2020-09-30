import threading

class UserGoThread(threading.Thread):
    '用户下棋的线程'
    def __init__(self, engine, chessmanUser):
        super().__init__()
        self.engine = engine
        self.chessmanUser = chessmanUser

    # 执行子线程的方法
    def run(self):
        while True:
            #   1. 用户从终端输入下棋坐标
            userInput = input('请输入下棋坐标：')
            self.engine.userGo(self.chessmanUser,userInput)
            #   2. 用户notify
            self.chessmanUser.doNotify()
            #   3. 用户wait
            self.chessmanUser.doWait()