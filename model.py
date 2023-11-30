# Train a model! 
# Logistic Regression


# Import the libaries

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np 
import pandas as pd


# load your data

# set x and y
# trying to classify the type of plant
#X is going to be what the model will use to learn how to predict
#X is a matrix of values


#x1 -> length of stem
#x2 -> length of the petal
#x3 -> the color of the flower 
#x4 -> the width of the petal

#y is the actual answer!
#y -> the type of plant it is


df = pd.read_csv('./dataset/data.csv', sep=',', header=None)
df = df.to_numpy()
num_features = len(df[0]) - 1

X = df[:,0:num_features]
y = df[:,num_features]

print(X)
print(y)

# make train and test data 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .2)

# print("X_train: ", X_train)
# print("X_test: ", X_test)
# print("y_train: ", y_train)
# print("y_test: ", y_test)

# fit the model (training)
logistic_regression = LogisticRegression(random_state=42)

logistic_regression.fit(X_train, y_train)

# predict using the model
y_pred = logistic_regression.predict(X_test)

# print out predictions and get the Accuracy!
accuracy = accuracy_score(y_test, y_pred)
print(accuracy)





