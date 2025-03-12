import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib

# Load dataset
df = pd.read_csv("backend/Real_Combine.csv")
df.dropna(inplace=True)

X = df.drop(columns=["PM 2.5"])
y = df["PM 2.5"]

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the data for Neural Network
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Save the scaler for later use
joblib.dump(scaler, "backend/scaler.pkl")

# ------------------ Train Random Forest ------------------
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Save the Random Forest model
joblib.dump(rf_model, "backend/pm25_model.joblib")

# Predictions using Random Forest
y_pred_rf = rf_model.predict(X_test)

# Evaluation Metrics for Random Forest
mae_rf = mean_absolute_error(y_test, y_pred_rf)
mse_rf = mean_squared_error(y_test, y_pred_rf)
rmse_rf = np.sqrt(mse_rf)

# ------------------ Train Neural Network ------------------
nn_model = keras.Sequential([
    keras.layers.Dense(64, activation="relu", input_shape=(X_train.shape[1],)),
    keras.layers.Dense(64, activation="relu"),
    keras.layers.Dense(1)  # Output layer for regression
])

nn_model.compile(optimizer="adam", loss="mse", metrics=["mae"])

# Train the Neural Network
nn_model.fit(X_train_scaled, y_train, epochs=50, batch_size=16, validation_data=(X_test_scaled, y_test), verbose=1)

# Save the trained Neural Network model
nn_model.save("backend/nn_pm25_model.h5")

# Predictions using Neural Network
y_pred_nn = nn_model.predict(X_test_scaled)

# Evaluation Metrics for Neural Network
mae_nn = mean_absolute_error(y_test, y_pred_nn)
mse_nn = mean_squared_error(y_test, y_pred_nn)
rmse_nn = np.sqrt(mse_nn)

# ------------------ Print Comparison ------------------
print("\nModel Performance Comparison:")
print(f"Random Forest  -> MAE: {mae_rf:.4f}, MSE: {mse_rf:.4f}, RMSE: {rmse_rf:.4f}")
print(f"Neural Network -> MAE: {mae_nn:.4f}, MSE: {mse_nn:.4f}, RMSE: {rmse_nn:.4f}")
