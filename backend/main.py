from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import pandas as pd
import os
import logging
from backend.model import load_model, predict_pm25

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

# Load dataset
DATA_PATH = r"C:\Users\ruchi\OneDrive\Desktop\chennai city project\backend\Real_Combine.csv"
if not os.path.exists(DATA_PATH):
    logger.error(f"The dataset file '{DATA_PATH}' was not found.")
    raise FileNotFoundError(f"The dataset file '{DATA_PATH}' was not found. Please ensure it exists in the correct directory.")
df = pd.read_csv(DATA_PATH)

# Load trained ML model
MODEL_PATH = r"C:\Users\ruchi\OneDrive\Desktop\chennai city project\backend\pm25_model.joblib"
if not os.path.exists(MODEL_PATH):
    logger.error(f"The model file '{MODEL_PATH}' was not found.")
    raise FileNotFoundError(f"The model file '{MODEL_PATH}' was not found. Please ensure it exists in the correct directory.")
model = load_model(MODEL_PATH)

@app.get("/")
async def read_root():
    # Serve the index.html file
    try:
        with open("backend/static/index.html", "r") as file:
            return HTMLResponse(content=file.read(), status_code=200)
    except Exception as e:
        logger.error(f"Error reading index.html: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to load the dashboard.")

@app.get("/data")
def get_data():
    """Return the entire dataset."""
    try:
        logger.info("Fetching dataset...")
        cleaned_df = df.dropna()  # Drop rows with NaN values
        return cleaned_df.to_dict(orient="records")
    except Exception as e:
        logger.error(f"Error retrieving dataset: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving dataset: {str(e)}")

@app.post("/predict")
def predict(input_data: dict):
    """Predict PM2.5 level based on input features."""
    try:
        input_df = pd.DataFrame([input_data])
        prediction = predict_pm25(model, input_df)
        return {"prediction": prediction[0]}
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))