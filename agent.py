'''
Created on Apr 25, 2017

@author: radon18
'''
import keras
import tensorflow
from decimal import Decimal
from keras.layers import Activation, Dense
import copy
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import RMSprop

from GameStateManager import *
from agent import *
from Player import *
from random import *
from neuralNet import *
import numpy as np
from sys import argv
# from pygame.examples.aliens import Player


class Agent:
    
    global terminalState
    def __init__(self,state):
        print('CONSTRUCTOR function')
        self.AgentState = np.zeros((10,10,5))
        self.AS = np.zeros((10,10,5))
        self.state = state
        self.WallOrNot()
        self.InitAreaStructure(state)
        self.net = neuralNet()
        self.playerPos = []
        self.enemyPos = []
        self.model = neuralNet()
        self.steps = 0
        self.epsilon = 1
        self.epsilon_min = 0.1
        self.epsilon_decay = 0.9999
        self.timesOfWrongAct = 0
        self.formme = Player
        self.formenemy=Player
        self.formstate= state
        self.target = open("winLos", 'a')
        self.winnPre = open("winPresentage", 'a')
        self.numberOfTurns = 0
        self.wins = 0
        self.loss = 0
        self.myTurn = 0
      
        
        
    def loadModelToTrain(self, path):
        print("fileName: model.h5")
  #      path = input()
        self.model.loadModel('model.h5')    

    def WallOrNot(self):
        print("WALLORNOT")
        for i in range (10):
            self.AS[i,0,0] = 0.3
            self.AS[i,9,0] = 0.4
            self.AS[0,i,0] = 0.1
            self.AS[0,i,0] = 0.2
        for i in range(9):
            for j in range(9):
                if(self.state[i+1 , j+1] == [1,0,0]).all():
                    self.AS[i+1,j+1,0]=0.5;

    def MeEnemypos(self,me, enemy):
        print("MEANDENEMY")
        for i in range(10):
            for j in range(10):
                self.AgentState[i,j,1] = 0
        self.AgentState[me.posx, me.posy,1] = 1
        self.AgentState[enemy.posx, enemy.posy,1] = 2
                    
    def initAgentParameters(self):
        self.timesOfWrongAct = 0
        self.numberOfTurns = 0
        self.gamma = 0.9
        
    def InitAreaStructure(self, state):   
#         print('InitAreaStructure function')     
        for i in range(10):
            for j in range(10):
                wallspos=0
                if(state.checkPosition(i,j)==1):
                    if(i>1):
                        if(state.checkPosition(i-1,j)==0):
                            wallspos = 1
                    if((i>1)&(j<9)):
                        if(state.checkPosition(i-1,j+1)==0):         
                            wallspos = wallspos*10+2
                    if(j<9):
                        if(state.checkPosition(i,j+1)==0):         
                            wallspos = wallspos*10+3
                    if((i<9)&(j<9)):
                        if(state.checkPosition(i+1,j+1)==0):         
                            wallspos = wallspos*10+4
                    if(i<9):
                        if(state.checkPosition(i+1,j)==0):         
                            wallspos = wallspos*10+5   
                    if((i<9)&(j>1)):
                        if(state.checkPosition(i+1,j-1)==0):         
                            wallspos = wallspos*10+6  
                    if(j>1):
                        if(state.checkPosition(i,j-1)==0):         
                           wallspos = wallspos*10+7
                    if((i>1)&(j>1)):
                        if(state.checkPosition(i-1,j-1)==0):         
                            wallspos = wallspos*10+8
                self.AgentState[i,j,2] = wallspos
#                print("WALLS POSITION   " , wallspos)
#                print(" BLABLABLA" ,"X = ", i , " | Y = ", j , " | value = ", self.AgentState[i,j,2])
                
                
    def CheckDistance(self,player, dim):
        print('DISTANCE function')
        for i in range (10):
            for j in range(10):
                self.AS[i,j,dim] = (abs(player.posx - i) +abs(player.posy - j))*0.1
 #               print(self.AgentState[i,j,dim])


     
    def CanHeShootMe(self, player):
