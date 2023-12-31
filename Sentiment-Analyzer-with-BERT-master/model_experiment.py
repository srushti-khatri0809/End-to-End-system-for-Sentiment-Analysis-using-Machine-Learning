import tensorflow as tf
from keras import backend as K
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
import collections
import numpy as np
import pickle
import matplotlib.pyplot as plt
from sacred import SETTINGS
SETTINGS.CONFIG.READ_ONLY_CONFIG = False

from sacred import Experiment
from sacred.observers import MongoObserver
ex = Experiment()
ex.observers.append(MongoObserver(
    url='mongodb://192.168.1.2:27017'))
    
def load_model():
    train_x = pickle.load(open("data/train_x.pkl", 'rb'))
    print(train_x)
    train_y = pickle.load(open("data/train_y.pkl", 'rb'))
    test_x = pickle.load(open("data/test_x.pkl", 'rb'))
    test_y = pickle.load(open("data/test_y.pkl", 'rb'))
    valid_x = pickle.load(open("data/valid_x.pkl", 'rb'))
    valid_y = pickle.load(open("data/valid_y.pkl", 'rb'))
    return train_x, train_y, test_x, test_y, valid_x, valid_y

def build_model(train_x, batch_size=128,
                dense_1_nodes=256, dense_2_nodes=256, dense_3_nodes=256, dense_4_nodes=256,
                dropout_1_size=0.1, dropout_2_size=0.1, dropout_3_size=0.1, dropout_4_size=0.1, dropout_5_size=0.3):
    model = Sequential()
    
    # The Input Layer :
    model.add(Dense(dense_1_nodes, kernel_initializer='normal',input_dim = train_x.shape[1], activation='relu'))
    model.add(Dropout(rate=dropout_1_size))
    
    # The Hidden Layers :
    model.add(Dense(dense_2_nodes, kernel_initializer='normal',activation='relu'))
    model.add(Dropout(dropout_2_size))
    
    model.add(Dense(dense_3_nodes, kernel_initializer='normal',activation='relu'))
    model.add(Dropout(dropout_3_size))
    
    model.add(Dense(dense_4_nodes, kernel_initializer='normal',activation='relu'))
    model.add(Dropout(dropout_4_size))

    # The Output Layer :
    model.add(Dense(units = 1, activation="sigmoid"))
    model.add(Dropout(dropout_5_size))
    model.compile(loss='mean_squared_error', optimizer='rmsprop', metrics = ['mse', 'mae'])
    print(model.summary)
    return model


def model_testing(test_x, test_y, model, history):
    pred_y = model.predict(test_x)
    np.savetxt("data/pred_y.csv", pred_y, delimiter=",")
    mae = mean_absolute_error(pred_y, test_y)
    mse = mean_squared_error(pred_y, test_y)
    print(f'MSE = {mse}')
    plt.plot(history.history['mse'])
    print(f'MAE = {mae}')
    plt.plot(history.history['mae'])
    plt.legend()
    plt.show()

    ex.log_scalar("MAE", mae)
    ex.log_scalar("MSE", mse)

@ex.config
def cfg():
    epochs=30 
    batch_size=128
    dense_1_nodes=256 
    dense_2_nodes=256 
    dense_3_nodes=256 
    dense_4_nodes=256
    dropout_1_size=0.1 
    dropout_2_size=0.1 
    dropout_3_size=0.1 
    dropout_4_size=0.1
    dropout_5_size=0.3 

def model_training(train_x, train_y, valid_x, valid_y, epochs, batch_size,
                   dense_1_nodes, dense_2_nodes, dense_3_nodes, dense_4_nodes,
                dropout_1_size, dropout_2_size, dropout_3_size, dropout_4_size, dropout_5_size):
    model = build_model(train_x, batch_size, 
                         dense_1_nodes, dense_2_nodes, dense_3_nodes, dense_4_nodes,
                dropout_1_size, dropout_2_size, dropout_3_size, dropout_4_size, dropout_5_size)
    history = model.fit(train_x.values, train_y.values, epochs=epochs, batch_size=batch_size, verbose=2, validation_data=(valid_x.values, valid_y.values))
    model.save('model.h5')
    return model, history

@ex.automain
def main(epochs, batch_size,
         dense_1_nodes, dense_2_nodes, dense_3_nodes, dense_4_nodes,
         dropout_1_size, dropout_2_size, dropout_3_size, dropout_4_size, dropout_5_size):
    
    train_x, train_y, test_x, test_y, valid_x, valid_y = load_model()
    model, history = model_training(train_x, train_y, valid_x, valid_y, epochs=epochs, batch_size=batch_size,
                                    dense_1_nodes=dense_1_nodes, dense_2_nodes=dense_2_nodes, dense_3_nodes=dense_3_nodes, dense_4_nodes=dense_4_nodes,
                                    dropout_1_size=dropout_1_size, dropout_2_size=dropout_2_size, dropout_3_size=dropout_3_size, dropout_4_size=dropout_4_size, dropout_5_size=dropout_5_size)
    model_testing(test_x, test_y, model, history)
