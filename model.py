import numpy as np 
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def load_data(filename):
    """Load dataset from a file and split it into features and labels."""
    df = pd.read_csv(filename, sep=',', header=None)
    df = df.to_numpy()
    num_features = len(df[0]) - 1
    X = df[1:, 1:num_features]  # All rows, all columns except the last one
    y = df[1:, num_features]    # All rows, only the last column
    return X, y

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
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy

# Main execution
def main():
    # Load the data
    X, y = load_data('processed_dataset.csv')

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = split_data(X, y)

    # Train the model
    model = train_model(X_train, y_train)

    # Evaluate the model
    accuracy = evaluate_model(model, X_test, y_test)

    # Print the accuracy
    print("Model Accuracy:", accuracy)

if __name__ == "__main__":
    main()
