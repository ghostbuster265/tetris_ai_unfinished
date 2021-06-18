# import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

from keras.layers import Dense, Activation, Flatten, Conv2D, MaxPooling2D, Input, Dropout
from keras.models import Sequential

import dane_do_nn

input_shape = (20,10,3)
nb_act = 3
epochs = 50000
train_x,train_labels = dane_do_nn.data(20)
val_x,val_labels = dane_do_nn.data(5)

# train_x = np.expand_dims(train_x,-1)
# val_x = np.expand_dims(val_x,-1)

model = Sequential()
model.add(Input(shape=input_shape))
model.add(Conv2D(32,kernel_size=(3,3),activation='relu',))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Conv2D(64,kernel_size=(3,3),activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Flatten(input_shape=(20,10,3)))
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dense(256))
model.add(Activation('relu'))
# model.add(Dense())
# model.add(Activation('relu'))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(8))
model.add(Activation('relu'))
# model.add(Dropout(0.5))
# model.add(Activation('relu'))
model.add(Dense(nb_act))
model.add(Activation('relu'))
model.compile(loss='poisson',optimizer='Adam', metrics=['accuracy'])
print(model.summary())

history = model.fit(train_x,train_labels,epochs=epochs,verbose=1,validation_data=(val_x,val_labels))

x_ticks = [x for x in range(0,epochs+1,5000)]
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

print(model.summary())