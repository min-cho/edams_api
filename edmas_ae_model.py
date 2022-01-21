# -*- coding: utf-8 -*-
"""
@author: MR004CHM
"""
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
import datetime

from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers, losses
from tensorflow.keras.models import Model

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

os.chdir('C:\\Users\\MR004CHM\\Desktop\\TFcode\\2021-fdd_AE\\chiller_21')

np.random.seed(777)

#%% 

# Abnormal Data will not have boolean label column
# In this study, all train data are normal, and all test data are fault condition


def train_pre(train_data):
    raw =pd.read_csv(train_data).drop('Date/Time',axis='columns') #first column is timestamp
    filt = raw['SUPPLY FAN 1F:Fan Electric Energy [J](TimeStep)']!=0 # operation time
    raw  = raw.where(filt).dropna()
    raw  = raw.to_numpy(dtype=np.float32)
    
    trainX, valX = train_test_split(raw, test_size=0.2, shuffle=True)
    scalerX = MinMaxScaler(feature_range=(0.001,1)) 
    scalerX.fit(trainX)
    trainX=scalerX.transform(trainX)
    valX=scalerX.transform(valX)
    return raw, trainX, valX, scalerX

def test_pre(test_data):
    raw  = pd.read_csv(test_data).drop('Date/Time',axis='columns') #first column is timestamp
    filt = raw['SUPPLY FAN 1F:Fan Electric Energy [J](TimeStep)']!=0 # operation time
    raw  = raw.where(filt).dropna()
    raw  = raw.to_numpy(dtype=np.float32)
    
    testX = scalerX.transform(raw)
    return raw, testX
    
def set_threshold(model, normal_train_data):
    normal_train_data = scalerX.transform(normal_train_data)
    reconstructions = model.predict(normal_train_data)
    train_loss = tf.keras.losses.mse(reconstructions, normal_train_data)
    threshold = np.median(train_loss) + np.std(train_loss)
    return threshold

def predict_bool(model, data, threshold):
    reconstructions = model(data)               # By definition, autoencoder(data) returns decoded value 
    loss = tf.keras.losses.mse(reconstructions, data)
    return tf.math.less(loss, threshold) , loss # return True when (x1 < x2)



def pred_plot(error, threshold):
    plt.plot(error, label="Reconstruction Error")
    plt.axhline(y=threshold, color='r', linewidth=1)     
    #plt.ylim(0, 0.01)
    plt.legend()
    plt.show()
    print("Threshold: ", threshold)


def re_difference(model, train, test):
    enco_train = model.encoder(train)
    enco_test = model.encoder(test)
    return enco_test



 
def print_stats_bool(predictions, labels):
    print("Accuracy = {}".format(accuracy_score(labels, predictions)))
    print("Precision = {}".format(precision_score(labels, predictions)))
    print("Recall = {}".format(recall_score(labels, predictions)))
     

#def gt_table(normaldata, faultdata):
#    normal_labels = train_labels.astype(bool)
#    fault_labels = test_labels.astype(bool)

#%% Model Build
n_input = 32

class AnomalyDetector(Model):
  def __init__(self):
    super(AnomalyDetector, self).__init__()
    self.encoder = tf.keras.Sequential([
      layers.Dense(16, activation="relu"),
      layers.Dense(8, activation="relu"),
      layers.Dense(4, activation="relu")])
    self.decoder = tf.keras.Sequential([
      layers.Dense(8, activation="relu"),
      layers.Dense(16, activation="relu"),
      layers.Dense(n_input, activation="sigmoid")])
    
  def call(self, x):
    encoded = self.encoder(x)
    decoded = self.decoder(encoded)
    return decoded



def train_NN(model, traindata, valdata):
    model.compile(optimizer='adam', loss='MSE')
    history = model.fit(traindata, traindata, 
          epochs=200, 
          batch_size=32,
          validation_data=(valdata, valdata),
          shuffle=True)
    plt.plot(history.history["loss"], label="Training Loss")
    plt.plot(history.history["val_loss"], label="Validation Loss")
    plt.legend()
    plt.show()

#%% Model Train and Save

# Make Model
raw_normal, trainX, valX, scalerX = train_pre('chiller_train_rev2.csv')
autoencoder = AnomalyDetector()

train_NN(autoencoder, trainX, valX)
tf.saved_model.save(autoencoder, '/AEmodel/chiller_rev2')
#autoencoder = tf.saved_model.load('/AEmodel/boiler')

threshold_mse = set_threshold(autoencoder, raw_normal)


# FDD Test - unfaulted
raw_test, testX = test_pre('chiller_normal_rev2.csv')
pred_result , recon_error = predict_bool(autoencoder, testX, threshold_mse)
pred_plot(recon_error, threshold_mse)

# FDD Test - fault c1
raw_test, testX = test_pre('chiller_fouling_bias_severe_rev2.csv')
pred_result , recon_error = predict_bool(autoencoder, testX, threshold_mse)
pred_plot(recon_error, threshold_mse)

# FDD Test - fault c2
raw_test, testX = test_pre('chiller_fouling_bias_light_rev2.csv')
pred_result , recon_error = predict_bool(autoencoder, testX, threshold_mse)
pred_plot(recon_error, threshold_mse)


# FDD Test - tower - light bias
raw_test, testX = test_pre('coolingtower_1024_light.csv')
pred_result , recon_error = predict_bool(autoencoder, testX, threshold_mse)
pred_plot(recon_error, threshold_mse)

# FDD Test - tower - severe bias
raw_test, testX = test_pre('coolingtower_1024_sev.csv')
pred_result , recon_error = predict_bool(autoencoder, testX, threshold_mse)
pred_plot(recon_error, threshold_mse)




#%%


