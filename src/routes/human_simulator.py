from flask import Blueprint, request, jsonify
from src.models.human_simulator import (
    db, UserClone, BehavioralPattern, ConversationStyle, 
    DecisionPattern, PhraseLibrary, SessionLearning, CloneAccess
)
import json
import random
from datetime import datetime
from collections import Counter
import re

human_simulator_bp = Blueprint('human_simulator', __name__)

class CloneLearningEngine:
    """Core learning engine for Human Simulator clones"""
    
    def __init__(self, clone_id):
        self.clone_id = clone_id
        self.clone = UserClone.query.get(clone_id)
        
    def analyze_user_input(self, user_message, context):
        """Analyze user input to learn patterns"""
        patterns = {
            'communication_style': self._analyze_communication_style(user_message),
            'decision_preference': self._analyze_decision_preference(user_message, context),
            'topic_interest': self._extract_topic_interests(user_message),
            'agent_preference': self._analyze_agent_preference(context)
        }
        
        self._store_learning_data(patterns, context)
        return patterns
    
    def _analyze_communication_style(self, message):
        """Analyze communication patterns"""
        style_indicators = {
            'formality': len(re.findall(r'\b(please|thank you|kindly|would you)\b', message.lower())) / max(len(message.split()), 1),
            'directness': len(re.findall(r'\b(just|simply|exactly|specifically)\b', message.lower())) / max(len(message.split()), 1),
            'enthusiasm': len(re.findall(r'[!]{1,3}|awesome|great|excellent', message.lower())) / max(len(message.split()), 1),
            'questioning': message.count('?') / max(len(message.split()), 1)
        }
        return style_indicators
    
    def _analyze_decision_preference(self, message, context):
        """Learn decision-making patterns"""
        decisions = {
            'prefers_quick_decisions': 'quick' in message.lower() or 'fast' in message.lower(),
            'wants_multiple_options': 'options' in message.lower() or 'alternatives' in message.lower(),
            'detail_oriented': len(message.split()) > 50,
            'action_focused': any(word in message.lower() for word in ['do', 'implement', 'execute', 'build'])
        }
        return decisions
    
    def _extract_topic_interests(self, message):
        """Extract topic preferences"""
        business_keywords = ['business', 'strategy', 'marketing', 'revenue', 'profit', 'customer']
        tech_keywords = ['technology', 'AI', 'software', 'development', 'code', 'system']
        creative_keywords = ['creative', 'design', 'innovative', 'brainstorm', 'idea']
        
        topics = {
            'business_interest': sum(1 for word in business_keywords if word in message.lower()),
            'tech_interest': sum(1 for word in tech_keywords if word in message.lower()),
            'creative_interest': sum(1 for word in creative_keywords if word in message.lower())
        }
        return topics
    
    def _analyze_agent_preference(self, context):
        """Learn which agents user prefers for different contexts"""
        if 'selected_agents' in context:
            return {
                'primary_agent': context.get('agent_a'),
                'secondary_agent': context.get('agent_b'),
                'context_type': context.get('conversation_type', 'general')
            }
        return {}
    
    def _store_learning_data(self, patterns, context):
        """Store learned patterns in database"""
        try:
            # Store behavioral patterns
            for pattern_type, pattern_data in patterns.items():
                existing_pattern = BehavioralPattern.query.filter_by(
                    clone_id=self.clone_id,
                    pattern_type=pattern_type
                ).first()
                
                if existing_pattern:
                    # Update existing pattern
                    existing_data = json.loads(existing_pattern.pattern_data)
                    # Merge new data with existing (simple averaging for now)
                    for key, value in pattern_data.items():
                        if key in existing_data:
                            existing_data[key] = (existing_data[key] + value) / 2
                        else:
                            existing_data[key] = value
                    
                    existing_pattern.pattern_data = json.dumps(existing_data)
                    existing_pattern.usage_count += 1
                    existing_pattern.last_used = datetime.utcnow()
                else:
                    # Create new pattern
                    new_pattern = BehavioralPattern(
                        clone_id=self.clone_id,
                        pattern_type=pattern_type,
                        pattern_data=json.dumps(pattern_data),
                        confidence_score=0.1  # Start low, will increase with usage
                    )
                    db.session.add(new_pattern)
            
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error storing learning data: {e}")
    
    def generate_response_strategy(self, topic, context):
        """Generate intelligent response strategy based on learned patterns"""
        patterns = self._get_learned_patterns()
        
        strategy = {
            'selected_agents': self._choose_optimal_agents(topic, patterns),
            'conversation_style': self._determine_conversation_style(patterns),
            'estimated_rounds': self._estimate_optimal_rounds(topic, patterns),
            'strategy_mode': self._select_strategy_mode(topic, patterns)
        }
        
        return strategy
    
    def _get_learned_patterns(self):
        """Retrieve all learned patterns for this clone"""
        patterns = {}
        behavioral_patterns = BehavioralPattern.query.filter_by(clone_id=self.clone_id).all()
        
        for pattern in behavioral_patterns:
            patterns[pattern.pattern_type] = {
                'data': json.loads(pattern.pattern_data),
                'confidence': pattern.confidence_score,
                'usage_count': pattern.usage_count
            }
        
        return patterns
    
    def _choose_optimal_agents(self, topic, patterns):
        """Choose best agents based on learned preferences"""
        # Default agent preferences
        agent_scores = {
            'gpt-4o': 0.8,
            'deepseek-r1': 0.7,
            'claude-3-sonnet': 0.6,
            'gemini-pro': 0.5,
            'perplexity-pro': 0.4
        }
        
        # Adjust based on learned patterns
        if 'agent_preference' in patterns:
            pref_data = patterns['agent_preference']['data']
            for agent, score in agent_scores.items():
                if agent in pref_data:
                    agent_scores[agent] += 0.3
        
        # Sort by score and return top 2
        sorted_agents = sorted(agent_scores.items(), key=lambda x: x[1], reverse=True)
        return [agent[0] for agent in sorted_agents[:2]]
    
    def _determine_conversation_style(self, patterns):
        """Determine conversation style based on learned patterns"""
        if 'communication_style' in patterns:
            style_data = patterns['communication_style']['data']
            
            if style_data.get('directness', 0) > 0.3:
                return 'direct_and_focused'
            elif style_data.get('enthusiasm', 0) > 0.2:
                return 'energetic_and_creative'
            elif style_data.get('formality', 0) > 0.3:
                return 'professional_and_structured'
        
        return 'balanced_and_adaptive'
    
    def _estimate_optimal_rounds(self, topic, patterns):
        """Estimate optimal number of rounds based on learned preferences"""
        base_rounds = 10
        
        if 'decision_preference' in patterns:
            decision_data = patterns['decision_preference']['data']
            
            if decision_data.get('detail_oriented', False):
                base_rounds += 5
            if decision_data.get('prefers_quick_decisions', False):
                base_rounds -= 3
        
        return max(5, min(25, base_rounds))
    
    def _select_strategy_mode(self, topic, patterns):
        """Select strategy mode based on learned patterns"""
        if 'topic_interest' in patterns:
            topic_data = patterns['topic_interest']['data']
            
            if topic_data.get('business_interest', 0) > topic_data.get('creative_interest', 0):
                return 'focused_analysis'
            elif topic_data.get('creative_interest', 0) > 0:
                return 'creative_exploration'
        
        return 'balanced_orchestration'

