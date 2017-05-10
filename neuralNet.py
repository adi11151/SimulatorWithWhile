'''
Created on Apr 26, 2017

@author: radon18
'''
import keras
import tensorflow
from keras.layers import Activation, Dense

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import RMSprop

class neuralNet:
    
    def __init__(self):
        self.model = Sequential()
        self.model.add(Dense(250, init='lecun_uniform', input_shape=(400,)))
        self.model.add(Activation('sigmoid'))
        self.model.add(Dropout(0.2)) 
        
        self.model.add(Dense(150, init='lecun_uniform'))
        self.model.add(Activation('sigmoid'))
        self.model.add(Dropout(0.2))
        
        self.model.add(Dense(4, init='lecun_uniform'))
  #      self.model.add(Activation('sigmoid')) #linear output so we can have range of real-valued outputs
        
        rms = RMSprop()
        self.model.compile(loss='mse', optimizer=rms)
        print("NNN initial!!!")
        
    def predict(self, state):
        return(self.model.predict(state.reshape(1,400), batch_size=1))

    
    def fit(self, state, y):   
        print(self.model.fit(state.reshape(1,400), y,  batch_size=1, nb_epoch=4, verbose=1))
    
    
    
    