#         print('CAN SOOT ME function')
        for i in range (10):
            for j in range(10):
                self.AgentState[i,j,4] = 0
        if (player.get_ammo()>0):
            for i in range (1,4):
                if (player.get_direction()== 'U'):
                    if (self.state[player.posx, player.posy+i] == np.array([0,0,0])).all():
                        self.AgentState[player.posx, player.posy-i, 4] = 1
                    else:
                        break
                if (player.get_direction()== 'D'):
                    if (self.state[player.posx, player.posy-i] == np.array([0,0,0])).all():
                        self.AgentState[player.posx, player.posy-i, 4] = 1
                    else:
                        break
                    
                if (player.get_direction()== 'L'):
                    if (self.state[player.posx+i, player.posy] == np.array([0,0,0])).all():
                      self.AgentState[player.posx+i, player.posy, 4] = 1
                    else:
                        break
                    
                if (player.get_direction()== 'R'):
                    if (self.state[player.posx-i, player.posy] == np.array([0,0,0])).all():
                      self.AgentState[player.posx-i, player.posy, 4] = 1
                    else:
                        break
    
    def tialAS(self, player, dim, state):
        for i in range (10):
            for j in range (10):
                self.AS[i,j,dim] = 0
        if player.get_direction()== 'L':
            self.AS[player.posx, player.posy, dim] = 0.1
        if player.get_direction()== 'R':
            self.AS[player.posx, player.posy, dim] = 0.2
        if player.get_direction()== 'U':
                self.AS[player.posx, player.posy, dim] = 0.3
        if player.get_direction()== 'D':
            self.AS[player.posx, player.posy, dim] = 0.4
            
 #       self.AS[enemy.posx, enemy.posy, 1] = 1
 #       for i in range (10):
 #           for j in range (10):
 #               if(state.checkPosition(i,j)==0):
 #                   self.AS[enemy.posx, enemy.posy, 2] = 1
        
    
#     def MyPlace(self):   
#         for i in range(10):
#             for j in range(10): 
#                 self.AgentState[i,j, 4] = 0
#         self.AgentState[self.me.posx, self.me.posy, 4] = 1
#         
#     def EnemyPlace(self):   
#         for i in range(10):
#             for j in range(10): 
#                 self.AgentState[i,j, 5] = 0
#         self.AgentState[self.enemy.posx, self.enemy.posy, 5] = 1

#
         
    def Reward(self,enemy, me, me_, WinNum, eog):   
        reward = -abs(self.MyPlayer.posx - self.EnemyPlayer.posx)-abs(self.MyPlayer.posy - self.EnemyPlayer.posy)
        reward *= 0.1 
        if (me.posx == me_.posx):
            if (me.posy == me_.posy):
                if(me.direction == me_.direction):                    
                    self.timesOfWrongAct += 1
                    print(self.timesOfWrongAct)
                    reward = reward -1.5
        if(me.direction == me_.direction):
            reward = reward - 0.2
        if (eog == 1):
            if (WinNum == me.ID):
                self.wins +=1
                print("***************************end of game AI WON!!!***********************")
                print("*****************************end of game AI WON!!!***********************")
                print("******************************end of game AI WON!!!***********************")
                lines_of_text = [" +++ Win! took %s  tries, my location: %s,%s, enemy:%s,%s times of wrong:%s \n " % (self.numberOfTurns,me_.posx, me_.posy, enemy.posx, enemy.posy, self.timesOfWrongAct)] 
                self.target.writelines(lines_of_text) 
                self.myTurn = 0
                reward = 12 - self.numberOfTurns 
            else:
                self.loss +=1
                reward = -10 -self.numberOfTurns - self.timesOfWrongAct -abs(self.MyPlayer.posx - self.EnemyPlayer.posx)-abs(self.MyPlayer.posy - self.EnemyPlayer.posy)
                print("*******************************end of game AI los!!!***********************")
                print("********************************end of game AI los!!!***********************")
                print("*********************************end of game AI los!!!***********************")
                self.myTurn = 0
                lines_of_text = [' ---Lose!  my location: %s,%s, enemy: %s,%s wrong act: %s \n ' %(me_.posx, me_.posy, enemy.posx, enemy.posy, self.timesOfWrongAct)]
                self.target.writelines(lines_of_text) 
        print("reward:      ",reward)   
        return reward            
                
    def evaluation(self, state, me, enemy):    #after preforming action   
