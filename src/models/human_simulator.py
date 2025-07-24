from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class UserClone(db.Model):
    """Stores user clone profiles and learning data"""
    __tablename__ = 'user_clones'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), unique=True, nullable=False)
    clone_name = db.Column(db.String(100), nullable=False)
    is_premium_clone = db.Column(db.Boolean, default=False)  # True for your clone that premium users can access
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Learning data
    total_sessions = db.Column(db.Integer, default=0)
    total_interactions = db.Column(db.Integer, default=0)
    learning_confidence = db.Column(db.Float, default=0.0)  # 0-1 scale of how well trained the clone is
    
    # Relationships
    behavioral_patterns = db.relationship('BehavioralPattern', backref='user_clone', lazy=True, cascade='all, delete-orphan')
    conversation_styles = db.relationship('ConversationStyle', backref='user_clone', lazy=True, cascade='all, delete-orphan')
    decision_patterns = db.relationship('DecisionPattern', backref='user_clone', lazy=True, cascade='all, delete-orphan')
    phrase_library = db.relationship('PhraseLibrary', backref='user_clone', lazy=True, cascade='all, delete-orphan')

class BehavioralPattern(db.Model):
    """Stores learned behavioral patterns for each clone"""
    __tablename__ = 'behavioral_patterns'
    
    id = db.Column(db.Integer, primary_key=True)
    clone_id = db.Column(db.Integer, db.ForeignKey('user_clones.id'), nullable=False)
    
    pattern_type = db.Column(db.String(50), nullable=False)  # 'agent_selection', 'conversation_flow', 'topic_preference'
    pattern_data = db.Column(db.Text, nullable=False)  # JSON data
    confidence_score = db.Column(db.Float, default=0.0)
    usage_count = db.Column(db.Integer, default=1)
    last_used = db.Column(db.DateTime, default=datetime.utcnow)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ConversationStyle(db.Model):
    """Stores conversation style preferences and patterns"""
    __tablename__ = 'conversation_styles'
    
    id = db.Column(db.Integer, primary_key=True)
    clone_id = db.Column(db.Integer, db.ForeignKey('user_clones.id'), nullable=False)
    
    topic_category = db.Column(db.String(100), nullable=False)  # 'business', 'technical', 'creative', etc.
    preferred_agents = db.Column(db.Text, nullable=False)  # JSON array of preferred agent order
    conversation_length = db.Column(db.Integer, default=10)  # Preferred number of rounds
    strategy_preference = db.Column(db.String(50), nullable=False)  # 'balanced', 'focused', etc.
    
    # Style characteristics
    formality_level = db.Column(db.Float, default=0.5)  # 0=casual, 1=formal
    detail_preference = db.Column(db.Float, default=0.5)  # 0=brief, 1=detailed
    creativity_preference = db.Column(db.Float, default=0.5)  # 0=conservative, 1=creative
    
    usage_count = db.Column(db.Integer, default=1)
    success_rate = db.Column(db.Float, default=0.0)  # How often this style leads to successful conversations
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class DecisionPattern(db.Model):
    """Stores decision-making patterns and preferences"""
    __tablename__ = 'decision_patterns'
    
    id = db.Column(db.Integer, primary_key=True)
    clone_id = db.Column(db.Integer, db.ForeignKey('user_clones.id'), nullable=False)
    
    decision_type = db.Column(db.String(50), nullable=False)  # 'agent_switch', 'strategy_change', 'conversation_end'
    context_data = db.Column(db.Text, nullable=False)  # JSON data about the context when decision was made
    decision_data = db.Column(db.Text, nullable=False)  # JSON data about the decision made
    
    outcome_rating = db.Column(db.Float, default=0.0)  # How successful was this decision (0-1)
    confidence_score = db.Column(db.Float, default=0.0)
    usage_count = db.Column(db.Integer, default=1)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PhraseLibrary(db.Model):
    """Stores the user's characteristic phrases and communication patterns"""
    __tablename__ = 'phrase_library'
    
    id = db.Column(db.Integer, primary_key=True)
    clone_id = db.Column(db.Integer, db.ForeignKey('user_clones.id'), nullable=False)
    
    phrase_text = db.Column(db.Text, nullable=False)
    phrase_type = db.Column(db.String(50), nullable=False)  # 'redirect', 'encouragement', 'clarification', 'conclusion'
    context_tags = db.Column(db.Text)  # JSON array of when to use this phrase
    
    usage_count = db.Column(db.Integer, default=0)
    effectiveness_score = db.Column(db.Float, default=0.0)  # How effective this phrase is
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_used = db.Column(db.DateTime)

class SessionLearning(db.Model):
    """Stores learning data from each session for continuous improvement"""
    __tablename__ = 'session_learning'
    
    id = db.Column(db.Integer, primary_key=True)
    clone_id = db.Column(db.Integer, db.ForeignKey('user_clones.id'), nullable=False)
    session_id = db.Column(db.String(100), nullable=False)
    
    # Session data
    topic = db.Column(db.String(200))
    agents_used = db.Column(db.Text)  # JSON array
    strategies_used = db.Column(db.Text)  # JSON array
    total_rounds = db.Column(db.Integer)
    user_interventions = db.Column(db.Integer, default=0)  # How many times user had to intervene
    
    # Learning metrics
    session_success_rating = db.Column(db.Float, default=0.0)  # User satisfaction with session
    clone_accuracy = db.Column(db.Float, default=0.0)  # How well clone matched user preferences
    new_patterns_learned = db.Column(db.Integer, default=0)
    
    # Raw session data for analysis
    conversation_data = db.Column(db.Text)  # JSON of full conversation
    user_feedback = db.Column(db.Text)  # Any explicit feedback from user
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class CloneAccess(db.Model):
    """Manages access to premium clones"""
    __tablename__ = 'clone_access'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)  # User who has access
    clone_id = db.Column(db.Integer, db.ForeignKey('user_clones.id'), nullable=False)
    
    access_type = db.Column(db.String(50), nullable=False)  # 'premium_subscription', 'enterprise_license'
    access_granted = db.Column(db.DateTime, default=datetime.utcnow)
    access_expires = db.Column(db.DateTime)
    
    usage_count = db.Column(db.Integer, default=0)
    usage_limit = db.Column(db.Integer)  # Optional usage limit
    
    is_active = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

