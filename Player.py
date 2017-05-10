'''
Created on Apr 26, 2017

@author: radon18
'''

class Player:
    def __init__(self, positionX, positionY, id, direct):
        self.ammo = 10
        self.hp = 100
        self.ID = id
        self.MyTurn = 1
        self.stepsLeft = 2
        self.shootThisTurn = 0
        self.posx = positionX
        self.posy = positionY
        self.direction = direct


    #    ****************
    #    GETTERS
    #    ****************

    def get_ammo(self):
        return self.ammo

    def get_HP(self):
        return self.HP

    def get_ID(self):
        return self.ID

    # def get_position(self):
    #     return self.position

    def get_stepsLeft(self):
        return self.stepsLeft

    def isItMyTurn(self):
        return self.MyTurn

    def get_direction(self):
        return self.direction

    #    ****************
    #    SETTERS
    #    ****************

    def set_ammo(self,Ammo):
        ammo = Ammo

    def set_HP(self,hp):
        HP = hp

    # def set_position(self,pos):
    #     position = pos

    def set_stepsLeft(self, steps):

        self.stepsLeft = steps

    #    **************

    #    **************

    def myTurn(self):
        self.shootThisTurn = 0
        self.stepsLeft = 2
        self.MyTurn = 1    

    def NotMyTurn(self):
        
        self.MyTurn = 0

    def Fire(self):
        self.ammo = self.ammo-1

    def HpMinus(self):
        self.hp = self.hp - 100
#        GameStateManager().gameturns = 0

    def moveLeft(self):
        self.posx = self.posx - 1
        print("new pos at player module" , self.posx, self.posy)
        print("I took a step to the left")
        return self.posx, self.posy

    def moveRight(self):
        self.posx = self.posx + 1
        print("new pos at player module" , self.posx, self.posy)
        print("I took a step to the right")
        return self.posx, self.posy

    def moveUp(self):
        self.posy = self.posy - 1
        print("new pos at player module" , self.posx, self.posy)
        print("I took a step to the up")
        return self.posx, self.posy

    def moveDown(self):
        self.posy = self.posy + 1
        print("new pos at player module" , self.posx, self.posy)
        print("I took a step to the down", self.ID)
        return self.posx, self.posy

    def changeDirection(self, direction):
        self.direction = direction

    def printPlayerInfo(self):
        print('')
        print('id = ' ,self.ID)
        print('hp = ' ,self.hp)
        print('ammo = ' ,self.ammo)
        print('posx = ' ,self.posx)
        print('posy = ' ,self.posy)
        print('direction = ' ,self.direction)
        print('steps left = ' ,self.stepsLeft)

    def TurnLog(self, player):    # hasMovesLeft
        if (player.get_stepsLeft() == 0):
            return 0
        else:
            player.set_stepsLeft(player.get_stepsLeft() - 1)
            return 1




    def DidIHit(self, me, enemy,state):

        if ((me.get_ammo()>0)&(me.shootThisTurn == 0)):
            if (me.get_direction()== 'U'):
                if((me.posy - enemy.posy)<4)&((me.posy - enemy.posy)>0)&(me.posx==enemy.posx):
                    for i in range(me.posy - enemy.posy):
                        #print(i , enemy.posy , me.posy)
                        if (state[me.posx,enemy.posy+i]==[1,0,0]).all():
                            print('kir')
                            return 0
                    return 1
            if (me.get_direction()== 'D'):
                if((enemy.posy - me.posy)<4)&((enemy.posy - me.posy)>0)&(me.posx==enemy.posx):
                    for i in range(enemy.posy - me.posy):
                        if (state[me.posx,me.posy+i]==[1,0,0]).all():
                            print('kir')
                            return 0
                    return 1
            if (me.get_direction()== 'L'):
                if((me.posx - enemy.posx)<4)&((me.posx - enemy.posx)>0)&(me.posy==enemy.posy):
                    for i in range(me.posx - enemy.posx):
                        if (state[enemy.posx+i,me.posy]==[1,0,0]).all():
                            print('kir')
                            return 0
                    return 1
            if (me.get_direction()== 'R'):
                if((enemy.posx - me.posx)<4)&((enemy.posx - me.posx)>0)&(me.posy==enemy.posy):
                    for i in range(enemy.posx - me.posx):
                        if (state[me.posx+i,me.posy]==[1,0,0]).all():
                            print('kir')
                            return 0
                    return 1


    def shoot(self, player):
        if (player.ammo>0):
            if (player.shootThisTurn==0):
                return 1
            else:
                print('You already shot')
                return 0
        else:
            print('You do not have enough bullets')
            return 0


    def isDead(self, player):
        if (player.hp>0):
            return 1
        else:
            return 0