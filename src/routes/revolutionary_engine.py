from flask import Blueprint, request, jsonify
import requests
import json
import time
from datetime import datetime
import os
import threading
from queue import Queue

revolutionary_engine_bp = Blueprint('revolutionary_engine', __name__)

# THE REVOLUTIONARY 20-AGENT POWERHOUSE (NO COLLABORATION KILLERS)
REVOLUTIONARY_AGENTS = [
    # BUSINESS STRATEGY POWERHOUSES
    {'id': 1, 'name': 'GPT-4o', 'model': 'openai/gpt-4o', 'category': 'business', 'specialty': 'Strategic analysis and planning'},
    {'id': 2, 'name': 'Command R+', 'model': 'cohere/command-r-plus', 'category': 'business', 'specialty': 'Enterprise solutions'},
    {'id': 3, 'name': 'Gemini Pro 1.5', 'model': 'google/gemini-pro-1.5', 'category': 'business', 'specialty': 'Market analysis'},
    {'id': 4, 'name': 'GPT-4 Turbo', 'model': 'openai/gpt-4-turbo', 'category': 'business', 'specialty': 'Business optimization'},
    
    # TECHNICAL CODING MASTERS
    {'id': 5, 'name': 'DeepSeek R1', 'model': 'deepseek/deepseek-r1', 'category': 'technical', 'specialty': 'Advanced reasoning and coding'},
    {'id': 6, 'name': 'Qwen 2.5 Coder', 'model': 'qwen/qwen-2.5-coder-32b-instruct', 'category': 'technical', 'specialty': 'Code generation'},
    {'id': 7, 'name': 'Mixtral 8x22B', 'model': 'mistralai/mixtral-8x22b-instruct', 'category': 'technical', 'specialty': 'Technical problem solving'},
    {'id': 8, 'name': 'WizardLM 2', 'model': 'microsoft/wizardlm-2-8x22b', 'category': 'technical', 'specialty': 'Reasoning and logic'},
    
    # CREATIVE RESEARCH INNOVATORS
    {'id': 9, 'name': 'Gemini 2.0 Flash', 'model': 'google/gemini-2.0-flash-exp', 'category': 'creative', 'specialty': 'Creative thinking'},
    {'id': 10, 'name': 'Perplexity Pro', 'model': 'perplexity/llama-3.1-sonar-huge-128k-online', 'category': 'research', 'specialty': 'Research and fact-finding'},
    {'id': 11, 'name': 'Llama 3.3 70B', 'model': 'meta-llama/llama-3.3-70b-instruct', 'category': 'creative', 'specialty': 'Creative exploration'},
    {'id': 12, 'name': 'Yi Large', 'model': '01-ai/yi-large', 'category': 'analysis', 'specialty': 'Innovative solutions'},
    
    # COMMUNICATION ANALYSIS EXPERTS
    {'id': 13, 'name': 'Mistral Large', 'model': 'mistralai/mistral-large', 'category': 'communication', 'specialty': 'Communication and analysis'},
    {'id': 14, 'name': 'Qwen 2.5 72B', 'model': 'qwen/qwen-2.5-72b-instruct', 'category': 'multilingual', 'specialty': 'Multilingual expertise'},
    {'id': 15, 'name': 'Nous Hermes 3', 'model': 'nousresearch/nous-hermes-2-mixtral-8x7b-dpo', 'category': 'collaboration', 'specialty': 'Uncensored collaboration'},
    {'id': 16, 'name': 'OpenHermes 2.5', 'model': 'teknium/openhermes-2.5-mistral-7b', 'category': 'collaboration', 'specialty': 'Collaborative intelligence'},
    
    # SYNTHESIS SUMMARY SPECIALISTS
    {'id': 17, 'name': 'Dolphin Mixtral', 'model': 'cognitivecomputations/dolphin-2.6-mixtral-8x7b', 'category': 'synthesis', 'specialty': 'Uncensored synthesis'},
    {'id': 18, 'name': 'Starling 7B', 'model': 'berkeley-nest/starling-lm-7b-alpha', 'category': 'synthesis', 'specialty': 'Fast collaborative synthesis'},
    {'id': 19, 'name': 'Neural Chat', 'model': 'intel/neural-chat-7b-v3-1', 'category': 'communication', 'specialty': 'Intelligent conversation'},
    {'id': 20, 'name': 'Zephyr Beta', 'model': 'huggingfaceh4/zephyr-7b-beta', 'category': 'synthesis', 'specialty': 'Advanced reasoning synthesis'}
]

