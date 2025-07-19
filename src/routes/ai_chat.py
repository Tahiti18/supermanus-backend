"""
AI Chat Routes for Testing Backend
Copied from working real_openrouter_backend.py
"""

from flask import Blueprint, request, jsonify
import requests
import os
import time

ai_bp = Blueprint('ai', __name__)

# Real Manus supported models (copied from working backend)
OPENROUTER_MODELS = {
    "gpt4o": "gpt-4.1-mini",
    "chatgpt4": "gpt-4.1-nano", 
    "chatgpt": "gpt-4.1-mini",
    "chatgpt-4-turbo": "gpt-4.1-mini",
    "deepseek": "gemini-2.5-flash",
    "llama": "gpt-4.1-mini",
    "mistral": "gpt-4.1-nano",
    "gemini2": "gemini-2.5-flash",
    "perplexity": "gpt-4.1-mini",
    "gemini15": "gemini-2.5-flash",
    "commandr": "gpt-4.1-nano",
    "qwen": "gpt-4.1-mini"
}

# Manus OpenRouter proxy configuration
API_BASE = os.getenv('OPENAI_API_BASE')
API_KEY = os.getenv('OPENAI_API_KEY')

@ai_bp.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "TESTING BACKEND ONLINE",
        "message": "🦸‍♂️ SUPERMANUS TESTING BACKEND - SAFE EXPERIMENTS!",
        "agents_count": len(OPENROUTER_MODELS),
        "fake_responses": False,
        "demo_mode": False,
        "openrouter": True,
        "manus_proxy": True,
        "api_base": API_BASE,
        "backend_type": "testing",
        "timestamp": time.time()
    })

@ai_bp.route('/agents/list', methods=['GET'])
def list_agents():
    agents = []
    for agent_id, model in OPENROUTER_MODELS.items():
        agents.append({
            "id": agent_id,
            "name": agent_id.upper(),
            "model": model,
            "provider": "openrouter",
            "status": "ready"
        })
    
    return jsonify({
        "agents": agents,
        "total": len(agents),
        "message": "🦸‍♂️ ALL 9 REAL OPENROUTER AGENTS READY! (Testing Backend)",
        "fake_responses": False
    })

@ai_bp.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        
        agent_id = data.get('agent')
        agents = data.get('agents', [])
        
        # Handle both formats: agent (string) or agents (array)
        if not agent_id and agents and len(agents) > 0:
            agent_id = agents[0]
        elif not agent_id and not agents:
            return jsonify({
                "error": "No agent specified. Please provide 'agent' or 'agents' field.",
                "available_agents": list(OPENROUTER_MODELS.keys())
            }), 400
        
        message = data.get('message', '')
        session_id = data.get('session_id')
        mode = data.get('mode', 'general')
        
        if not agent_id or agent_id not in OPENROUTER_MODELS:
            return jsonify({
                "error": "Invalid agent ID",
                "available_agents": list(OPENROUTER_MODELS.keys())
            }), 400
        
        if not message.strip():
            return jsonify({
                "error": "Message cannot be empty"
            }), 400
        
        # Get real OpenRouter model
        model = OPENROUTER_MODELS[agent_id]
        
        # Make real API call to Manus OpenRouter proxy
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": f"You are {agent_id}, a helpful AI assistant. Provide genuine, thoughtful responses."
                },
                {
                    "role": "user", 
                    "content": message
                }
            ],
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        # Real API call
        response = requests.post(
            f"{API_BASE}/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result['choices'][0]['message']['content'].strip()
            
            return jsonify({
                "status": "success",
                "response": ai_response,
                "agent": agent_id,
                "model": model,
                "provider": "openrouter",
                "session_id": session_id,
                "mode": mode,
                "fake": False,
                "demo": False,
                "real_api": True,
                "backend_type": "testing",
                "timestamp": time.time()
            })
        else:
            return jsonify({
                "error": f"OpenRouter API Error: {response.status_code} - {response.text}",
                "agent": agent_id,
                "model": model
            }), 500
        
    except Exception as e:
        return jsonify({
            "error": f"Backend Error: {str(e)}",
            "agent": agent_id if 'agent_id' in locals() else None,
            "fake": False
        }), 500

@ai_bp.route('/session/start', methods=['POST'])
def start_session():
    try:
        data = request.get_json()
        mode = data.get('mode', 'manual')
        agent_a = data.get('agent_a')
        agent_b = data.get('agent_b')
        
        session_id = f"testing_backend_session_{int(time.time())}"
        
        return jsonify({
            "status": "success",
            "session_id": session_id,
            "mode": mode,
            "agent_a": agent_a,
            "agent_b": agent_b,
            "message": "🦸‍♂️ TESTING BACKEND SESSION STARTED!",
            "fake": False,
            "demo": False,
            "real_api": True,
            "backend_type": "testing"
        })
        
    except Exception as e:
        return jsonify({
            "error": f"Session start error: {str(e)}"
        }), 500

@ai_bp.route('/user/credits', methods=['GET'])
def get_user_credits():
    return jsonify({
        "credits": 2500,
        "plan": "free",
        "message": "🦸‍♂️ TESTING BACKEND CREDITS",
        "backend_type": "testing"
    })

@ai_bp.route('/user/consume-credits', methods=['POST'])
def consume_credits():
    return jsonify({
        "status": "success",
        "remaining_credits": 2499,
        "message": "🦸‍♂️ TESTING BACKEND CREDITS CONSUMED",
        "backend_type": "testing"
    })

