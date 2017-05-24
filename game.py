'''
Created on Apr 25, 2017

@author: radon18
'''
from decimal import Decimal
from Player import *
from GameStateManager import *
from agent import *
from random import *


global Index


def PlayerVsPlayer():

    for i in range(400):
        g = GameStateManager()
        print('=============================================')
        print('================= NEW GAME ==================')
        print('=============================================')
        g.display()
        print('')
        while g.endOfGAme == 0:
            print('Game N-' , i)
            print('There are' ,g.gameturns, 'steps left until the end of the game')
            
            act = input('    Please enter your Action: ')
            if (act == 'l'):
                g.moveLeft()
            if (act == 'r'):
                g.moveRight()
            if (act == 'u'):
                g.moveUp()
            if (act == 'd'):
                g.moveDown()
            if (act == 'p'):
                g.passTurn()
            if (act == 's'):
                g.shoot()
            g.display()
            g.players[0].printPlayerInfo()
            g.players[1].printPlayerInfo()
            print('=============================================')


def Tarin2AI(): 
    g = GameStateManager()
    MyAgent = Agent(g.state)
    path = input()
    MyAgent.loadModelToTrain(path)
    MyAgent2 = Agent(g.state)
    path = input()
    MyAgent2.loadModelToTrain(path)
    for i in range (10):
        MyAgent.numberOfTurns = 0
        print("number of turns    :",MyAgent.numberOfTurns)
        MyAgent.terminalState = 0
#        if (i%100==0):
#           towrite = ['For %s iterations, %s \n' %(i, self.wins)] 
#           self.winnPre.writelines(towrite)
#           self.wins = 0 

        while (g.endOfGAme == 0):
            if (MyAgent.terminalState == 1):
                print("end og game winner: ",g.winner)
            while(MyAgent.myTurn)&(g.endOfGAme == 0):
                MyAgent.makeQaction(g)
            MyAgent.myTurn = 1
#            g.display()
            while(MyAgent2.myTurn)&(g.endOfGAme == 0):
                MyAgent2.makeQaction(g)
            MyAgent2.myTurn = 1
            g.display()
        g = GameStateManager() 
        print("========new game======= ", i)
#    self.n.saveModel("model2.h5")
#    self.target.close()
#    self.winnPre.close()


def TrainAI():
#    for i in range(10):
    print("Load existing AI?")
    print("press y/n")
    g = GameStateManager()
    MyAgent = Agent(g.state)
    mode = input()
#    if mode == "y":
    MyAgent.loadModelToTrain('bestmodelever.h5')
    illigalAct = 0
    highestNumbersOfWins = 40
    for i in range(15000):
        j = 0
        illigalAct = illigalAct + MyAgent.timesOfWrongAct
        if (i%50 == 0):
            towrite = ["eplsilon: %s illegal : %s wins: %s \n"%(MyAgent.epsilon, illigalAct, MyAgent.wins)]
            MyAgent.winnPre.writelines(towrite)
            illigalAct = 0
            
            if (MyAgent.wins >= highestNumbersOfWins):
                MyAgent.save('bestmodelever2.h5')
                highestNumbersOfWins = MyAgent.wins
            MyAgent.wins = 0
        MyAgent.initAgentParameters()
        while (g.endOfGAme == 0):
            j +=1
            print("========turns = ", j)
            
            while(MyAgent.myTurn)&(g.endOfGAme == 0):
                MyAgent.makeQaction(g)
            act = randint(0,3)
            g.makeMove(act)
            act = randint(0,3)
            g.makeMove(act)
            g.passTurn()
            MyAgent.myTurn = 1
            g.display() 
        g = GameStateManager()
        print("========new game======= ", i)   

        


    

        
        
        
        
#         print('=============================================')
#         print('================= NEW GAME ==================')
#         print('=============================================')
#         g.display()
#         print('')
#         MyAgent.Training(g)
#         while g.endOfGAme == 0:
#             print('Game N-' , i)
#             print('There are' ,g.gameturns, 'steps left until the end of the game')
#             
#             if (Index == 0):
#                 act = input('    Please enter your Action: ')
#                 if (act == 'l'):
#                     g.moveLeft()
#                 if (act == 'r'):
#                     g.moveRight()
#                 if (act == 'u'):
#                     g.moveUp()
#                 if (act == 'd'):
#                     g.moveDown()
#                 if (act == 'p'):
#                     g.passTurn()
#                     Index = 1
#                 if (act == 's'):
#                     g.shoot()
#             elif (Index == 1):
#                 qval = MyAgent.n.predict(MyAgent.AgentState)
#                 act = (np.argmax(qval))
#                 if (act == 0):
#                     g.moveLeft()
#                 if (act == 1):
#                     g.moveRight()
#                 if (act == 2):
#                     g.moveUp()
#                 if (act == 3):
#                     g.moveDown()
#                 if (act == 4):
#                     g.passTurn()
#                     Index = 0
#                 if (act == 5):
#                     g.shoot()
#             g.display()
#             g.players[0].printPlayerInfo()
#             g.players[1].printPlayerInfo()
#             print('=============================================', Index)


#def AIvsAI(): #load train file from interface
    #send nets to train AI
    
 

def mainLoop():
    print("Choose the Mode")
    print("1: Player vs Player")
    print("2: Player vs AI")

    mode = input()
    if (mode == "1"):
        PlayerVsPlayer()
    if (mode == "2"):
        TrainAI()
    if (mode == "3"):
        Tarin2AI()



mainLoop()



