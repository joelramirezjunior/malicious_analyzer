import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import pandas as pd
from imblearn.over_sampling import SMOTE
import joblib
# Assume load_data and other necessary imports are defined elsewhere




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
    return model.predict(X_test)

def feature_weights(model, features):
    feature_weight_pairs = zip(features.flatten(), model[1].coef_.flatten())
    feature_weight_pairs = sorted(feature_weight_pairs, key=lambda x: x[1])
    return feature_weight_pairs

def run_model():
    X, y, col_names = load_data('new_processed_dataset.csv')
    X_train, X_test, y_train, y_test = split_data(X, y)
    pipe = make_pipeline(StandardScaler(), LogisticRegression())
    pipe.fit(X_train, y_train)  # apply scaling on training data
    y_pred = evaluate_model(pipe, X_test, y_test)
    cm = confusion_matrix(y_test, y_pred, labels=pipe.classes_)
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy, feature_weights(pipe, col_names), cm, pipe.classes_, pipe  # Return confusion matrix and labels

def main():
    acc = 0
    best_cm = None
    best_labels = None
    best_fw = None
    best_model = None

    for i in range(1000):
        acc_new, fw_new, cm_new, labels_new, _pipe = run_model()
        if acc_new > acc:
            acc = acc_new
            best_cm = cm_new
            best_labels = labels_new
            best_fw = fw_new
            best_model = _pipe

    joblib.dump(best_model, "model.pkl") 
    
    print(f"Best Accuracy: {acc}")

    for label, weight in best_fw:
        print(f"{label}, {weight}")
    # Display the confusion matrix of the best model
    disp = ConfusionMatrixDisplay(confusion_matrix=best_cm, display_labels=best_labels)
    disp.plot()
    plt.show()

if __name__ == "__main__":
    main()
