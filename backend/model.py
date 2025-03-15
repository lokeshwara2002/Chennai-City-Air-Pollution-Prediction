import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib
import numpy as np
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def train_model(data_path="backend/Real_Combine.csv", model_path="pm25_model.joblib"):
    """Train an improved Random Forest model to predict PM2.5 levels."""
    try:
        # Load dataset
        df = pd.read_csv(data_path)
        df.dropna(inplace=True)  # Remove NaN values
        
        # Split features and target
        X = df.drop(columns=["PM 2.5"])
        y = df["PM 2.5"]
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Define improved Random Forest model
        model = RandomForestRegressor(
            n_estimators=300,      # Increased trees
            max_depth=20,          # Restrict tree depth
            min_samples_split=5,   # Minimum samples to split
            max_features="sqrt",   # Use sqrt(features) for best split
            random_state=42,
            n_jobs=-1              # Use all CPU cores
        )
        
        # Train model
        model.fit(X_train, y_train)
        
        # Predictions
        y_pred = model.predict(X_test)
        
        # Model evaluation
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        
        logging.info(f"Improved Random Forest Model Performance:")
        logging.info(f"MAE: {mae:.4f}, MSE: {mse:.4f}, RMSE: {rmse:.4f}")
        
        # Save model
        joblib.dump(model, model_path)
        logging.info(f"Model saved successfully to {model_path}")
    except Exception as e:
        logging.error(f"Error during model training: {str(e)}")

def load_model(model_path="pm25_model.joblib"):
    """Load the trained Random Forest model."""
    try:
        return joblib.load(model_path)
    except Exception as e:
        logging.error(f"Error loading model: {str(e)}")

def predict_pm25(model, input_data):
    """Make predictions using the trained model."""
    return model.predict(input_data)

# Run training
if __name__ == "__main__":
    train_model()
