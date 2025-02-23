# -*- coding: utf-8 -*-
"""ANN.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/156eIv6aGGpGdTob_DkS5FemxOE7RptqE
"""

import pandas as pd
# Load the dataset
df = pd.read_csv('Alphabets_data.csv')
df.head()

df.shape

df.describe().transpose()

df.isnull().sum()

df.info()

# Data Visualizeation
import matplotlib.pyplot as plt
import seaborn as sns
sns.countplot(x="letter", data=df)
plt.show()

# Select only numeric columns for correlation analysis
num_col = df.select_dtypes(include=[float, int])
if not num_col.empty:
    sns.heatmap(num_col.corr(), annot=True, cmap='coolwarm')
    plt.show()

# Normalize the features
X = df.drop('letter', axis=1)
y = df['letter']

from sklearn.preprocessing import StandardScaler, LabelEncoder
from tensorflow.keras.utils import to_categorical
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Convert labels to categorical (one-hot encoding)
LE = pd.factorize(y)[0]
y = to_categorical(LE)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Input
from tensorflow.keras.utils import to_categorical

# Build the ANN model
model = Sequential([
    Input(shape=(X_train.shape[1],)),  # Explicitly define the input shape
    Dense(64, activation='relu'),
    #Dense(64, activation='relu'),
    Dense(len(y_train[0]), activation='softmax')
])

# Compile the model
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Train the model
history = model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)

model_loss  = pd.DataFrame(model.history.history)
model_loss

model_loss.plot()

from tensorflow.keras.callbacks import EarlyStopping
early_stop = EarlyStopping(monitor='val_loss', mode='min',verbose=1,patience=25)

model.fit(x = X_train, y = y_train, epochs=500, validation_data=(X_test,y_test),verbose=1,callbacks=[early_stop])

model_loss  = pd.DataFrame(model.history.history)
model_loss

model_loss.plot()

Y_pred_train = model.predict(X_train)
Y_pred_train

Y_pred_test = model.predict(X_test)
Y_pred_test

Y_pred_train_final = (Y_pred_train>0.5).astype(int)
Y_pred_test_final = (Y_pred_test>0.5).astype(int)

import numpy as np
from sklearn.metrics import accuracy_score
ac1 = accuracy_score(y_train,Y_pred_train_final)
ac2 = accuracy_score(y_test,Y_pred_test_final)

print("Training score: ",np.round(ac1,2))
print("Test score: ",np.round(ac2,2))

pip install keras-tuner

import keras_tuner as kt

def build_model(hp):
  model = Sequential()
  model.add(Input(shape=(X_train.shape[1],)))

  # Tune the number of hidden layers and neurons per layer
  for i in range(hp.Int('num_layers', 1, 3)):  # Try 1 to 3 hidden layers
    model.add(Dense(units=hp.Int(f'units_{i}', min_value=32, max_value=128, step=32),
                    activation=hp.Choice(f'activation_{i}', ['relu', 'tanh'])))

  model.add(Dense(len(y_train[0]), activation='softmax'))

  # Tune the learning rate
  learning_rate = hp.Float('learning_rate', min_value=1e-4, max_value=1e-2, step=1e-4)
  optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)

  model.compile(optimizer=optimizer,
                loss='categorical_crossentropy',
                metrics=['accuracy'])
  return model

# Initialize the tuner
tuner = kt.RandomSearch(
    build_model,
    objective='val_accuracy',  # Optimize for validation accuracy
    max_trials=5,  # Number of different hyperparameter combinations to try
    directory='my_tuning_dir',
    project_name='alphabet_classification'
)

# Perform hyperparameter tuning
tuner.search(X_train, y_train, epochs=10, validation_split=0.2)

# Get the best hyperparameters
best_hps = tuner.get_best_hyperparameters(num_trials=1)[0]

# Build the model with the best hyperparameters
best_model = tuner.hypermodel.build(best_hps)

# Train the best model
early_stop = EarlyStopping(monitor='val_loss', mode='min', patience=25)
best_model.fit(X_train, y_train, epochs=50, validation_split=0.2, callbacks=[early_stop])

# Evaluate the best model
Y_pred_test = best_model.predict(X_test)
Y_pred_test_final = (Y_pred_test>0.5).astype(int)
ac2 = accuracy_score(y_test,Y_pred_test_final)
print("Test score with best hyperparameters: ",np.round(ac2,2))

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Convert one-hot encoded predictions back to class labels
Y_pred_test_labels = np.argmax(Y_pred_test_final, axis=1)

# Convert one-hot encoded y_test to class labels (already done earlier)
y_test_labels = np.argmax(y_test, axis=1)

# Calculate metrics
accuracy = accuracy_score(y_test_labels, Y_pred_test_labels)
precision = precision_score(y_test_labels, Y_pred_test_labels, average='macro')
recall = recall_score(y_test_labels, Y_pred_test_labels, average='macro')
f1 = f1_score(y_test_labels, Y_pred_test_labels, average='macro')

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1-score:", f1)

