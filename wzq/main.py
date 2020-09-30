from chessboard import *
from chessman import *
from usergothread import *
from computergothread import *
from engine import *

# def test1():
#     chessboard = ChessBoard()
#     chessboard.initBoard()
#     chessboard.printBoard()
#
# def test2():
#     chessboard = ChessBoard()
#     chessboard.initBoard()
#     # 在(3,5)位置上放置一颗黑棋
#     chessboard.setChess((3,5), 'x')
#     chessman = ChessMan()
#     # 在(4,7)位置上放置一颗黑棋
#     chessman.setPos((4,7))
#     chessman.setColor('o')
#     chessboard.setChessMan(chessman)
#     chessboard.printBoard()
#     #测试读取棋子
#     ret = chessboard.getChess((4,11))
#     print(ret)
#     #测试坐标是否为空
#     ret = chessboard.isEmpty((4,7))
#     if ret:
#         print('empty')
#     else:
#         print('not empty')
#
# def test3():
#     chessboard = ChessBoard()
#     chessboard.initBoard()
#     # 创建棋子对象
#     chessman = ChessMan()
#     chessman.setColor('o') # 电脑用白棋
#     # 创建引擎对象
#     engine = Engine(chessboard)
#     engine.computerGo(chessman)
#     # 把电脑下棋的位置放到棋盘上
#     chessboard.setChessMan(chessman)
#     chessboard.printBoard()
#
# def test4():
#     chessboard = ChessBoard()
#     chessboard.initBoard()
#
#     chessman = ChessMan()
#     chessman.setColor('x')
#
#     engine = Engine(chessboard)
#     userInput = input('请输入下棋坐标：')
#     ret = engine.userGo(chessman,userInput)
#     if ret:
#         chessboard.setChessMan(chessman)
#         chessboard.printBoard()
#
# def test5():
#     '''测试判断是否赢棋'''
#     chessboard = ChessBoard()
#     chessboard.initBoard()
#     # 创建Engine对象
#     engine = Engine(chessboard)
#     # 连续放置5颗棋子
#     chessboard.setChess((15,3), 'x')
#     chessboard.setChess((15,4), 'x')
#     chessboard.setChess((15,5), 'x')
#     chessboard.setChess((15,6), 'x')
#     chessboard.setChess((15,7), 'x')
#     # 打印棋盘
#     chessboard.printBoard()
#     # 判断是否赢棋
#     ret = engine.isWon((15,5), 'x')
#     if ret:
#         print('胜负已分')
#     else:
#         print('胜负未分')
#
def main():
    chessboard = ChessBoard()
    engine = Engine(chessboard)
    engine.play()

def mainThread():
    '''多线程五子棋的主流程'''
    # 创建棋盘并初始化
    chessboard = ChessBoard()
    chessboard.initBoard()
    chessboard.printBoard()
    # 创建引擎对象
    engine = Engine(chessboard)
    # 创建两个棋子对象
    chessmanUser = ChessMan()
    chessmanUser.setColor('x') # 用户执黑
    chessmanPC = ChessMan()
    chessmanPC.setColor('o') # 电脑执白
    # 启动两个线程
    computerGo = ComputerGoThread(engine, chessmanPC)
    userGo = UserGoThread(engine, chessmanUser)
    computerGo.setDaemon(True)
    userGo.setDaemon(True)
    computerGo.start()
    userGo.start()

    # 开始循环
    while True:
        #   1. 用户wait
        chessmanUser.doWait()
        #   2. 在棋盘上摆放棋子
        chessboard.setChessMan(chessmanUser)
        chessboard.printBoard()
        pos = chessmanUser.getPos()
        if engine.isWon(pos, 'x'):
            print('恭喜赢了')
            break
        #   3. 电脑notify
        chessmanPC.doNotify()
        #   4. 电脑wait
        chessmanPC.doWait()
        #   5. 在棋盘上摆放棋子
        chessboard.setChessMan(chessmanPC)
        chessboard.printBoard()
        pos = chessmanPC.getPos()
        if engine.isWon(pos, 'o'):
            print('呵呵输了')
            break
        #   6. 用户notify
        chessmanUser.doNotify()


if  __name__ == '__main__':
    # main()
    mainThread()