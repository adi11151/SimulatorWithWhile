# from GameLogic import *
from Player import *
from map import *
import random

#from players import *
class GameStateManager:

    state = Map()
    global gameturns
    

    def __init__(self):
        self.players = []
        self.tmpPlayers = [] #??
        self.players.append(Player(0,0,1,'R'))
        self.players.append(Player(9,9,2,'L'))
        self.playerTurnId = 0
        self.gameturns = 100
        self.state = Map()
        self.winner = -1
        self.state.placePlayer(self.players[0])
        self.state.placePlayer(self.players[1])
        self.endOfGAme = 0

    def setGameWinner(self):
        self.state.winner = self.winner
        
    
    def playerEnemy(self):
        for i in range(len(self.players)):
            if (i == self.playerTurnId):
                me = self.players[i]
            else:
                enemy = self.players[i]
        return me, enemy
    
    
    #=======================
    #      ACTIONS
    #=======================
        
    def makeMove(self , act):
        if (act == 0):
            self.moveLeft()
        if (act == 1):
            self.moveRight()
        if (act == 2):
            self.moveUp()
        if (act == 3):
            self.moveDown()
        if (act == 4):
            self.passTurn()
        if (act == 5):
            self.shoot()
      

    def passTurn(self):
        if(self.checkTimeOut(self.gameturns)):
            if (self.players[self.playerTurnId].isDead(self.players[abs(self.playerTurnId-1)])):
 #               print('PASS TURN PRINT ')
                self.players[self.playerTurnId].NotMyTurn()
                if(self.playerTurnId == len(self.players)-1):
                    self.playerTurnId = 0
                else:
                    self.playerTurnId = self.playerTurnId + 1
                print('****pass turn****   turn passed to player: ', self.playerTurnId)
                self.players[self.playerTurnId].myTurn()
                self.gameturns = self.gameturns-1

            else:
                self.winner = self.playerTurnId
                self.setGameWinner()
                self.endOfGAme = 1
#                print('End of Game 1')
        else:
            self.setGameWinner()
            self.endOfGAme = 1
#            print('End of Game 2')

    def moveLeft(self):
        i = self.playerTurnId        
        if(self.players[i].direction == 'L'):
            if(self.state.CheckValidationLeft(self.players[i], self.state)):
                if(self.players[self.playerTurnId].TurnLog(self.players[self.playerTurnId])):
                    self.state.moveLeft(self.players[i])
                else:
                    print('no steps left, pass the turn.')
            else:
                print('Choose another direction')
        else:
            if(self.players[self.playerTurnId].TurnLog(self.players[self.playerTurnId])):
                self.players[i].changeDirection('L')
 #               print("I turned left" , i)
            else:
                print('no steps left, pass the turn.')


    def moveRight(self):
        i = self.playerTurnId
        if(self.players[i].direction == 'R'):
            if(self.state.CheckValidationRight(self.players[i], self.state)):
                if(self.players[self.playerTurnId].TurnLog(self.players[self.playerTurnId])):
                    self.state.moveRight(self.players[i])
                else:
                    print('no steps left, pass the turn.')
            else:
                print('Choose another direction')

        else:
            if(self.players[self.playerTurnId].TurnLog(self.players[self.playerTurnId])):
                self.players[i].changeDirection('R')
 #               print("I turned right")
            else:
                print('no steps left, pass the turn.')        

    def moveUp(self):
        i = self.playerTurnId
        if(self.players[i].get_direction() == 'U'):
            if(self.state.CheckValidationUp(self.players[i], self.state)):
                if(self.players[self.playerTurnId].TurnLog(self.players[self.playerTurnId])):
                    self.state.moveUp(self.players[i])
                else:
                    print('no steps left, pass the turn.')
            else:
                print('Choose another direction')
        else:
            if(self.players[self.playerTurnId].TurnLog(self.players[self.playerTurnId])):
                self.players[i].changeDirection('U')
#                print("I turned up")
            else:
                print('no steps left, pass the turn.')

    def moveDown(self):
        i = self.playerTurnId
        if(self.players[i].direction == 'D'):
            if(self.state.CheckValidationDown(self.players[i], self.state)):
                if(self.players[self.playerTurnId].TurnLog(self.players[self.playerTurnId])):
                    self.state.moveDown(self.players[i])
                else:
                    print('!!!No steps left, pass the turn!!!')
            else:
                print('!!!Choose another direction!!!')
        else:
            if(self.players[self.playerTurnId].TurnLog(self.players[self.playerTurnId])):
                self.players[i].changeDirection('D')
#                print("I turned down")
            else:
                print('!!!No steps left, pass the turn!!!')
        
    def shoot(self):
        if(self.players[self.playerTurnId].shoot(self.players[self.playerTurnId])):
            if self.players[self.playerTurnId].DidIHit(self.players[self.playerTurnId], self.players[abs(self.playerTurnId-1)],self.state):
                self.players[abs(self.playerTurnId-1)].HpMinus()
                if (self.players[abs(self.playerTurnId-1)].hp==0):
#                    print('End of Game !!! Player ',self.playerTurnId+1,'WIN!!!')
                    self.endOfGAme = 1
                    self.winner = self.playerTurnId+1
#                    print("kto-to umer!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    ", self.endOfGAme , self.winner)
                    self.gameturns = 0
            self.players[self.playerTurnId].Fire()
            self.players[self.playerTurnId].shootThisTurn = 1

    def display(self):
        for j in range(10):
            print('')
            for i in range(10):
                temp = i,j
                if (self.state[temp] == np.array([1,0,0])).all():
                    print('XX|',end = ""),
                if (self.state[temp] == np.array([0,1,0])).all():
                    print('PL|',end = ""),
                if (self.state[temp] == np.array([0,0,1])).all():
                    print('E_|',end = ""),
                if (self.state[temp] == np.array([0,0,0])).all():
                    print ('__|',end = ""),

              
    def getState(self):
        me, enemy = self.playerEnemy()
        return self.state, me, enemy              

        
    def checkTimeOut(self,gameturns):
        if (gameturns>0):
            return 1
        else:
#            print("zakonchilos` vremya!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" , self.winner)
            return 0 

    




