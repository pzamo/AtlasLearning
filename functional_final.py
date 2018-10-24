#!/usr/bin/env python2.7
import sys
sys.path.append('/home/zamoldotch/SFTP/SFTP_zamolod_pbs/DB_management')
from process_clean_files import *
import numpy as np

import tensorflow as tf
import keras
from keras.models import Model
from keras.layers import Dense, Dropout, Masking, concatenate
from keras.layers import LSTM, Bidirectional, Input, TimeDistributed, GRU, GaussianNoise
from keras.utils import to_categorical
from keras.callbacks import Callback
from keras import backend as K
from keras.optimizers import Adam
from keras import regularizers

from sklearn.metrics import roc_curve, auc, roc_auc_score
from sklearn import metrics
from keras.utils import plot_model


from RNN_PROC_FINAL_2 import *

logname = 'logname' # The name used to save the model, and the training losses as a log file
# checkpoint is the callback that will save the model every epoch
checkpoint = keras.callbacks.ModelCheckpoint('/sps/atlas/z/zamolod/RNN/eta25US/{}.h5'.format(logname), monitor='val_loss', verbose=0, save_best_only=True, save_weights_only=False, mode='min', period=1)
# logger is the callback that will save avery epoch's losses and other metrics of the neural net
logger = keras.callbacks.CSVLogger('/pbs/home/p/pzamolod/{}.log'.format(logname), separator=',', append=True)

saving = [checkpoint, logger]


mask = Masking(mask_value = -50)(inputs_clus)
mask = GaussianNoise(0.1)(mask)
## Recurrent part
timedistrib = TimeDistributed(Dense(32, activation = 'relu'))(mask)
timedistrib = Dropout(0.3)(timedistrib)
lstm0 = Bidirectional(GRU(32, return_sequences=True, dropout = 0.5, kernel_initializer = 'glorot_normal', activation = 'relu'), merge_mode = 'ave')(timedistrib)
lstm1 = Bidirectional(GRU(32, return_sequences=False, dropout = 0.5, kernel_initializer = 'glorot_normal', activation = 'relu'), merge_mode = 'ave')(lstm0)
## MLP part
dense1 = Dense(32, activation = 'tanh')(lstm1)
dense1 = Dropout(0.5)(dense1)
dense2 = Dense(32, activation = 'tanh')(dense1)
dense2 = Dropout(0.5)(dense2)
dense3 = Dense(32, activation = 'tanh')(dense2)
dense3 = Dropout(0.5)(dense3)
## output layer
output= Dense(2, activation = 'softmax')(dense3)
#
model = load_model('/sps/atlas/z/zamolod/RNN/eta25US/GPU_10k_phase2_home_2.h5')

optimizer = Adam(lr=0.00005)
model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics = ['accuracy'])

model.fit_generator(gen(path, 500, clusters = True, tree_name = treeN), steps_per_epoch = 50, epochs = 10000, validation_data = (X_test, y_test), callbacks = [RocAucMetricCallback()] + saving)
