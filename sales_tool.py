from tools.sales_prediction_tool import predict_sales

# Langchain tools temporarily disabled due to missing dependencies
# To enable, install: pip install langchain

def sales_prediction(features: str) -> str:
    """
    Predict sales.
    Input should be comma-separated numbers.
    Example: "1000,200,1"
    """
    values = [float(x) for x in features.split(",")]
    result = predict_sales(values)
    return f"Predicted Sales: {result}"
