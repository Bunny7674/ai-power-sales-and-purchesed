from flask import Blueprint, request, jsonify
from services.agent_service import agent_decision

agent_bp = Blueprint("agent", __name__)

@agent_bp.route("/agent", methods=["POST"])
def run_agent():
    data = request.json
    query = data.get("query")

    response = agent_decision(query)

    return jsonify({"response": response})

@agent_bp.route("/agent", methods=["POST"])
def run_agent_route():
    data = request.json
    query = data.get("query")
    model = data.get("model")
    temperature = data.get("temperature")

    response = run_agent(query, model=model, temperature=temperature)

    return jsonify({"response": response})
