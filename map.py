'''
Created on Apr 26, 2017

@author: radon18
'''
import numpy as np


class Map:

    def __init__(self):
        self.state = self.build()
        self.winner = -1

    def    __getitem__(self ,arg):
        return(self.state[arg])

    def build(self):
        self.state = np.zeros((10,10,3))
        wall1Pos = [1,3]
        wall2Pos = [1,7]
        wall3Pos = [5,8]
        for i in range(4):
            self.state[i+wall1Pos[0], wall1Pos[1]] = np.array([1,0,0])
        for i in range(4):
            self.state[i+wall2Pos[0], wall2Pos[1]] = np.array([1,0,0])
        for i in range(4):
            self.state[i+wall3Pos[0], wall3Pos[1]] = np.array([1,0,0])

        return self.state
    

    def moveLeft(self, player):
        self.state[player.posx, player.posy] = np.array([0,0,0])
        self.state[player.moveLeft()] = np.array([0,1,0])
        # print("newposss" , player.posx, player.posy)

    def moveRight(self, player):
        self.state[player.posx, player.posy] = np.array([0,0,0])
        self.state[player.moveRight()] = np.array([0,1,0])


    def moveUp(self, player):
        self.state[player.posx, player.posy] = np.array([0,0,0])
        self.state[player.moveUp()] = np.array([0,1,0])
        # print("newposss" , player.posx, player.posy)

    def moveDown(self, player):
        self.state[player.posx, player.posy] = np.array([0,0,0])
        self.state[player.moveDown()] = np.array([0,1,0])

    def placePlayer(self, player):
        self.state[player.posx , player.posy] = np.array([0,1,0])


    def checkPosition(self, x, y):
        if (self.state[x,y] == np.array([0,0,0])).all():
#             print("11111111111111111111111111       ", self.state[x,y])
            return 1
        else:
            return 0

    def CheckValidationLeft(self,player, state):
        if (player.posx-1 >= 0):
            if (state.checkPosition(player.posx-1, player.posy)):
                return 1
            else:
                print('Something is hindered on the road')
                return 0 
        else:
            print('You are to close to left border')
            return 0


    def CheckValidationRight(self,player, state):
        if (player.posx+1 < 10):
            if (state.checkPosition(player.posx+1, player.posy)):
                return 1
            else:
                print('Something is hindered on the road')
                return 0 
        else:
            print('You are to close to right border')
            return 0

    def CheckValidationDown(self,player, state):
        if (player.posy+1 <10):
            if (state.checkPosition(player.posx,player.posy+1)):
                return 1
            else:
                print('Something is hindered on the road')
                return 0 
        else:
            print('You are to close to down border')
            return 0

    def CheckValidationUp(self, player, state):
#        print('check up')
        if (player.posy-1 >= 0):
#            print('first condition good')
            if (state.checkPosition(player.posx,player.posy-1)):
                return 1
            else:
                print('Something is hindered on the road')
                return 0 
        else:
            print('You are to close to up border')
            return 0
