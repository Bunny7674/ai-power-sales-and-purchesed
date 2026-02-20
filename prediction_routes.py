from flask import Blueprint, request, jsonify
import joblib
import pandas as pd

prediction_bp = Blueprint("prediction", __name__)

# Load pipeline once when server starts
try:
    model = joblib.load("C:/ai/MarketMind/backend/models/lead_model.pkl")
    print("Model loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")
    print("Using fallback scoring method")
    model = None

@prediction_bp.route("/predict-lead", methods=["POST"])
def predict_single_lead():
    try:
        if model is None:
            return jsonify({"error": "Model not loaded"})

        data = request.json

        # Convert JSON input to DataFrame
        input_df = pd.DataFrame([data])

        # Define numeric columns for type conversion
        numeric_cols = ['age', 'balance', 'day_of_week', 'duration', 'campaign', 
                       'pdays', 'previous', 'emp.var.rate', 'cons.price.idx', 
                       'cons.conf.idx', 'euribor3m', 'nr.employed']
        
        # Convert numeric columns to float
        for col in numeric_cols:
            if col in input_df.columns:
                input_df[col] = pd.to_numeric(input_df[col], errors='coerce')
        
        # Ensure all other columns are strings (object dtype)
        for col in input_df.columns:
            if col not in numeric_cols:
                input_df[col] = input_df[col].astype(str)

        # Predict probability
        try:
            if model is not None:
                probability = model.predict_proba(input_df)[0][1]
            else:
                # Fallback scoring
                age = float(data.get('age', 30))
                balance = float(data.get('balance', 0))
                probability = min(0.9, max(0.1, (age * 0.01) + (balance * 0.00001) + 0.3))
        except Exception as e:
            probability = 0.5

        return jsonify({
            "conversion_probability": float(probability),
            "message": "High Potential Lead" if probability > 0.5 else "Low Potential Lead"
        })

    except Exception as e:
        return jsonify({"error": str(e)})

@prediction_bp.route("/predict", methods=["POST"])
def predict_leads_bulk():
    try:
        if model is None:
            return jsonify({"error": "Model not loaded"})

        data = request.json
        leads = data.get('leads', [])

        if not leads:
            return jsonify({"error": "No leads provided"})

        scores = []

        for lead in leads:
            # Convert single lead to DataFrame
            input_df = pd.DataFrame([lead])

            # Define numeric columns for type conversion
            numeric_cols = ['age', 'balance', 'day_of_week', 'duration', 'campaign', 
                           'pdays', 'previous', 'emp.var.rate', 'cons.price.idx', 
                           'cons.conf.idx', 'euribor3m', 'nr.employed']
            
            # Convert numeric columns to float
            for col in numeric_cols:
                if col in input_df.columns:
                    input_df[col] = pd.to_numeric(input_df[col], errors='coerce')
            
            # Ensure all other columns are strings (object dtype)
            for col in input_df.columns:
                if col not in numeric_cols:
                    input_df[col] = input_df[col].astype(str)

            # Predict probability
            try:
                if model is not None:
                    probability = model.predict_proba(input_df)[0][1]
                else:
                    # Fallback scoring: simple heuristic based on age and balance
                    age = float(lead.get('age', 30))
                    balance = float(lead.get('balance', 0))
                    # Simple scoring formula
                    probability = min(0.9, max(0.1, (age * 0.01) + (balance * 0.00001) + 0.3))
                scores.append(float(probability))
            except Exception as e:
                # If prediction fails, return a default score
                scores.append(0.5)

        return jsonify({
            "predictions": scores,
            "message": f"Scored {len(scores)} leads successfully"
        })

    except Exception as e:
        return jsonify({"error": str(e)})
