import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, accuracy_score
from imblearn.over_sampling import SMOTE
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, InputLayer, Dropout, BatchNormalization
from tensorflow.keras.regularizers import l2
from tensorflow.keras.optimizers.legacy import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import tensorflowjs as tfjs

def load_data(filename):
    """Load dataset from a file and split it into features and labels, then apply SMOTE."""
    df = pd.read_csv(filename, sep=',', dtype=float)
    X = df.iloc[:, :-1].values
    y = df.iloc[:, -1].values

    sm = SMOTE(random_state=1341938091)
    X_res, y_res = sm.fit_resample(X, y)
    return X_res, y_res, df.columns[:-1]

def split_data(X, y, test_size=0.2):
    """Split the data into training and testing sets."""
    return train_test_split(X, y, test_size=test_size, random_state=42)

def create_model(input_shape):
    model = Sequential([
        InputLayer(input_shape=(input_shape,)),
        Dense(128, activation='tanh', kernel_regularizer=l2(0.001)),
        BatchNormalization(),
        Dropout(0.5),
        Dense(64, activation='tanh', kernel_regularizer=l2(0.0005)),
        BatchNormalization(),
        Dropout(0.5),
        Dense(32, activation='tanh', kernel_regularizer=l2(0.0005)),
        BatchNormalization(),
        Dropout(0.5),
        Dense(16, activation='tanh'),
        BatchNormalization(),
        Dropout(0.2),
        Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer=Adam(),
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    return model

def create_simplified_model(input_shape):
    model = Sequential([
        InputLayer(input_shape=(input_shape,)),
        
        # Reduced the complexity of the model by decreasing the number of neurons
        Dense(64, activation='relu', kernel_regularizer=l2(0.0005)), # Reduced regularization strength
        Dropout(0.1),  # Slightly reduced dropout rate
        
        # Removed one of the hidden layers to simplify the model further
        Dense(32, activation='relu', kernel_regularizer=l2(0.0005)),
        Dropout(0.1),
        
        # Output layer remains the same
        Dense(1, activation='sigmoid')
    ])
    
    model.compile(optimizer='adam',  # Consider experimenting with the learning rate or different optimizers
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    
    return model

def main(iterations=1000, target_accuracy=0.95):
    X, y, col_names = load_data('new_processed_dataset.csv')
    X_train, X_test, y_train, y_test = split_data(X, y)

    model = create_model(X_train.shape[1])
    
    # Setup callbacks
    early_stopping = EarlyStopping(monitor='val_accuracy', patience=10, verbose=1, mode='max', restore_best_weights=True)
    model_checkpoint = ModelCheckpoint('best_model.h5', monitor='val_accuracy', save_best_only=True, verbose=1, mode='max')
    
    # Train the model with validation data and callbacks
    history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=iterations, batch_size=32, verbose=1, callbacks=[early_stopping, model_checkpoint])
    
    # Load the best model saved by ModelCheckpoint
    model.load_weights('best_model.h5')
    
    # Evaluate the model
    y_pred = (model.predict(X_test) > 0.5).astype("int32")
    cm = confusion_matrix(y_test, y_pred)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"Best Accuracy: {accuracy}")
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot()
    plt.show()

    # Save the best model for TensorFlow.js
    tfjs.converters.save_keras_model(model, './new_model')


if __name__ == "__main__":
    main()
