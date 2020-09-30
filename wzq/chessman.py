from chessboard import *
import threading

class ChessMan(object):
    '''棋子类'''

    def __init__(self):
        '''初始化'''
        self.__pos = [0, 0]
        self.__color = '+'
        self.con = threading.Condition()

    def setPos(self, pos):
        '''指定棋子的位置'''
        self.__pos = pos

    def getPos(self):
        '''返回棋子的位置'''
        return self.__pos

    def setColor(self, color):
        '''指定棋子的颜色'''
        self.__color = color

    def getColor(self):
        '''返回棋子的颜色'''
        return self.__color

    def doNotify(self):
        self.con.acquire()
        self.con.notify()
        self.con.release()

    def doWait(self):
        self.con.acquire()
        self.con.wait()
        self.con.release()