@human_simulator_bp.route('/human-simulator/start', methods=['POST'])
def start_human_simulator():
    """Start Human Simulator session with learning"""
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'demo_user')
        topic = data.get('topic', '')
        instructions = data.get('instructions', '')
        
        # Get or create user clone
        clone = UserClone.query.filter_by(user_id=user_id).first()
        if not clone:
            clone = UserClone(
                user_id=user_id,
                clone_name=f"{user_id}_clone",
                is_premium_clone=(user_id == 'master_user')  # Your clone
            )
            db.session.add(clone)
            db.session.commit()
        
        # Initialize learning engine
        learning_engine = CloneLearningEngine(clone.id)
        
        # Analyze the input to learn patterns
        context = {
            'conversation_type': data.get('conversation_type', 'general'),
            'agent_a': data.get('agent_a'),
            'agent_b': data.get('agent_b')
        }
        
        learning_engine.analyze_user_input(topic + ' ' + instructions, context)
        
        # Generate intelligent strategy
        strategy = learning_engine.generate_response_strategy(topic, context)
        
        # Update clone statistics
        clone.total_sessions += 1
        clone.learning_confidence = min(1.0, clone.learning_confidence + 0.01)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'session_id': f"session_{clone.id}_{datetime.utcnow().timestamp()}",
            'strategy': strategy,
            'clone_confidence': clone.learning_confidence,
            'message': f"Human Simulator started with {clone.learning_confidence:.1%} confidence"
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@human_simulator_bp.route('/human-simulator/learn', methods=['POST'])
def record_learning():
    """Record learning data from user interactions"""
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'demo_user')
        
        clone = UserClone.query.filter_by(user_id=user_id).first()
        if not clone:
            return jsonify({'error': 'Clone not found'}), 404
        
        # Record session learning
        session_learning = SessionLearning(
            clone_id=clone.id,
            session_id=data.get('session_id'),
            topic=data.get('topic'),
            agents_used=json.dumps(data.get('agents_used', [])),
            strategies_used=json.dumps(data.get('strategies_used', [])),
            total_rounds=data.get('total_rounds', 0),
            user_interventions=data.get('user_interventions', 0),
            session_success_rating=data.get('success_rating', 0.5),
            conversation_data=json.dumps(data.get('conversation_data', {}))
        )
        
        db.session.add(session_learning)
        
        # Update clone statistics
        clone.total_interactions += 1
        clone.learning_confidence = min(1.0, clone.learning_confidence + 0.005)
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'learning_recorded': True,
            'clone_confidence': clone.learning_confidence
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@human_simulator_bp.route('/human-simulator/clone-status/<user_id>', methods=['GET'])
def get_clone_status(user_id):
    """Get clone learning status and statistics"""
    try:
        clone = UserClone.query.filter_by(user_id=user_id).first()
        if not clone:
            return jsonify({'error': 'Clone not found'}), 404
        
        # Get learning statistics
        patterns_count = BehavioralPattern.query.filter_by(clone_id=clone.id).count()
        phrases_count = PhraseLibrary.query.filter_by(clone_id=clone.id).count()
        
        return jsonify({
            'clone_name': clone.clone_name,
            'learning_confidence': clone.learning_confidence,
            'total_sessions': clone.total_sessions,
            'total_interactions': clone.total_interactions,
            'patterns_learned': patterns_count,
            'phrases_stored': phrases_count,
            'is_premium_clone': clone.is_premium_clone,
            'created_at': clone.created_at.isoformat(),
            'last_updated': clone.updated_at.isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@human_simulator_bp.route('/human-simulator/add-phrase', methods=['POST'])
def add_characteristic_phrase():
    """Add a characteristic phrase to the clone's library"""
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'demo_user')
        
        clone = UserClone.query.filter_by(user_id=user_id).first()
        if not clone:
            return jsonify({'error': 'Clone not found'}), 404
        
        phrase = PhraseLibrary(
            clone_id=clone.id,
            phrase_text=data.get('phrase_text'),
            phrase_type=data.get('phrase_type', 'general'),
            context_tags=json.dumps(data.get('context_tags', []))
        )
        
        db.session.add(phrase)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'phrase_added': True,
            'phrase_id': phrase.id
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