class RevolutionaryEngine:
    """THE MOST POWERFUL AI ORCHESTRATION ENGINE EVER BUILT"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENROUTER_API_KEY', '')
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://thepromptlink.com",
            "X-Title": "PromptLink Revolutionary Engine"
        }
        self.current_session = {}
    
    def expert_panel_mode(self, prompt, session_id):
        """10 PAIRS OF EXPERTS WORKING INDEPENDENTLY - SEQUENTIAL PROCESSING"""
        
        print(f"🏛️ EXPERT PANEL MODE: 10 Independent Expert Pairs")
        print(f"📋 Session: {session_id}")
        
        # Initialize session tracking
        self.current_session[session_id] = {
            'mode': 'expert_panel',
            'status': 'running',
            'current_pair': 0,
            'total_pairs': 10,
            'results': [],
            'start_time': datetime.utcnow()
        }
        
        # Process 10 pairs sequentially (agents 1-20)
        for pair_num in range(10):
            agent_a = REVOLUTIONARY_AGENTS[pair_num * 2]
            agent_b = REVOLUTIONARY_AGENTS[pair_num * 2 + 1]
            
            print(f"🤝 Processing Pair {pair_num + 1}: {agent_a['name']} + {agent_b['name']}")
            
            # Update session status
            self.current_session[session_id]['current_pair'] = pair_num + 1
            self.current_session[session_id]['current_agents'] = [agent_a['name'], agent_b['name']]
            
            # Agent A analyzes the prompt
            print(f"🤖 Agent A ({agent_a['name']}) analyzing...")
            response_a = self._call_agent(agent_a, prompt, session_id)
            
            if response_a:
                # Agent B gets prompt + Agent A's response
                combined_input = f"ORIGINAL PROMPT: {prompt}\n\nCOLLEAGUE'S ANALYSIS: {response_a}\n\nProvide your own expert analysis and build upon or challenge the colleague's insights:"
                
                print(f"🤖 Agent B ({agent_b['name']}) responding...")
                response_b = self._call_agent(agent_b, combined_input, session_id)
                
                # Store pair results
                pair_result = {
                    'pair_number': pair_num + 1,
                    'agent_a': {
                        'id': agent_a['id'],
                        'name': agent_a['name'],
                        'specialty': agent_a['specialty'],
                        'response': response_a
                    },
                    'agent_b': {
                        'id': agent_b['id'],
                        'name': agent_b['name'],
                        'specialty': agent_b['specialty'],
                        'response': response_b
                    },
                    'timestamp': datetime.utcnow().isoformat()
                }
                
                self.current_session[session_id]['results'].append(pair_result)
                print(f"✅ Pair {pair_num + 1} completed successfully")
            else:
                print(f"❌ Pair {pair_num + 1} failed")
        
        # Mark session complete
        self.current_session[session_id]['status'] = 'completed'
        self.current_session[session_id]['end_time'] = datetime.utcnow()
        
        return self.current_session[session_id]
    
    def conference_chain_mode(self, prompt, session_id, max_agents=20):
        """STICKY CONTEXT CONFERENCE CHAIN - SEQUENTIAL PROCESSING"""
        
        print(f"🔗 CONFERENCE CHAIN MODE: 20-Agent Sticky Context Chain")
        print(f"📋 Session: {session_id}")
        
        # Initialize session tracking
        self.current_session[session_id] = {
            'mode': 'conference_chain',
            'status': 'running',
            'current_agent': 0,
            'total_agents': max_agents,
            'results': [],
            'start_time': datetime.utcnow()
        }
        
        current_context = prompt
        
        # Process all 20 agents sequentially
        for i in range(max_agents):
            agent = REVOLUTIONARY_AGENTS[i]
            
            print(f"🎯 Processing Agent {i + 1}/{max_agents}: {agent['name']}")
            
            # Update session status
            self.current_session[session_id]['current_agent'] = i + 1
            self.current_session[session_id]['current_agent_name'] = agent['name']
            
            # Create sticky prompt
            if i == 0:
                agent_input = prompt
            else:
                agent_input = f"ORIGINAL PROMPT: {prompt}\n\nPREVIOUS EXPERT'S INSIGHT: {current_context}\n\nBuild upon this analysis with your {agent['specialty']} expertise:"
            
            print(f"🤖 {agent['name']} analyzing...")
            response = self._call_agent(agent, agent_input, session_id)
            
            if response:
                # Update context for next agent
                current_context = response
                
                # Store result
                agent_result = {
                    'position': i + 1,
                    'agent_id': agent['id'],
                    'agent_name': agent['name'],
                    'agent_specialty': agent['specialty'],
                    'response': response,
                    'timestamp': datetime.utcnow().isoformat()
                }
                
                self.current_session[session_id]['results'].append(agent_result)
                print(f"✅ Agent {i + 1} completed successfully")
            else:
                print(f"❌ Agent {i + 1} failed")
        
        # Mark session complete
        self.current_session[session_id]['status'] = 'completed'
        self.current_session[session_id]['end_time'] = datetime.utcnow()
        self.current_session[session_id]['final_synthesis'] = current_context
        
        return self.current_session[session_id]
    
    def _call_agent(self, agent, prompt, session_id):
        """Call individual agent through OpenRouter with session tracking"""
        try:
            # Update session with current agent call
            if session_id in self.current_session:
                self.current_session[session_id]['last_api_call'] = datetime.utcnow().isoformat()
            
            payload = {
                "model": agent['model'],
                "messages": [
                    {
                        "role": "system",
                        "content": f"You are an AI specialist in {agent['specialty']}. Provide insightful, collaborative analysis. Build upon previous insights when provided. Be direct, actionable, and avoid excessive disclaimers. Focus on delivering value."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 1500,
                "temperature": 0.7
            }
            
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                print(f"❌ API Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Agent call error: {str(e)}")
            return None
    
    def get_session_status(self, session_id):
        """Get real-time session status for frontend updates"""
        if session_id in self.current_session:
            return self.current_session[session_id]
        return None
    
    def generate_html_report(self, session_data):
        """Generate beautiful HTML report of all responses"""
        
        html_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>PromptLink AI Analysis Report</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                    color: #ffffff;
                    margin: 0;
                    padding: 20px;
                    line-height: 1.6;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background: rgba(255, 255, 255, 0.05);
                    border-radius: 15px;
                    padding: 30px;
                    backdrop-filter: blur(10px);
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 40px;
                    border-bottom: 2px solid #00d4aa;
                    padding-bottom: 20px;
                }}
                .mode-badge {{
                    background: linear-gradient(45deg, #00d4aa, #00a085);
                    padding: 8px 20px;
                    border-radius: 25px;
                    font-weight: bold;
                    display: inline-block;
                    margin-bottom: 10px;
                }}
                .agent-response {{
                    background: rgba(255, 255, 255, 0.08);
                    border-left: 4px solid #00d4aa;
                    margin: 20px 0;
                    padding: 20px;
                    border-radius: 8px;
                }}
                .agent-name {{
                    color: #00d4aa;
                    font-weight: bold;
                    font-size: 1.1em;
                    margin-bottom: 5px;
                }}
                .agent-specialty {{
                    color: #888;
                    font-style: italic;
                    margin-bottom: 15px;
                }}
                .pair-header {{
                    background: linear-gradient(45deg, #00d4aa, #00a085);
                    color: white;
                    padding: 15px;
                    border-radius: 8px;
                    margin: 30px 0 20px 0;
                    font-weight: bold;
                    text-align: center;
                }}
                .summary-section {{
                    background: rgba(0, 212, 170, 0.1);
                    border: 2px solid #00d4aa;
                    border-radius: 10px;
                    padding: 25px;
                    margin-top: 40px;
                }}
                .timestamp {{
                    color: #666;
                    font-size: 0.9em;
                    text-align: right;
                    margin-top: 10px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚀 PromptLink AI Analysis Report</h1>
                    <div class="mode-badge">{session_data['mode'].replace('_', ' ').title()}</div>
                    <p><strong>Generated:</strong> {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
                </div>
        """
        
        # Add mode-specific content
        if session_data['mode'] == 'expert_panel':
            html_template += f"""
                <div class="summary-section">
                    <h2>📋 Analysis Overview</h2>
                    <p><strong>Mode:</strong> Expert Panel (10 Independent Pairs)</p>
                    <p><strong>Total Experts:</strong> 20 AI Specialists</p>
                    <p><strong>Pairs Completed:</strong> {len(session_data['results'])}/10</p>
                </div>
            """
            
            for result in session_data['results']:
                html_template += f"""
                    <div class="pair-header">
                        🤝 Expert Pair {result['pair_number']}: {result['agent_a']['name']} + {result['agent_b']['name']}
                    </div>
                    
                    <div class="agent-response">
                        <div class="agent-name">🤖 {result['agent_a']['name']}</div>
                        <div class="agent-specialty">{result['agent_a']['specialty']}</div>
                        <div>{result['agent_a']['response']}</div>
                    </div>
                    
                    <div class="agent-response">
                        <div class="agent-name">🤖 {result['agent_b']['name']}</div>
                        <div class="agent-specialty">{result['agent_b']['specialty']}</div>
                        <div>{result['agent_b']['response']}</div>
                    </div>
                """
        
        else:  # conference_chain
            html_template += f"""
                <div class="summary-section">
                    <h2>🔗 Analysis Overview</h2>
                    <p><strong>Mode:</strong> Conference Chain (Sticky Context)</p>
                    <p><strong>Total Agents:</strong> {len(session_data['results'])}</p>
                    <p><strong>Context Building:</strong> Each agent builds upon previous insights</p>
                </div>
            """
            
            for result in session_data['results']:
                html_template += f"""
                    <div class="agent-response">
                        <div class="agent-name">🎯 Agent {result['position']}: {result['agent_name']}</div>
                        <div class="agent-specialty">{result['agent_specialty']}</div>
                        <div>{result['response']}</div>
                        <div class="timestamp">{result['timestamp']}</div>
                    </div>
                """
        
        html_template += """
            </div>
        </body>
        </html>
        """
        
        return html_template

