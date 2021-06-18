import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

from keras.layers import Dense, Activation, Flatten, Conv2D, MaxPooling2D, Input
from keras.models import Sequential
from keras.optimizers import Adam
import keras.utils as utils
import tensorflow_addons as tfa
import tensorflow as tf

import dane_inf

input_shape = (10,)
nb_act = 3
epochs = 5000
train_x,train_labels = dane_inf.data(50)
val_x,val_labels = dane_inf.data(20)

# train_x = np.expand_dims(train_x,-1)
# val_x = np.expand_dims(val_x,-1)
print(train_x.shape)
model = Sequential()
# model.add(Input(shape=input_shape))
# model.add(Conv2D(32,kernel_size=(3,3),activation='relu'))
# model.add(MaxPooling2D(pool_size=(2,2)))
# model.add(Conv2D(64,kernel_size=(3,3),activation='relu'))
# model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Flatten(input_shape=(18,)))
# model.add(Dense(512))
# model.add(Activation('relu'))
# model.add(Dense(256))
# model.add(Activation('relu'))
# model.add(Dense(128))
# model.add(Activation('relu'))
# model.add(Dense(64))
# model.add(Activation('relu'))
# model.add(Dense(32))
# model.add(Activation('relu'))
# model.add(Dense(16))
# model.add(Activation('relu'))
# model.add(Dense(8))
# model.add(Activation('relu'))
model.add(Dense(8))
model.add(Activation('relu'))
model.add(Dense(3))
model.add(Activation('softmax'))
model.compile(loss='binary_crossentropy' ,optimizer='Adam', metrics=['accuracy'])
# print(model.summary())

history = model.fit(train_x,train_labels,epochs=epochs,verbose=1,validation_data=(val_x,val_labels))

x_ticks = [x for x in range(0,epochs+1,200)]
train_loss = history.history['accuracy']
val_loss = history.history['val_accuracy']
epochs = range(1,epochs+1)
plt.plot(epochs, train_loss, 'r', label='Training acc')
plt.plot(epochs, val_loss, 'b', label='Validation acc')
plt.title('Training and Validation accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.xticks(ticks=x_ticks)
plt.legend()
plt.show()
# print(history.history.keys())
# utils.plot_model(model,show_shapes=True, rankdir='LR')
print(model.summary())