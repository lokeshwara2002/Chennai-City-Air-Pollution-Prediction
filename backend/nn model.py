import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def load_data(data_path="Real_Combine.csv"):
    """Load and preprocess data"""
    try:
        df = pd.read_csv(data_path)
        df.dropna(inplace=True)  # Remove missing values

        X = df.drop(columns=["PM 2.5"])
        y = df["PM 2.5"]

        return train_test_split(X, y, test_size=0.2, random_state=42)
    except Exception as e:
        logging.error(f"Error loading data: {str(e)}")
        return None, None, None, None

def build_model(input_dim):
    """Build an improved deep learning model"""
    model = keras.Sequential([
        keras.layers.Dense(128, activation='relu', input_shape=(input_dim,)),
        keras.layers.BatchNormalization(),  # Normalizes input data for stability
        keras.layers.Dropout(0.2),  # Reduces overfitting
        
        keras.layers.Dense(64, activation='relu'),
        keras.layers.BatchNormalization(),
        keras.layers.Dropout(0.2),

        keras.layers.Dense(32, activation='relu'),
        keras.layers.Dense(1)  # Output layer (no activation for regression)
    ])

    optimizer = keras.optimizers.Adam(learning_rate=0.01)  # Start with higher LR, decay later

    model.compile(loss='mse', optimizer=optimizer, metrics=['mae'])
    return model

def train_deep_learning(data_path="backend/Real_Combine.csv", model_path="pm25_nn_model.keras"):
    """Train and save an improved deep learning model"""
    try:
        X_train, X_test, y_train, y_test = load_data(data_path)
        if X_train is None:
            return
        
        # Standardize features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Build model
        model = build_model(input_dim=X_train.shape[1])

        # Learning rate scheduler
        lr_schedule = keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=10, verbose=1)

        # Early stopping
        early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=20, restore_best_weights=True, verbose=1)

        # Train model
        history = model.fit(
            X_train_scaled, y_train,
            validation_data=(X_test_scaled, y_test),
            epochs=500,
            batch_size=32,
            callbacks=[lr_schedule, early_stop],
            verbose=1
        )

        # Evaluate model
        y_pred = model.predict(X_test_scaled)
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)

        logging.info(f"Improved Neural Network -> MAE: {mae:.4f}, MSE: {mse:.4f}, RMSE: {rmse:.4f}")

        # Save model
        model.save(model_path)
        logging.info(f"Neural Network model saved to {model_path}")

    except Exception as e:
        logging.error(f"Error during training: {str(e)}")

def load_nn_model(model_path="pm25_nn_model.keras"):
    """Load the trained deep learning model"""
    try:
        return keras.models.load_model(model_path)
    except Exception as e:
        logging.error(f"Error loading model: {str(e)}")
        return None

def predict_pm25_nn(model, input_data):
    """Make predictions using the trained deep learning model"""
    return model.predict(input_data)

# Run training
train_deep_learning()
