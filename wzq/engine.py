from chessman import *
from chessboard import *
import random
import re


class Engine(object):
    def __init__(self, chessboard):
        self.__chessboard = chessboard

    def computerGo(self, chessman):
        if not isinstance(chessman, ChessMan):
            raise Exception('第1个参数必须为ChessMan对象')

        '''
        电脑下棋 把下棋的位置写入chessman对象中
        :param chessman: 棋子对象 里面已经设置号棋子的颜色 
        :return: 
        '''
        while True:
            posX = random.randint(1, 15) # [1,15]
            posY = random.randint(1, 15) # [1,15]
            # 判断该位置是否为空
            if self.__chessboard.isEmpty((posX, posY)):
                print('电脑下棋的位置：', (posX, posY))
                # 如果该位置为空 则把posX和posY写入棋子的位置中
                chessman.setPos((posX, posY))
                # 退出while循环
                break

    def userGo(self, chessman, userInput):
        '''
        用户下棋 读取用户输入的字符串 并把下棋的位置写入chessman对象中
        :param chessman: 棋子对象 里面已经设置号棋子的颜色
        :param userInput: 用户输入的下棋坐标 '1-15,a-o'
        :return: False不能正常下棋 True能够下棋
        '''

        if not isinstance(chessman, ChessMan):
            raise Exception('第1个参数必须为ChessMan对象')

        pattern = '^([1-9]|1[0-5]),([a-o])$'
        ret = re.findall(pattern, userInput)
        if len(ret):
            posX, posY = ret[0]
            posX = int(posX)
            posY = ord(posY) - ord('a') + 1
            print('用户下棋的位置：', (posX, posY))
            # 判断该位置是否为空
            if self.__chessboard.isEmpty((posX, posY)):
            # 如果该位置为空 则把posX和posY写入棋子的位置中
                chessman.setPos((posX, posY))
                return True
        # 输入格式不正确或位置非空
        return False

    def isWon(self,pos,color):
        '''
        判断当下某一颗棋子后是否赢棋
        :param pos:下棋的位置
        :param color:下棋的颜色
        :return:True胜负已分 False胜负未分
        '''
        if not isinstance(pos, tuple) and not isinstance(pos, list):
            raise Exception('第1个参数必须为元组或列表')
        if pos[0] <= 0 or pos[0] > ChessBoard.BOARD_SIZE:
            raise Exception('下标越界')
        if pos[1] <= 0 or pos[1] > ChessBoard.BOARD_SIZE:
            raise Exception('下标越界')

        #上下方向
        startX = 1  #开始遍历的x位置
        if pos[0] - 4 > 1:
            startX = pos[0] - 4
        endX = ChessBoard.BOARD_SIZE  #结束遍历的x位置
        if pos[0] + 4 < ChessBoard.BOARD_SIZE:
            endX = pos[0] + 4
        count = 0 #统计有多少颗棋子连在一起
        for posX in range(startX,endX+1):
            if self.__chessboard.getChess((posX,pos[1])) == color:
                count += 1
                if count >= 5:
                    return True
            else:
                count = 0

        # 左右方向
        startY = 1  # 开始遍历的x位置
        if pos[1] - 4 > 1:
            startY = pos[1] - 4
        endY = ChessBoard.BOARD_SIZE  # 结束遍历的x位置
        if pos[1] + 4 < ChessBoard.BOARD_SIZE:
            endY = pos[1] + 4
        count = 0  # 统计有多少颗棋子连在一起
        for posY in range(startY, endY + 1):
            if self.__chessboard.getChess((pos[0], posY)) == color:
                count += 1
                if count >= 5:
                    return True
            else:
                count = 0

        # 左上右下方向
        count = 0
        for posX in range(startX,endX + 1):
            for posY in range(startY, endY + 1):
                if self.__chessboard.getChess((posX, posY)) == color:
                    count += 1
                    posY += 1
                    posX += 1
                    if posX > 15:
                        posX = 15
                    if posY > 15:
                        posY = 15
                    if count >= 5:
                        return True
                else:
                    count = 0

        # 左下右上方向
        count2 = 0
        for posX in range(startX, endX + 1):
            for posY in range(endY, startY - 1, -1):
                if self.__chessboard.getChess((posX, posY)) == color:
                    count2 += 1
                    posY -= 1
                    posX += 1
                    if posX > 15:
                        posX = 15
                    if posY > 15:
                        posY = 15
                    if count2 >= 5:
                        return True
                else:
                    count2 = 0


        return False

    def isWonMan(self,chessman):
        '''
        判断在棋盘上放置chessman棋子后是否赢棋
        :param chessman:放置的棋子位置和颜色
        :return:True胜负已分 False胜负未分
        '''
        if not isinstance(chessman, ChessMan):
            raise Exception('第1个参数必须为ChessMan对象')

        pos = chessman.getPos()
        color = chessman.getColor()
        return self.isWon(pos,color)

    def play(self):
        '''游戏主流程'''
        userBlack = True
        userGo = True
        #外循环
        while True:
            #用户选择先后
            userInput = input('请选择先后，b表示黑棋先下,w表示白棋后下:')
            if userInput.startswith('b'):
                userBlack =True  #用户选择黑棋
                userGo = True
            else:
                userBlack = False   #用户选择白棋
                userGo = False

            #初始化棋盘
            self.__chessboard.initBoard()
            self.__chessboard.printBoard()

            #内循环
            while True:
                chessmanUser = ChessMan()
                chessmanPC = ChessMan()
                if userBlack: #用户选择黑棋
                    chessmanUser.setColor('x')
                    chessmanPC.setColor('o')
                else:  #用户选择白棋
                    chessmanUser.setColor('o')
                    chessmanPC.setColor('x')

                #判断是否轮到用户下
                if userGo:  #轮到用户下
                    userInput = input('请输入下棋坐标:')
                    self.userGo(chessmanUser, userInput)
                    self.__chessboard.setChessMan(chessmanUser)
                else:  #轮到电脑下
                    #电脑下棋
                    self.computerGo(chessmanPC)
                    self.__chessboard.setChessMan(chessmanPC)
                #打印棋盘
                self.__chessboard.printBoard()

                #判断是否赢棋
                if userGo:  #轮到用户下
                    # pos = chessmanUser.getPos()
                    # color = chessmanUser.getColor()
                    if self.isWonMan(chessmanUser):
                        print('恭喜赢了')
                        break  #跳出内循环
                else:
                    # pos = chessmanPC.getPos()
                    # color = chessmanPC.getColor()
                    if self.isWonMan(chessmanPC):
                        print('呵呵输了')
                        break  #跳出内循环
                    else: #如果没有赢棋 则切换棋子 内循环继续
                        userGo = not userGo


            #判断是否继续游戏
            userInput = input('是否继续?(y/n)')
            if userInput.startswith('y'): #继续游戏
                pass
            else: #如果用户选择退出，则退出外循环
                break