#        self.MeEnemypos(me,enemy)
#        self.CheckDistance(me, 4)
#        self.CheckDistance(enemy, 3)
        self.MyPlayer = me
        self.EnemyPlayer = enemy


        #        send gsm to agent.makeQaction
        #        send gsm to agent2.makeQaction
        #} save   
        
    def makeQaction(self, gsm):#change name to makeQaction(gsm, model){....return gsm}     
        
        state, me, enemy = gsm.getState()
        self.evaluation(state, me, enemy)
        self.tialAS(me, 1, state)
        self.tialAS(enemy, 2, state)
        self.CheckDistance(me, 3)
        self.CheckDistance(enemy, 4)
#        print("after first evaluation")
#        print("===============AI is playin as player:   ", me.ID)
        if(me.DidIHit(me, enemy, state)):
            gsm.shoot()
        qVal = np.zeros((1,4))                 
        qVal = self.model.predict(self.AS) 
        print("11111 first predict : " , qVal)
#        OldState = np.zeros((10,10,4))
#        OldState = copy.deepcopy(self.AgentState)
        OldState = copy.deepcopy(self.AS)
        formme = copy.copy(me)
        formenemy = copy.copy(enemy)
#        formstate = state[:]
        RandomRange = uniform(0,1)
        if RandomRange <= self.epsilon:
            act = randint(0,3)
            print("Random: ",act)
        else: 
            act = qVal.argmax()
        print("my direction   :   ", me.direction)

        print("AgentState:", self.AS[0,1,2],"oldstate:", OldState[0,1,2])
        gsm.makeMove(act)
        
        state, me, enemy = gsm.getState()
        self.tialAS(me, 1, state)
        self.tialAS(enemy, 2, state)
        self.CheckDistance(me, 3)
        self.CheckDistance(enemy, 4)
#        print("=============AI is playin as player:   ", me.ID)
#        print("after second get map: ", me.direction,"former me: ", formme.direction)
        self.evaluation(state, me, enemy)
        print("AgentState:", self.AS[0,1,2],"oldstate:", OldState[0,1,2])
        if(me.DidIHit(me, enemy, state)):
            print("shoot!!")
            gsm.shoot()
            
        if (gsm.gameturns<1)|(gsm.endOfGAme == 1):
            reward = self.Reward(formenemy, formme, me, gsm.winner, 1)
            qVal[0,act] = reward
            self.model.fit(self.AS, qVal)
            terminalState = 1
            print("this is the end of the game   ", gsm.gameturns)
        else: 
            reward = self.Reward(formenemy, formme, me, gsm.winner, gsm.endOfGAme)
            print ("Rt+1 ", reward)
            qVal_ = np.zeros((1,4))  
            qVal_ = self.model.predict(self.AS)
 #           print ("qvalues after second predict S(i+1): ", self.model.predict(self.AgentState),"j = ", )
            maxQ = np.amax(qVal_)
#            print("max q  : ",maxQ, "reward = ", gamma)
            futureValue = self.gamma * maxQ
#            print("future value(gamma*maxQ): ",futureValue, "")
            newQ =np.add(reward, futureValue)
#            print("adding reward : ", reward,"to future value: ",futureValue, " = ", newQ )
            qVal[0,act] = newQ
#            print("qVal updated: ", qVal[0,act], " shoul be same as new q = " , newQ)
#            print("qVal arrey updated: ", qVal[0])
            self.model.fit(self.AS, qVal)               
            print ("predict the old state: ", self.model.predict(OldState))
#            print ("qvalues after second fit: ", self.model.predict(self.AgentState))
            print ("predict the new state: ", self.model.predict(self.AS))
#            print ("steps left : ", me.stepsLeft)
        if(me.stepsLeft==0):
  #          print("*********pass turn from AI*********8")
            gsm.passTurn()
            self.myTurn = 0
  #          print("~~~~~~~~~~~~~~~~~~number of turns:", self.numberOfTurns )
            self.numberOfTurns +=1 
  #          print("~~~~~~~~~~~~~~~~~~number of turns:", self.numberOfTurns )
#                    print("!!!!!!!!!!!!!!!status:", gsm.endOfGAme)
           
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay 
        self.gamma *= 0.9999  
     #           map, me, enemy = state_, me_, enemy_

        
               
                
                
                
                
            
            
            
            
            
            
            
            
        