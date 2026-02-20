import os
import requests

GROK_API_KEY = os.getenv("XAI_API_KEY")
DOODLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def call_grok(prompt):
    try:
        response = requests.post(
            "https://api.x.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROK_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "grok-beta",
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API returned {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def call_doodle(prompt):
    try:
        response = requests.post(
            "https://api.doodle.com/v1/chat",
            headers={
                "Authorization": f"Bearer {DOODLE_API_KEY}",
                "Content-Type": "application/json"
            },
            json={"prompt": prompt},
            timeout=10
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def generate_response(prompt, provider):
    if provider == "Grok":
        return call_grok(prompt)
    elif provider == "Doodle":
        return call_doodle(prompt)
    else:
        return {"error": f"Unknown provider: {provider}"}

def ask_llm(prompt, provider="Grok"):
    """
    Ask LLM a question using the specified provider.
    Returns the response text or error message.
    """
    response = generate_response(prompt, provider)
    
    if isinstance(response, dict) and "error" in response:
        return response["error"]
    
    # Extract text from response based on provider
    if provider == "Grok":
        try:
            return response.get("choices", [{}])[0].get("message", {}).get("content", "No response")
        except (IndexError, KeyError, TypeError):
            return str(response)
    elif provider == "Doodle":
        return response.get("response", str(response))
    
    return str(response)
