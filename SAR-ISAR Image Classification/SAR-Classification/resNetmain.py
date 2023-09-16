"""
SAR Images recognition by CNN
"""
from DataLoader import loadDataset
from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt
from Model import SarNet, SarNet2
import numpy as np
import tensorflow as tf



DatasetPath = "/home/jany/Documents/GitHub/ISAR-Image-Classification/SAR-Classification/mstar"
# Chargement du jeu d'entrainement
X_train, y_train = loadDataset(DatasetPath + "/TRAIN")
# Chargement du jeu de test
X_test, y_test = loadDataset(DatasetPath + "/TEST")

#X_train = np.array(X_train)
#y_train = np.array(y_train)
#X_test = np.array(X_test)
#y_test = np.array(y_test)
#print(y_train)
y_train = y_train.reshape((y_train.shape[0], 1))
X_train = X_train.reshape((X_train.shape[0], 158, 158, 1))
X_test = X_test.reshape((X_test.shape[0], 158, 158, 1))
#print(y_train)
# One hot encoding
#y_train = to_categorical(y_train)
#y_test = to_categorical(y_test)
#print(y_train)


print("-------------------------------------------------------------")
print("|                 Format du jeu de données                  |")
print("-------------------------------------------------------------")
print("Format X_train : ", X_train.shape)
print("Format X_test : ", X_test.shape)
print("Format y_train : ", y_train.shape)
print("Format y_test : ", y_test.shape)
print("Format d'une image : ", X_train[0].shape)

print("-------------------------------------------------------------")
print("|                   Entrainement du model                   |")
print("-------------------------------------------------------------")
from ResnetModel import ResNet_Like
from tensorflow.keras import layers
from tensorflow import keras

model = ResNet_Like().model()
base_input = model.layers[0].input
base_output = model.layers[2].output
output = layers.Dense(10)(layers.Flatten()(base_output))
model = keras.Model(base_input, output)

model.compile(
    optimizer=keras.optimizers.Adam(),
    loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=["accuracy"],
)
model.summary()
history = model.fit(X_train, y_train, validation_split=0.1, batch_size=64, epochs=25)
print("Evaluation sur le jeu de test")
model.evaluate(X_test, y_test, batch_size=64, verbose=2)
model.save("pretrainedtest2")
print(history.history.keys())
print("-------------------------------------------------------------")
print("|                   Analyse des résultats                   |")
print("-------------------------------------------------------------")

plt.figure('Analyse des résultats SarNet2')
plt.subplot(121)
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')

plt.subplot(122)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()
