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

    for i in range(10):
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


def PlayerVsAI():

    for i in range(10):
        Index = 0
        g = GameStateManager()
        MyAgent = Agent(g.state)
        MyAgent.Training(g)
        print('=============================================')
        print('================= NEW GAME ==================')
        print('=============================================')
        g.display()
        print('')
        MyAgent.Training(g)
        while g.endOfGAme == 0:
            print('Game N-' , i)
            print('There are' ,g.gameturns, 'steps left until the end of the game')
            
            if (Index == 0):
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
                    Index = 1
                if (act == 's'):
                    g.shoot()
            elif (Index == 1):
                qval = MyAgent.n.predict(MyAgent.AgentState)
                act = (np.argmax(qval))
                if (act == 0):
                    g.moveLeft()
                if (act == 1):
                    g.moveRight()
                if (act == 2):
                    g.moveUp()
                if (act == 3):
                    g.moveDown()
                if (act == 4):
                    g.passTurn()
                    Index = 0
                if (act == 5):
                    g.shoot()
            g.display()
            g.players[0].printPlayerInfo()
            g.players[1].printPlayerInfo()
            print('=============================================', Index)


def mainLoop():
    print("Choose the Mode")
    print("1: Player vs Player")
    print("2: Player vs AI")

    mode = input()
    if (mode == "1"):
        PlayerVsPlayer()
    if (mode == "2"):
        PlayerVsAI()



mainLoop()



