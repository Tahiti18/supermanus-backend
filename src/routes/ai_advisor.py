from flask import Blueprint, request, jsonify

ai_advisor_bp = Blueprint('ai_advisor', __name__)

# Available agents in your system
AVAILABLE_AGENTS = [
    'GPT-4o',
    'ChatGPT 4 Turbo', 
    'DeepSeek R1',
    'Meta Llama 3.3',
    'Mistral Large',
    'Gemini 2.0 Flash',
    'Perplexity Pro',
    'Gemini Pro 1.5',
    'Command R+',
    'Qwen 2.5 72B'
]

# AI Advisor recommendations for each conversation type
AI_ADVISOR_RECOMMENDATIONS = {
    'free_discussion': {
        'name': 'Free Discussion',
        'description': 'Open-ended conversation and exploration',
        'primary_agent': 'GPT-4o',
        'secondary_agent': 'Gemini 2.0 Flash',
        'strategy': 'balanced_orchestration',
        'rounds': 10,
        'reasoning': 'GPT-4o for comprehensive analysis, Gemini for creative perspectives'
    },
    'brainstorm': {
        'name': 'Brainstorm',
        'description': 'Creative idea generation and innovation',
        'primary_agent': 'Gemini 2.0 Flash',
        'secondary_agent': 'Command R+',
        'strategy': 'creative_exploration',
        'rounds': 12,
        'reasoning': 'Gemini for creative thinking, Command R+ for business viability'
    },
    'debate': {
        'name': 'Debate',
        'description': 'Structured argument and counterargument',
        'primary_agent': 'DeepSeek R1',
        'secondary_agent': 'GPT-4o',
        'strategy': 'focused_analysis',
        'rounds': 15,
        'reasoning': 'DeepSeek for analytical reasoning, GPT-4o for balanced perspectives'
    },
    'strategy': {
        'name': 'Strategy',
        'description': 'Business planning and strategic analysis',
        'primary_agent': 'GPT-4o',
        'secondary_agent': 'Command R+',
        'strategy': 'focused_analysis',
        'rounds': 18,
        'reasoning': 'GPT-4o for comprehensive analysis, Command R+ for business focus'
    },
    'technical': {
        'name': 'Technical',
        'description': 'Technical analysis and problem-solving',
        'primary_agent': 'DeepSeek R1',
        'secondary_agent': 'ChatGPT 4 Turbo',
        'strategy': 'deep_analysis',
        'rounds': 20,
        'reasoning': 'DeepSeek for technical depth, ChatGPT 4 Turbo for implementation'
    },
    'compliance': {
        'name': 'Compliance',
        'description': 'Regulatory and compliance analysis',
        'primary_agent': 'ChatGPT 4 Turbo',
        'secondary_agent': 'Command R+',
        'strategy': 'conservative_analysis',
        'rounds': 15,
        'reasoning': 'ChatGPT 4 Turbo for careful analysis, Command R+ for business context'
    }
}

@ai_advisor_bp.route('/ai-advisor/recommendations', methods=['GET'])
def get_all_recommendations():
    """Get all AI Advisor conversation type recommendations"""
    try:
        return jsonify({
            'status': 'success',
            'recommendations': AI_ADVISOR_RECOMMENDATIONS,
            'available_agents': AVAILABLE_AGENTS
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_advisor_bp.route('/ai-advisor/recommend/<conversation_type>', methods=['GET'])
def get_recommendation(conversation_type):
    """Get specific recommendation for conversation type"""
    try:
        if conversation_type not in AI_ADVISOR_RECOMMENDATIONS:
            return jsonify({'error': 'Invalid conversation type'}), 400
        
        recommendation = AI_ADVISOR_RECOMMENDATIONS[conversation_type]
        
        return jsonify({
            'status': 'success',
            'conversation_type': conversation_type,
            'recommendation': recommendation
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_advisor_bp.route('/ai-advisor/apply-recommendation', methods=['POST'])
def apply_recommendation():
    """Apply AI Advisor recommendation to session"""
    try:
        data = request.get_json()
        conversation_type = data.get('conversation_type')
        
        if conversation_type not in AI_ADVISOR_RECOMMENDATIONS:
            return jsonify({'error': 'Invalid conversation type'}), 400
        
        recommendation = AI_ADVISOR_RECOMMENDATIONS[conversation_type]
        
        # Return configuration for frontend to apply
        return jsonify({
            'status': 'success',
            'applied': True,
            'configuration': {
                'agent_a': recommendation['primary_agent'],
                'agent_b': recommendation['secondary_agent'],
                'strategy_mode': recommendation['strategy'],
                'recommended_rounds': recommendation['rounds'],
                'conversation_type': conversation_type,
                'reasoning': recommendation['reasoning']
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_advisor_bp.route('/ai-advisor/custom-recommendation', methods=['POST'])
def create_custom_recommendation():
    """Create custom agent recommendation based on topic"""
    try:
        data = request.get_json()
        topic = data.get('topic', '').lower()
        requirements = data.get('requirements', [])
        
        # Simple keyword-based agent selection
        agent_scores = {}
        
        # Initialize all agents with base score
        for agent in AVAILABLE_AGENTS:
            agent_scores[agent] = 0.5
        
        # Adjust scores based on topic keywords
        if any(word in topic for word in ['business', 'strategy', 'marketing', 'revenue']):
            agent_scores['GPT-4o'] += 0.3
            agent_scores['Command R+'] += 0.3
            
        if any(word in topic for word in ['technical', 'code', 'programming', 'development']):
            agent_scores['DeepSeek R1'] += 0.4
            agent_scores['ChatGPT 4 Turbo'] += 0.3
            
        if any(word in topic for word in ['creative', 'design', 'innovative', 'brainstorm']):
            agent_scores['Gemini 2.0 Flash'] += 0.4
            agent_scores['Gemini Pro 1.5'] += 0.3
            
        if any(word in topic for word in ['research', 'analysis', 'data', 'information']):
            agent_scores['Perplexity Pro'] += 0.4
            agent_scores['DeepSeek R1'] += 0.3
            
        if any(word in topic for word in ['multilingual', 'international', 'global']):
            agent_scores['Qwen 2.5 72B'] += 0.4
            
        # Sort agents by score
        sorted_agents = sorted(agent_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Select top 2 agents
        primary_agent = sorted_agents[0][0]
        secondary_agent = sorted_agents[1][0]
        
        # Determine strategy based on topic
        if any(word in topic for word in ['quick', 'fast', 'urgent']):
            strategy = 'aggressive_exploration'
            rounds = 8
        elif any(word in topic for word in ['detailed', 'comprehensive', 'thorough']):
            strategy = 'deep_analysis'
            rounds = 20
        elif any(word in topic for word in ['creative', 'innovative', 'brainstorm']):
            strategy = 'creative_synthesis'
            rounds = 12
        else:
            strategy = 'balanced_orchestration'
            rounds = 10
        
        return jsonify({
            'status': 'success',
            'custom_recommendation': {
                'primary_agent': primary_agent,
                'secondary_agent': secondary_agent,
                'strategy': strategy,
                'recommended_rounds': rounds,
                'reasoning': f"Selected {primary_agent} and {secondary_agent} based on topic analysis",
                'confidence': sorted_agents[0][1]
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

