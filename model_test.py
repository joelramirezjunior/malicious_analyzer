import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import pandas as pd
from imblearn.over_sampling import SMOTE
import joblib


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

    return X_res, y_res, features_labels


# def split_data(X, y, test_size=0.2):
#     """Split the data into training and testing sets."""
#     return train_test_split(X, y, test_size=test_size)

def main():
    model =  joblib.load("model.pkl")
    X, y, labels = load_data("new_processed_dataset.csv")
    pred = model.predict([X[0]])
    print(pred)
    print(f"Correct answer: {y[0]}")

if __name__ == "__main__":
    main()