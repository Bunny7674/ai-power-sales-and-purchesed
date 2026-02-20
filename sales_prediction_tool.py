import joblib
import numpy as np
import os

# Load model safely - fallback if not found
model = None
model_path = os.path.join(os.path.dirname(__file__), "..", "models", "trained_model.pkl")
if os.path.exists(model_path):
    model = joblib.load(model_path)

def predict_sales(features):
    """
    features: list of numerical values
    """
    if model is None:
        # Return a mock prediction if model not available
        return np.mean(features) * 10.0
    
    prediction = model.predict([features])
    return float(prediction[0])

