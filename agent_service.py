from tools.sales_prediction_tool import predict_sales
from tools.rag_tool import rag_search
from tools.image_tool import create_marketing_image
from services.llm_service import ask_llm

def agent_decision(user_query):

    system_prompt = """
    You are an AI Sales Agent.
    Decide which tool to use:
    
    Available tools:
    - sales_prediction
    - rag_search
    - image_generation
    - general_chat
    
    Respond ONLY with tool name.
    """

    tool = ask_llm(system_prompt + "\nUser: " + user_query)

    tool = tool.strip().lower()

    if "sales_prediction" in tool:
        # Dummy features for now
        result = predict_sales([1000, 200, 1])
        return f"Predicted Sales: {result}"

    elif "rag_search" in tool:
        result = rag_search(user_query)
        return result

    elif "image_generation" in tool:
        image = create_marketing_image(user_query)
        return image

    else:
        return ask_llm(user_query)
