'''
Created on Apr 26, 2017

@author: radon18
'''
import keras
import tensorflow
from keras.layers import Activation, Dense
import h5py
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import RMSprop
from keras.optimizers import SGD

class neuralNet:
    
    def __init__(self):
        self.model = Sequential()
        self.model.add(Dense(60, init='lecun_uniform', input_shape=(500,)))
        self.model.add(Activation('sigmoid'))
        self.model.add(Dropout(0.1))
        self.model.add(Dense(120, init='lecun_uniform'))
        self.model.add(Activation('sigmoid'))
        self.model.add(Dropout(0.01))
        self.model.add(Dense(80, init='lecun_uniform'))
        self.model.add(Activation('sigmoid'))
        self.model.add(Dropout(0.01))
        
        self.model.add(Dense(4, init='lecun_uniform'))
  #      self.model.add(Activation('sigmoid')) #linear output so we can have range of real-valued outputs
#        sgd = SGD(lr=0.06, momentum=0.1, nesterov=False)
        rms = RMSprop(lr=0.001)
 #       ab = keras.optimizers.Adadelta(lr=1.0, rho=0.95, epsilon=1e-8, decay=0.)#learning rate is really high                                                                        
        self.model.compile(loss='mse', optimizer = rms) #probably need to change later

        print("NNN initial!!!")
        
    def predict(self, state):
        return(self.model.predict(state.reshape(1,500), batch_size=1))

    
    def saveModel(self, path):
        self.model.save_weights(path, overwrite=True)
        print("file saved!!!!!!!")
        
    def loadModel(self,path):   
        self.model.load_weights(path) 
        print("file loaded!!!!!!!")
        
    def fit(self, state, y):   
        print(self.model.fit(state.reshape(1,500), y,  batch_size=5, nb_epoch=10, verbose=1))
    
    
    
    