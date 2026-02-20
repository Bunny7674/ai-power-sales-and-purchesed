from tools.sales_prediction_tool import predict_sales
from tools.rag_tool import rag_search
from tools.image_tool import create_marketing_image

TOOLS = {
    "sales_prediction": {
        "function": predict_sales,
        "description": "Predict sales based on numerical features",
        "parameters": {
            "features": "List of numerical input values"
        }
    },
    "rag_search": {
        "function": rag_search,
        "description": "Search company documents",
        "parameters": {
            "query": "User query string"
        }
    },
    "image_generation": {
        "function": create_marketing_image,
        "description": "Generate marketing image",
        "parameters": {
            "prompt": "Text description for image"
        }
    }
}
