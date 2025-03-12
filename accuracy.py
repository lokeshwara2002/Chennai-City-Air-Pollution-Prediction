import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def train_model(data_path=r"C:\Users\ruchi\OneDrive\Desktop\chennai city project\backend\Real_Combine.csv", model_path="pm25_model.joblib", model_type="random_forest"):
    """Train a model to predict PM2.5 levels."""
    try:
        # Load the dataset
        df = pd.read_csv(data_path)
        df.dropna(inplace=True)  # Remove rows with NaN values
        
        # Split features and target
        X = df.drop(columns=["PM 2.5"])
        y = df["PM 2.5"]
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Initialize the model
        if model_type == "random_forest":
            model = RandomForestRegressor(n_estimators=100, random_state=42)
        else:
            raise ValueError("Invalid model type specified.")
        
        # Train the model
        model.fit(X_train, y_train)
        
        # Evaluate the model
        y_pred = model.predict(X_test)
        
        # Calculate evaluation metrics
        mse = mean_squared_error(y_test, y_pred)
        rmse = mse ** 0.5  # Root Mean Squared Error
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        # Log the metrics
        logging.info(f"Model Evaluation Metrics:")
        logging.info(f"Mean Squared Error (MSE): {mse}")
        logging.info(f"Root Mean Squared Error (RMSE): {rmse}")
        logging.info(f"Mean Absolute Error (MAE): {mae}")
        logging.info(f"R² Score: {r2}")
        
        # Save the model
        joblib.dump(model, model_path)
        logging.info(f"Model type: {model_type} saved to {model_path}")
    except Exception as e:
        logging.error(f"Error during model training: {str(e)}")

def load_model(model_path="pm25_model.joblib"):
    """Load the trained model."""
    try:
        return joblib.load(model_path)
    except Exception as e:
        logging.error(f"Error loading model: {str(e)}")

def predict_pm25(model, input_data):
    """Make predictions using the trained model."""
    return model.predict(input_data)

# Run the training function
if __name__ == "__main__":
    train_model()