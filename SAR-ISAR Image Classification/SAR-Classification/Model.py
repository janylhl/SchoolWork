import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten



def SarNet(input_shape=(28, 28,1)):
    model = Sequential()
    model.add(Conv2D(filters = 32, kernel_size = (5, 5), padding = "same", input_shape = input_shape,activation = "relu"))
    model.add(MaxPooling2D((4,4)))
    model.add(Conv2D(filters = 64, kernel_size = (3, 3), padding = "same",activation = "relu"))
    model.add(MaxPooling2D((4, 4)))
    model.add(Flatten())
    model.add(Dense(10, activation="softmax"))
    model.summary()
    return model

def SarNet2(input_shape=(28, 28,1)):
    model = Sequential()
    model.add(Conv2D(filters = 32, kernel_size = (5, 5), padding = "same", input_shape = input_shape,activation = "relu"))
    model.add(MaxPooling2D((4,4)))
    model.add(Conv2D(filters = 64, kernel_size = (3, 3), padding = "same", input_shape = input_shape ,activation = "relu"))
    model.add(MaxPooling2D((2,2), strides=2))
    model.add(Conv2D(filters=128, kernel_size=(2, 2), padding="same", activation="relu"))
    model.add(MaxPooling2D((2,2), strides=2))
    model.add(Flatten())
    #model.add(Dense(512, activation="relu"))
    #model.add(Dropout(0.5))
    model.add(Dense(10, activation="softmax"))
    return model