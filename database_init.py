from flask import Flask
from src.models.human_simulator import db, UserClone, PhraseLibrary
import json

def init_database(app):
    """Initialize database with tables and seed data"""
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if master clone exists
        master_clone = UserClone.query.filter_by(user_id='master_user').first()
        
        if not master_clone:
            # Create your master clone
            master_clone = UserClone(
                user_id='master_user',
                clone_name='Master Clone',
                is_premium_clone=True,
                learning_confidence=0.3  # Start with some base confidence
            )
            db.session.add(master_clone)
            db.session.commit()
            
            # Add your characteristic phrases
            characteristic_phrases = [
                {
                    'phrase_text': "You're the AI, not me - you figure it out",
                    'phrase_type': 'redirect',
                    'context_tags': ['when_ai_asks_for_guidance', 'decision_making']
                },
                {
                    'phrase_text': "Let's make this happen",
                    'phrase_type': 'encouragement',
                    'context_tags': ['project_start', 'motivation']
                },
                {
                    'phrase_text': "No more false promises",
                    'phrase_type': 'accountability',
                    'context_tags': ['quality_control', 'expectations']
                },
                {
                    'phrase_text': "Just deliver what works",
                    'phrase_type': 'directive',
                    'context_tags': ['implementation', 'results_focused']
                },
                {
                    'phrase_text': "Is this within your capability?",
                    'phrase_type': 'clarification',
                    'context_tags': ['capability_check', 'planning']
                },
                {
                    'phrase_text': "What do you need from me exactly?",
                    'phrase_type': 'clarification',
                    'context_tags': ['requirements_gathering', 'next_steps']
                },
                {
                    'phrase_text': "Stop the marketing fiction",
                    'phrase_type': 'correction',
                    'context_tags': ['quality_control', 'honesty']
                },
                {
                    'phrase_text': "Make it work or tell me why it won't",
                    'phrase_type': 'directive',
                    'context_tags': ['problem_solving', 'honesty']
                }
            ]
            
            for phrase_data in characteristic_phrases:
                phrase = PhraseLibrary(
                    clone_id=master_clone.id,
                    phrase_text=phrase_data['phrase_text'],
                    phrase_type=phrase_data['phrase_type'],
                    context_tags=json.dumps(phrase_data['context_tags'])
                )
                db.session.add(phrase)
            
            db.session.commit()
            print("Master clone initialized with characteristic phrases")
        
        print("Database initialized successfully")

if __name__ == '__main__':
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///human_simulator.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    init_database(app)

