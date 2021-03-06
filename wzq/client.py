from chessboard import *
from engine import *
import socket



import threading

class MeGoThread(threading.Thread):
    '''本方下棋的线程'''
    def __init__(self, socket, engine, chessmanMe):
        '''初始化方法'''
        super().__init__()
        self.socket = socket
        self.engine = engine
        self.chessmanMe = chessmanMe

    def run(self):
        '''执行子线程的方法'''
        try:
            while True:
                # 1. 本方从终端输入下棋坐标
                userInput = input('请输入下棋的坐标：')
                self.engine.userGo(self.chessmanMe,userInput)
                # 2. 通过网络通知对方下棋的坐标
                self.socket.send(userInput.encode('gbk'))
                # 3. 本方notify
                self.chessmanMe.doNotify()
                # 4. 本方wait
                self.chessmanMe.doWait()
        except:
            pass

class OppoGoThread(threading.Thread):
    '''对方下棋的线程'''
    def __init__(self, socket, engine, chessmanOppo):
        '''初始化方法'''
        super().__init__()
        self.socket = socket
        self.engine = engine
        self.chessmanOppo = chessmanOppo

    def run(self):
        '''执行子线程的方法'''
        try:
            while True:
                # 1. 对方wait
                self.chessmanOppo.doWait()
                # 2. 接收对方下棋的位置
                recvData = self.socket.recv(1024).decode('gbk')
                # 8,f
                # 3. 对方下棋的坐标输出到终端
                self.engine.userGo(self.chessmanOppo,recvData)
                x,y = self.chessmanOppo.getPos()
                print('对方下：%d,%d' % (x, y))
                # 4. 对方notify
                self.chessmanOppo.doNotify()
        except:
            pass


def mainThread():
    # 创建客户端的Socket
    clientSocket = None
    try:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect(('192.168.55.28', 8080))

        # 创建ChessBoard棋盘对象
        chessboard = ChessBoard()
        chessboard.initBoard()
        chessboard.printBoard()
        # 创建Engine引擎对象
        engine = Engine(chessboard)

        # 创建两个棋子对象
        chessmanMe = ChessMan()
        chessmanMe.setColor('x') # 本方执黑
        chessmanOppo = ChessMan()
        chessmanOppo.setColor('o') # 对方执白

        # 创建并启动两个线程
        meGoThread = MeGoThread(clientSocket, engine, chessmanMe)
        meGoThread.setDaemon(True)
        meGoThread.start()
        oppoGoThread = OppoGoThread(clientSocket, engine, chessmanOppo)
        oppoGoThread.setDaemon(True)
        oppoGoThread.start()

        while True:
            # 1. 本方wait
            chessmanMe.doWait()
            # 2. 在棋盘上摆放棋子
            chessboard.setChessMan(chessmanMe)
            chessboard.printBoard()
            pos = chessmanMe.getPos()
            color = chessmanMe.getColor()
            if engine.isWon(pos, color):
                print('恭喜赢了')
                break
            # 3. 对方notify
            chessmanOppo.doNotify()
            # 4. 对方wait
            chessmanOppo.doWait()
            # 5. 在棋盘上摆放棋子
            chessboard.setChessMan(chessmanOppo)
            chessboard.printBoard()
            pos = chessmanOppo.getPos()
            color = chessmanOppo.getColor()
            if engine.isWon(pos, color):
                print('呵呵输了')
                break
            # 6. 本方notify
            chessmanMe.doNotify()
    except:
        pass
    finally:
        if clientSocket != None:
            clientSocket.close()

if __name__ == '__main__':
    mainThread()