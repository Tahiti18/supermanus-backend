from flask import Blueprint, request, jsonify
import requests
import json
import os
from datetime import datetime

summary_engine_bp = Blueprint('summary_engine', __name__)

class IntelligentSummaryEngine:
    """Revolutionary AI Summary and Synthesis System"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENROUTER_API_KEY', '')
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://thepromptlink.com",
            "X-Title": "PromptLink Summary Engine"
        }
        
        # SPECIALIZED SUMMARY AGENTS (NO ANTHROPIC)
        self.summary_agents = {
            'executive_summary': {
                'name': 'GPT-4o',
                'model': 'openai/gpt-4o',
                'specialty': 'Executive summarization and strategic insights'
            },
            'technical_synthesis': {
                'name': 'DeepSeek R1',
                'model': 'deepseek/deepseek-r1',
                'specialty': 'Technical analysis and deep reasoning synthesis'
            },
            'creative_synthesis': {
                'name': 'Gemini Pro 1.5',
                'model': 'google/gemini-pro-1.5',
                'specialty': 'Creative synthesis and innovative connections'
            },
            'business_synthesis': {
                'name': 'Command R+',
                'model': 'cohere/command-r-plus',
                'specialty': 'Business analysis and actionable recommendations'
            }
        }
    
    def generate_executive_summary(self, session_data):
        """Generate comprehensive executive summary"""
        
        # Compile all responses
        all_responses = self._compile_all_responses(session_data)
        
        summary_prompt = f"""
ORIGINAL PROMPT: {session_data.get('original_prompt', 'N/A')}

ANALYSIS MODE: {session_data['mode'].replace('_', ' ').title()}

ALL AI EXPERT RESPONSES:
{all_responses}

EXECUTIVE SUMMARY REQUIREMENTS:
Create a comprehensive executive summary that includes:

1. KEY INSIGHTS SYNTHESIS
   - Most important findings across all experts
   - Common themes and patterns identified
   - Contradictions or differing viewpoints

2. STRATEGIC RECOMMENDATIONS
   - Top 3-5 actionable recommendations
   - Priority ranking with rationale
   - Implementation considerations

3. EXPERT CONSENSUS ANALYSIS
   - Areas of strong agreement
   - Points of divergence and why
   - Confidence levels in recommendations

4. NEXT STEPS
   - Immediate actions to take
   - Further analysis needed
   - Success metrics to track

Format as a professional executive summary suitable for decision-makers.
Be concise but comprehensive. Focus on actionable insights.
"""
        
        agent = self.summary_agents['executive_summary']
        summary = self._call_summary_agent(agent, summary_prompt)
        
        return {
            'type': 'executive_summary',
            'summary': summary,
            'agent_used': agent['name'],
            'total_responses_analyzed': self._count_responses(session_data),
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def generate_technical_synthesis(self, session_data):
        """Generate technical deep-dive synthesis"""
        
        all_responses = self._compile_all_responses(session_data)
        
        technical_prompt = f"""
ORIGINAL PROMPT: {session_data.get('original_prompt', 'N/A')}

ALL EXPERT RESPONSES:
{all_responses}

TECHNICAL SYNTHESIS REQUIREMENTS:
Provide a deep technical analysis that includes:

1. METHODOLOGY ANALYSIS
   - Approaches suggested by different experts
   - Technical feasibility assessment
   - Resource requirements and constraints

2. IMPLEMENTATION ROADMAP
   - Step-by-step technical implementation
   - Dependencies and prerequisites
   - Risk mitigation strategies

3. TECHNICAL TRADE-OFFS
   - Pros and cons of different approaches
   - Performance vs complexity considerations
   - Scalability implications

4. EXPERT TECHNICAL CONSENSUS
   - Technical solutions with highest expert agreement
   - Areas requiring further technical investigation
   - Alternative technical approaches to consider

Focus on technical depth, implementation details, and engineering considerations.
"""
        
        agent = self.summary_agents['technical_synthesis']
        synthesis = self._call_summary_agent(agent, technical_prompt)
        
        return {
            'type': 'technical_synthesis',
            'synthesis': synthesis,
            'agent_used': agent['name'],
            'total_responses_analyzed': self._count_responses(session_data),
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def generate_creative_synthesis(self, session_data):
        """Generate creative connections and innovative insights"""
        
        all_responses = self._compile_all_responses(session_data)
        
        creative_prompt = f"""
ORIGINAL PROMPT: {session_data.get('original_prompt', 'N/A')}

ALL EXPERT RESPONSES:
{all_responses}

CREATIVE SYNTHESIS REQUIREMENTS:
Generate innovative insights by identifying:

