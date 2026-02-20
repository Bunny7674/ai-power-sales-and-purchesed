from flask import Blueprint, request, jsonify
import os
import requests

genai_bp = Blueprint("genai", __name__)

GROK_API_KEY = os.getenv("XAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


@genai_bp.route("/generate-content", methods=["POST"])
def generate_content():
    data = request.json
    prompt = data.get("prompt", "")
    provider = data.get("provider", "Grok")

    # Check if API key is available
    if not GROK_API_KEY:
        return jsonify({
            "status": "api_not_configured",
            "message": "Grok API not configured. Set XAI_API_KEY environment variable.",
            "content": f"Generated content for: {prompt[:100]}... (mock response - API key not set)"
        })

    try:
        response = requests.post(
            "https://api.x.ai/v1/chat/completions",  # Corrected endpoint for xAI/Grok
            headers={
                "Authorization": f"Bearer {GROK_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "grok-beta",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            },
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()
            # Extract content from Grok API response
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            return jsonify({
                "content": content,
                "provider": provider,
                "status": "success"
            })
        else:
            return jsonify({
                "status": "api_error",
                "message": f"Grok API returned status {response.status_code}",
                "content": f"Content suggestions for: {prompt[:100]}..."
            })

    except requests.exceptions.ConnectionError as e:
        return jsonify({
            "status": "connection_error",
            "message": "Cannot connect to Grok API. Please check your internet connection.",
            "content": f"Suggested content for: {prompt[:100]}... (using fallback)"
        })
    except requests.exceptions.Timeout:
        return jsonify({
            "status": "timeout",
            "message": "Grok API request timed out",
            "content": f"Quick response for: {prompt[:100]}..."
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "content": f"Content ideas for: {prompt[:100]}..."
        })