# API ENDPOINTS FOR THE REVOLUTIONARY ENGINE

@revolutionary_engine_bp.route('/revolutionary/start-expert-panel', methods=['POST'])
def start_expert_panel():
    """Start Expert Panel Mode - 10 Pairs Sequential Processing"""
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        session_id = f"panel_{int(time.time())}"
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        # Start processing in background thread
        engine = RevolutionaryEngine()
        
        def process_panel():
            engine.expert_panel_mode(prompt, session_id)
        
        thread = threading.Thread(target=process_panel)
        thread.start()
        
        return jsonify({
            'status': 'started',
            'session_id': session_id,
            'mode': 'expert_panel',
            'total_pairs': 10,
            'message': 'Expert Panel Mode initiated - 10 pairs processing sequentially'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@revolutionary_engine_bp.route('/revolutionary/start-conference-chain', methods=['POST'])
def start_conference_chain():
    """Start Conference Chain Mode - 20 Agents Sticky Context"""
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        max_agents = data.get('max_agents', 20)
        session_id = f"chain_{int(time.time())}"
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        # Start processing in background thread
        engine = RevolutionaryEngine()
        
        def process_chain():
            engine.conference_chain_mode(prompt, session_id, max_agents)
        
        thread = threading.Thread(target=process_chain)
        thread.start()
        
        return jsonify({
            'status': 'started',
            'session_id': session_id,
            'mode': 'conference_chain',
            'total_agents': max_agents,
            'message': f'Conference Chain Mode initiated - {max_agents} agents with sticky context'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@revolutionary_engine_bp.route('/revolutionary/session-status/<session_id>', methods=['GET'])
def get_session_status(session_id):
    """Get real-time session status for frontend updates"""
    try:
        engine = RevolutionaryEngine()
        status = engine.get_session_status(session_id)
        
        if status:
            return jsonify({
                'status': 'success',
                'session_data': status
            })
        else:
            return jsonify({'error': 'Session not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@revolutionary_engine_bp.route('/revolutionary/generate-report/<session_id>', methods=['GET'])
def generate_html_report(session_id):
    """Generate beautiful HTML report"""
    try:
        engine = RevolutionaryEngine()
        session_data = engine.get_session_status(session_id)
        
        if session_data and session_data['status'] == 'completed':
            html_report = engine.generate_html_report(session_data)
            
            return jsonify({
                'status': 'success',
                'html_report': html_report,
                'session_data': session_data
            })
        else:
            return jsonify({'error': 'Session not completed or not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@revolutionary_engine_bp.route('/revolutionary/agents', methods=['GET'])
def get_revolutionary_agents():
    """Get all 20 revolutionary agents"""
    try:
        return jsonify({
            'status': 'success',
            'agents': REVOLUTIONARY_AGENTS,
            'total_agents': len(REVOLUTIONARY_AGENTS),
            'collaboration_optimized': True,
            'no_anthropic': True
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