1. UNEXPECTED CONNECTIONS
   - Novel relationships between expert insights
   - Cross-domain applications and analogies
   - Innovative combinations of ideas

2. CREATIVE OPPORTUNITIES
   - Unexplored possibilities mentioned by experts
   - Creative solutions that bridge different approaches
   - Innovative applications of suggested concepts

3. FUTURE POSSIBILITIES
   - Long-term implications of expert recommendations
   - Emerging trends and opportunities
   - Disruptive potential of suggested approaches

4. CREATIVE SYNTHESIS
   - Unique insights that emerge from combining expert perspectives
   - Creative frameworks that unify different viewpoints
   - Innovative next steps not explicitly mentioned

Focus on creativity, innovation, and discovering new possibilities.
"""
        
        agent = self.summary_agents['creative_synthesis']
        synthesis = self._call_summary_agent(agent, creative_prompt)
        
        return {
            'type': 'creative_synthesis',
            'synthesis': synthesis,
            'agent_used': agent['name'],
            'total_responses_analyzed': self._count_responses(session_data),
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def generate_business_synthesis(self, session_data):
        """Generate business-focused analysis and recommendations"""
        
        all_responses = self._compile_all_responses(session_data)
        
        business_prompt = f"""
ORIGINAL PROMPT: {session_data.get('original_prompt', 'N/A')}

ALL EXPERT RESPONSES:
{all_responses}

BUSINESS SYNTHESIS REQUIREMENTS:
Provide business-focused analysis including:

1. BUSINESS IMPACT ANALYSIS
   - Revenue implications of expert recommendations
   - Cost-benefit analysis of suggested approaches
   - Market opportunity assessment

2. COMPETITIVE ADVANTAGE
   - How recommendations create competitive differentiation
   - Market positioning implications
   - Barriers to entry for competitors

3. IMPLEMENTATION BUSINESS CASE
   - ROI projections for recommended actions
   - Resource allocation requirements
   - Timeline and milestone considerations

4. RISK ASSESSMENT
   - Business risks of recommended approaches
   - Mitigation strategies for identified risks
   - Contingency planning considerations

5. STAKEHOLDER IMPACT
   - How recommendations affect different stakeholders
   - Change management considerations
   - Communication strategy requirements

