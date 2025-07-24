import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db as user_db
from src.models.human_simulator import db as hs_db
from src.routes.user import user_bp
from src.routes.agents import agents_bp
from src.routes.chat import chat_bp
from src.routes.workflows import workflows_bp
from src.routes.relay import relay_bp
from src.routes.payments import payments_bp
from src.routes.human_simulator import human_simulator_bp
from src.routes.ai_advisor import ai_advisor_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'promptlink-orchestration-engine-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enable CORS for frontend integration
CORS(app, origins=[
    'http://localhost:3000',
    'https://lucky-kheer-f8d0d3.netlify.app',
    'https://thepromptlink.com',
    'https://thepromptlink.netlify.app'
])

# Initialize databases
user_db.init_app(app)
hs_db.init_app(app)

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(agents_bp, url_prefix='/api')
app.register_blueprint(chat_bp, url_prefix='/api')
app.register_blueprint(workflows_bp, url_prefix='/api')
app.register_blueprint(relay_bp, url_prefix='/api')
app.register_blueprint(payments_bp, url_prefix='/api')
app.register_blueprint(human_simulator_bp, url_prefix='/api')
app.register_blueprint(ai_advisor_bp, url_prefix='/api')

# Database initialization
with app.app_context():
    user_db.create_all()
    hs_db.create_all()

@app.route('/health')
def health_check():
    """Health check endpoint for deployment monitoring"""
    return {
        'status': 'healthy',
        'service': 'PromptLink Orchestration Engine',
        'version': '1.0.0',
        'features': ['human_simulator', 'payments', 'multi_agent_orchestration']
    }

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    """Serve frontend files"""
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return {
                'message': 'PromptLink Orchestration Engine API',
                'version': '1.0.0',
                'endpoints': [
                    '/api/agents',
                    '/api/chat',
                    '/api/workflows',
                    '/api/relay',
                    '/api/payments',
                    '/api/human-simulator',
                    '/health'
                ]
            }

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)

