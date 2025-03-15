from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
import pandas as pd
import os
import logging
import datetime
import numpy as np
import json
from backend.model import load_model, predict_pm25

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Mount static files directory
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

# File paths
DATA_PATH = "backend/Real_Combine.csv"
MODEL_PATH = "backend/pm25_model.joblib"
HISTORY_FILE = "backend/history.json"

# Load dataset
if not os.path.exists(DATA_PATH):
    logger.error(f"Dataset file '{DATA_PATH}' not found.")
    raise FileNotFoundError(f"Dataset file '{DATA_PATH}' not found.")

df = pd.read_csv(DATA_PATH)

# Load trained model
if not os.path.exists(MODEL_PATH):
    logger.error(f"Model file '{MODEL_PATH}' not found.")
    raise FileNotFoundError(f"Model file '{MODEL_PATH}' not found.")

model = load_model(MODEL_PATH)

# Ensure `history.json` exists
if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w") as file:
        json.dump([], file)

# ✅ Load history from JSON
def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    
    try:
        with open(HISTORY_FILE, "r") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, FileNotFoundError):
        return []

# ✅ Save history to JSON
def save_history(history):
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)

@app.get("/")
async def read_root():
    """Serve the index.html file."""
    try:
        with open("backend/static/index.html", "r") as file:
            return HTMLResponse(content=file.read(), status_code=200)
    except Exception as e:
        logger.error(f"Error reading index.html: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to load the homepage.")

@app.get("/history.html", response_class=HTMLResponse)
async def get_history_page():
    """Serve history.html file"""
    try:
        with open("backend/static/history.html", "r") as file:
            return HTMLResponse(content=file.read(), status_code=200)
    except Exception as e:
        logger.error(f"Error reading history.html: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to load history page.")

@app.get("/data")
def get_data():
    """Return the dataset without missing values."""
    try:
        logger.info("Fetching dataset...")
        return df.dropna().to_dict(orient="records")
    except Exception as e:
        logger.error(f"Error retrieving dataset: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving dataset: {str(e)}")

@app.post("/predict")
def predict(input_data: dict):
    """Predict PM2.5 level and store in history.json."""
    try:
        required_fields = ["T", "TM", "Tm", "SLP", "H", "V"]
        if not all(field in input_data for field in required_fields):
            raise HTTPException(status_code=400, detail="Missing required input fields")

        input_data = {key: float(value) for key, value in input_data.items()}

        input_df = pd.DataFrame([input_data])
        prediction = predict_pm25(model, input_df)
        predicted_pm25 = round(prediction[0], 2)

        history_entry = {
            "date": datetime.date.today().strftime("%Y-%m-%d"),
            **input_data,
            "predicted_pm25": predicted_pm25
        }

        history_data = load_history()
        history_data.append(history_entry)
        save_history(history_data)

        return {"prediction": predicted_pm25}

    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/history.json")
def get_history():
    """Fetch stored prediction history."""
    try:
        history = load_history()
        return JSONResponse(content=history, status_code=200)
    except Exception as e:
        logger.error(f"Error loading history: {str(e)}")
        return JSONResponse(content={"error": "Failed to load history"}, status_code=500)

@app.get("/get-forecast")
def get_forecast(days: int = Query(7, title="Number of days to predict")):
    """Predict future PM2.5 levels dynamically."""
    try:
        today = datetime.date.today()
        future_dates = [today + datetime.timedelta(days=i) for i in range(days)]

        avg_T, avg_TM, avg_Tm, avg_SLP, avg_H, avg_V = df[["T", "TM", "Tm", "SLP", "H", "V"]].mean()

        predictions = []
        for i in range(days):
            features = np.array([[avg_T, avg_TM, avg_Tm, avg_SLP, avg_H, avg_V]])
            predicted_pm25 = model.predict(features)[0]
            predictions.append({"date": future_dates[i].strftime("%Y-%m-%d"), "predicted_pm25": round(predicted_pm25, 2)})

        return predictions
    except Exception as e:
        logger.error(f"Error during forecasting: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


