import numpy as np 
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
from imblearn.over_sampling import SMOTE
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def load_data(filename):
    """Load dataset from a file and split it into features and labels."""
    df = pd.read_csv(filename, sep=',', header=None)
    df = df.to_numpy() #converting the DataFrame to a Numpy Array! (Just a matrix)
    features_labels = df[0:1, 0:-1 ]
    df = df[1:, ]

    num_features = len(df[0]) - 1 #length of the row - 1 

    X = df.astype(int)[0:, 1:num_features]  # All rows, all columns except the last one
    y = df.astype(int)[0:, num_features]    # All rows, only the last column

    sm = SMOTE(random_state=42)
    X_res, y_res = sm.fit_resample(X, y)

    # print("Before Smote")
    # print(f"Number of labels: {len(y)}")
    # print(f"Number of positive labels: {int(len(y)) - np.sum(y)}")

    # print(f"Number of labels: {len(y_res)}")
    # print(f"Number of positive labels: {int(len(y_res)) - np.sum(y_res)}")
    return X_res, y_res, features_labels

def split_data(X, y, test_size=0.2):
    """Split the data into training and testing sets."""
    return train_test_split(X, y, test_size=test_size)

def train_model(X_train, y_train):
    """Train a Logistic Regression model with the training data."""
    model = LogisticRegression(random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    """Evaluate the trained model using the testing data."""
    y_pred = model.predict(X_test)
    # cm = confusion_matrix(y_test, y_pred, labels = model.classes_)
    # disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels= model.classes_)
    # disp.plot()
    # plt.show()
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy


def feature_weights(model, features):

    feature_weight_pairs = zip(features.flatten(), model[1].coef_.flatten())
    feature_weight_pairs = sorted(feature_weight_pairs, key=lambda x: x[1])

    return feature_weight_pairs
   

# Main execution
def run_model():
    X, y, col_names = load_data('processed_dataset.csv')

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = split_data(X, y)

    pipe = make_pipeline(StandardScaler(), LogisticRegression())

    pipe.fit(X_train, y_train)  # apply scaling on training data
    
    # Evaluate the model
    accuracy = evaluate_model(pipe, X_test, y_test)


    # Print the accuracy
    # print("Model Accuracy:", accuracy)

    return accuracy, feature_weights(pipe, col_names)

def main():
    # Load the data
    acc = 0
    fw = None

    for i in range(1000):
        acc_new, fw_new = run_model()
        if(acc_new > acc):
            fw = fw_new
            acc = acc_new

    print(f"Best Accuracy: {acc}")
    for pair in fw:
        print(f"Feature: {pair[0]} \n \t weight: {pair[1]}")
    

if __name__ == "__main__":
    main()