Focus on business value, profitability, and strategic business implications.
"""
        
        agent = self.summary_agents['business_synthesis']
        synthesis = self._call_summary_agent(agent, business_prompt)
        
        return {
            'type': 'business_synthesis',
            'synthesis': synthesis,
            'agent_used': agent['name'],
            'total_responses_analyzed': self._count_responses(session_data),
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def generate_comprehensive_report(self, session_data):
        """Generate all synthesis types in one comprehensive report"""
        
        print("🔍 Generating comprehensive synthesis report...")
        
        # Generate all synthesis types
        executive = self.generate_executive_summary(session_data)
        technical = self.generate_technical_synthesis(session_data)
        creative = self.generate_creative_synthesis(session_data)
        business = self.generate_business_synthesis(session_data)
        
        return {
            'comprehensive_report': {
                'executive_summary': executive,
                'technical_synthesis': technical,
                'creative_synthesis': creative,
                'business_synthesis': business
            },
            'meta_analysis': {
                'total_responses_analyzed': self._count_responses(session_data),
                'analysis_mode': session_data['mode'],
                'synthesis_agents_used': 4,
                'report_generated': datetime.utcnow().isoformat()
            }
        }
    
    def _compile_all_responses(self, session_data):
        """Compile all responses into formatted text"""
        all_responses = ""
        
        if session_data['mode'] == 'expert_panel':
            for result in session_data.get('results', []):
                all_responses += f"\n--- EXPERT PAIR {result['pair_number']} ---\n"
                all_responses += f"EXPERT A - {result['agent_a']['name']} ({result['agent_a']['specialty']}):\n"
                all_responses += f"{result['agent_a']['response']}\n\n"
                all_responses += f"EXPERT B - {result['agent_b']['name']} ({result['agent_b']['specialty']}):\n"
                all_responses += f"{result['agent_b']['response']}\n\n"
        
        elif session_data['mode'] == 'conference_chain':
            for result in session_data.get('results', []):
                all_responses += f"\n--- AGENT {result['position']}: {result['agent_name']} ---\n"
                all_responses += f"Specialty: {result['agent_specialty']}\n"
                all_responses += f"Response: {result['response']}\n\n"
        
        return all_responses
    
    def _count_responses(self, session_data):
        """Count total number of responses"""
        if session_data['mode'] == 'expert_panel':
            return len(session_data.get('results', [])) * 2  # 2 responses per pair
        else:
            return len(session_data.get('results', []))
    
    def _call_summary_agent(self, agent, prompt):
        """Call specialized summary agent"""
        try:
            payload = {
                "model": agent['model'],
                "messages": [
                    {
                        "role": "system",
                        "content": f"You are an expert in {agent['specialty']}. Provide comprehensive, insightful analysis that synthesizes multiple expert perspectives. Be thorough, actionable, and professional."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 2000,
                "temperature": 0.3  # Lower temperature for more focused synthesis
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
                print(f"❌ Summary API Error: {response.status_code}")
                return "Summary generation failed due to API error."
                
        except Exception as e:
            print(f"❌ Summary agent error: {str(e)}")
            return "Summary generation failed due to technical error."

# API ENDPOINTS FOR SUMMARY ENGINE

@summary_engine_bp.route('/summary/executive/<session_id>', methods=['GET'])
def generate_executive_summary_endpoint(session_id):
    """Generate executive summary for session"""
    try:
        # Get session data (would integrate with revolutionary engine)
        from .revolutionary_engine import RevolutionaryEngine
        
        engine = RevolutionaryEngine()
        session_data = engine.get_session_status(session_id)
        
        if not session_data or session_data['status'] != 'completed':
            return jsonify({'error': 'Session not completed or not found'}), 404
        
        summary_engine = IntelligentSummaryEngine()
        summary = summary_engine.generate_executive_summary(session_data)
        
        return jsonify({
            'status': 'success',
            'summary': summary
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@summary_engine_bp.route('/summary/technical/<session_id>', methods=['GET'])
def generate_technical_synthesis_endpoint(session_id):
    """Generate technical synthesis for session"""
    try:
        from .revolutionary_engine import RevolutionaryEngine
        
        engine = RevolutionaryEngine()
        session_data = engine.get_session_status(session_id)
        
        if not session_data or session_data['status'] != 'completed':
            return jsonify({'error': 'Session not completed or not found'}), 404
        
        summary_engine = IntelligentSummaryEngine()
        synthesis = summary_engine.generate_technical_synthesis(session_data)
        
        return jsonify({
            'status': 'success',
            'synthesis': synthesis
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@summary_engine_bp.route('/summary/creative/<session_id>', methods=['GET'])
def generate_creative_synthesis_endpoint(session_id):
    """Generate creative synthesis for session"""
    try:
        from .revolutionary_engine import RevolutionaryEngine
        
        engine = RevolutionaryEngine()
        session_data = engine.get_session_status(session_id)
        
        if not session_data or session_data['status'] != 'completed':
            return jsonify({'error': 'Session not completed or not found'}), 404
        
        summary_engine = IntelligentSummaryEngine()
        synthesis = summary_engine.generate_creative_synthesis(session_data)
        
        return jsonify({
            'status': 'success',
            'synthesis': synthesis
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@summary_engine_bp.route('/summary/business/<session_id>', methods=['GET'])
def generate_business_synthesis_endpoint(session_id):
    """Generate business synthesis for session"""
    try:
        from .revolutionary_engine import RevolutionaryEngine
        
        engine = RevolutionaryEngine()
        session_data = engine.get_session_status(session_id)
        
        if not session_data or session_data['status'] != 'completed':
            return jsonify({'error': 'Session not completed or not found'}), 404
        
        summary_engine = IntelligentSummaryEngine()
        synthesis = summary_engine.generate_business_synthesis(session_data)
        
        return jsonify({
            'status': 'success',
            'synthesis': synthesis
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@summary_engine_bp.route('/summary/comprehensive/<session_id>', methods=['GET'])
def generate_comprehensive_report_endpoint(session_id):
    """Generate comprehensive synthesis report"""
    try:
        from .revolutionary_engine import RevolutionaryEngine
        
        engine = RevolutionaryEngine()
        session_data = engine.get_session_status(session_id)
        
        if not session_data or session_data['status'] != 'completed':
            return jsonify({'error': 'Session not completed or not found'}), 404
        
        summary_engine = IntelligentSummaryEngine()
        comprehensive_report = summary_engine.generate_comprehensive_report(session_data)
        
        return jsonify({
            'status': 'success',
            'comprehensive_report': comprehensive_report
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@summary_engine_bp.route('/summary/agents', methods=['GET'])
def get_summary_agents():
    """Get available summary agents"""
    try:
        summary_engine = IntelligentSummaryEngine()
        
        return jsonify({
            'status': 'success',
            'summary_agents': summary_engine.summary_agents,
            'total_agents': len(summary_engine.summary_agents),
            'synthesis_types': ['executive_summary', 'technical_synthesis', 'creative_synthesis', 'business_synthesis']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

