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
    
    
    def __init__(self,state):
        print('CONSTRUCTOR function')
        self.AgentState = np.zeros((10,10,4))
        self.AS = np.zeros((10,10,4))
        self.state = state
        self.WallOrNot()
        self.InitAreaStructure(state)
        self.net = neuralNet()
        self.playerPos = []
        self.enemyPos = []
        self.n = neuralNet()
        self.steps = 0
        self.epsilon = 1
        self.epsilon_min = 0.1
        self.epsilon_decay = 0.9999
        self.timesOfWrongAct = 0
        self.formme = Player
        self.formenemy=Player
        self.formstate= state
        self.target = open("winLos", 'a')
        self.numberOfTurns = 0
        
        

    def WallOrNot(self):
        for i in range(10):
            for j in range(10):
                if(self.state[i , j] == [1,0,0]).all():
                    self.AgentState[i,j,0]=1;
                    
    
        
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
                self.AgentState[i,j,1] = wallspos
#                print("WALLS POSITION   " , wallspos)
#                print(" BLABLABLA" ,"X = ", i , " | Y = ", j , " | value = ", self.AgentState[i,j,2])
                
                
    def CheckDistance(self,player, dim):
#         print('DISTANCE function')
        for i in range (10):
            for j in range(10):
                self.AgentState[i,j,dim] = abs(player.posx - i)*10 +abs(player.posy - j)


     
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
    
    def tialAS(self,me, enemy, state):
        self.AS[me.posx,me.posy,0] = 1
        self.AS[enemy.posx,enemy.posy,1] = 1
        for i in range (10):
            for j in range (10):
                if(state.checkPosition(i,j)==0):
                    self.AS[enemy.posx,enemy.posy,2] = 1
        
    
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
        distancex = (self.AgentState[me_.posx,me.posy,3])/10
        distancey = (self.AgentState[me_.posx,me.posy,3])%10
        reward = distancex - distancey    
        reward = -abs(self.MyPlayer.posx - self.EnemyPlayer.posx)-abs(self.MyPlayer.posy - self.EnemyPlayer.posy)
        reward *= 0.1 
        if (me.posx == me_.posx):
            if (me.posy == me_.posy):
                if(me.direction == me_.direction):
                    print("stuck in wall!!!!!!!!", reward,"old direction :", me.direction,"new direction: ", me_.direction)
                    
                    self.timesOfWrongAct += 1
                    reward = reward - 20 * self.timesOfWrongAct
                    print("new reward for stuck in wall!!!!!!!!", reward)
                else:
                    self.timesOfWrongAct = 0
            else:
                self.timesOfWrongAct = 0
        else:
            self.timesOfWrongAct = 0
            
        reward = -1
        if (eog == 1):
            if (WinNum == me.ID):
                print("**************end of game AI WON!!!***********************")
                print("**************end of game AI WON!!!***********************")
                print("**************end of game AI WON!!!***********************")
                lines_of_text = [" +++ Win! took %s  tries, my location: %s,%s, enemy:%s,%s \n " % (self.numberOfTurns,me_.posx, me_.posy, enemy.posx, enemy.posy)] 
                self.target.writelines(lines_of_text) 
                reward = +100 
            else:
                reward = -100
                print("**************end of game AI los!!!***********************")
                print("**************end of game AI los!!!***********************")
                print("**************end of game AI los!!!***********************")
                lines_of_text = [' ---Lose! \n my location: %s,%s, enemy: %s,%s \n ' %(me_.posx, me_.posy, enemy.posx, enemy.posy)]
                self.target.writelines(lines_of_text) 
        print("reward:      ",reward)   
        return reward            
                
    def evaluation(self, state, me, enemy):    #after preforming action   
        self.CheckDistance(me, 2)
        self.CheckDistance(enemy, 3)
        self.MyPlayer = me
        self.EnemyPlayer = enemy
#         print("  me   = " , self.MyPlayer.posx , "  =  " ,self.MyPlayer.posy)
#         print("  me   = " , self.EnemyPlayer.posx , "  =  " , self.EnemyPlayer.posy)
#        self.CanHeShootMe(enemy)
         
        
    def Training(self, gsm):     
        gamma = 0.9
        qval = []
        for i in range (1000):         
            gsm = GameStateManager()
            j = 0
            print('============New Game===========')
            print('============New Game===========')
            self.numberOfTurns = 0
            while (gsm.endOfGAme == 0):         
                self.formstate, self.formme, self.formenemy = gsm.getState()
                print("after first get map: ", self.formme.direction)
                self.evaluation(self.formstate, self.formme, self.formenemy)
                if(self.formme.DidIHit(self.formme, self.formenemy, self.formstate)):
                    gsm.shoot()
                qVal = np.zeros((1,4))                 
                qVal = self.n.predict(self.AgentState)
                
                
                OldState = self.AgentState[:]
                print ("qvalues after first predict: ", qVal,"j = ", j)
                uniforNum = uniform(0,1)
                if uniforNum <= self.epsilon:
                    act = randint(0,3)
                    print("Random: ",act)
                else: 
#                     act = (np.amax(qVal[0]))
                    act = qVal.argmax()
                print("after first get map: ", self.formme.direction)
                formme = copy.copy(self.formme)
                gsm.makeMove(act)
                state_, me_, enemy_ = gsm.getState()
                print("after second get map: ", me_.direction,"former me: ", formme.direction)
                self.evaluation(state_, me_, enemy_)
                if(me_.DidIHit(me_, enemy_, state_)):
                    print("shoot!!")
                    gsm.shoot()
                reward = self.Reward(self.formenemy, formme, me_, gsm.winner, gsm.endOfGAme)
                print ("Rt+1 ", reward)
                qVal_ = np.zeros((1,4))
                
                
                qVal_ = self.n.predict(self.AgentState)
                print ("qvalues after second predict S(i+1): ", qVal,"j = ", j)
                
                maxQ = np.amax(qVal_)
                
                print("max q  : ",maxQ, "reward = ", gamma)
                futureValue = gamma * maxQ
                print("future value(gamma*maxQ): ",futureValue, "")
                newQ =np.add(reward, futureValue)
                print("adding reward : ", reward,"to future value: ",futureValue, " = ", newQ )
                
                
                qVal[0,act] = newQ
                print("qVal updated: ", qVal[0,act], " shoul be same as new q = " , newQ)
                print("qVal arrey updated: ", qVal[0], "j = " , j)
                self.n.fit(OldState, qVal)
                print ("qvalues after second fit: ", self.n.predict(OldState),"j = ", j)

 #               gamma -= (i+1 * 0.1)
 #               print("gamma   : ", gamma)
                if(self.formme.stepsLeft==0):
                    gsm.passTurn()
                    self.numberOfTurns +=1 
#                    print("!!!!!!!!!!!!!!!status:", gsm.endOfGAme)
                    if(gsm.gameturns<2):
                        reward = self.Reward(self.formenemy, self.formme, me_, gsm.winner, 1)
                        qVal[0,act] = reward
                        self.n.fit(self.AgentState, qVal)
                    act = randint(0,3)
                    gsm.makeMove(act)
                    act = randint(0,3)
                    gsm.makeMove(act)
                    gsm.passTurn()
                    gsm.display()   
                    
                if self.epsilon > self.epsilon_min:
                    self.epsilon *= self.epsilon_decay
                j +=1   
     #           map, me, enemy = state_, me_, enemy_
        self.target.close()
               
                
                
                
                
            
            
            
            
            
            
            
            
        