from flask import Blueprint, request, jsonify
from services.forecasting import forecast

forecast_bp = Blueprint("forecast", __name__)

@forecast_bp.route("/forecast", methods=["POST"])
def run_forecast():
    data = request.json
    series = data.get("data", [])
    periods = data.get("periods", 12)
    model = data.get("model", "simple")

    if not series:
        return jsonify({"error": "No data provided"}), 400

    try:
        # Call the forecasting service
        forecast_result = forecast(series, periods)

        return jsonify({
            "forecast": forecast_result,
            "periods": periods,
            "model": model
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500