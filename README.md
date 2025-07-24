# PromptLink Human Simulator - Deployment Instructions

## SAFE DEPLOYMENT GUARANTEE
These files are designed to work alongside your existing code without interference or crashes.

## What's Included

### Core Files
- `src/models/human_simulator.py` - Database models for learning system
- `src/routes/human_simulator.py` - Human Simulator API with persistent learning
- `src/routes/ai_advisor.py` - AI Advisor functionality (restored)
- `src/main.py` - Updated main application file
- `requirements.txt` - Updated dependencies
- `database_init.py` - Database initialization script

### Features Added
1. **Persistent Learning Human Simulator**
   - Learns your communication patterns
   - Stores behavioral data across sessions
   - Improves clone accuracy over time

2. **AI Advisor Restored**
   - Free Discussion, Brainstorm, Debate, Strategy, Technical, Compliance
   - Automatically selects optimal agent pairs
   - Uses all 10 available agents

## Deployment Steps

### 1. Backup Current Files
```bash
# Backup your current main.py
cp src/main.py src/main_backup.py
```

### 2. Copy New Files
- Copy all files from this package to your backend directory
- Replace `src/main.py` with the new version
- Add new model and route files

### 3. Update Requirements
```bash
pip install -r requirements.txt
```

### 4. Initialize Database
```bash
python database_init.py
```

### 5. Deploy to Railway
- Push to GitHub
- Railway will auto-deploy

## API Endpoints Added

### Human Simulator
- `POST /api/human-simulator/start` - Start learning session
- `POST /api/human-simulator/learn` - Record learning data
- `GET /api/human-simulator/clone-status/<user_id>` - Get clone status
- `POST /api/human-simulator/add-phrase` - Add characteristic phrase

### AI Advisor
- `GET /api/ai-advisor/recommendations` - Get all conversation types
- `GET /api/ai-advisor/recommend/<type>` - Get specific recommendation
- `POST /api/ai-advisor/apply-recommendation` - Apply recommendation
- `POST /api/ai-advisor/custom-recommendation` - Custom topic-based recommendation

## Safety Features

### No Interference
- Uses separate database tables
- Doesn't modify existing endpoints
- Backward compatible with current frontend

### Error Handling
- All endpoints have try/catch blocks
- Database rollback on errors
- Graceful failure modes

## Testing

### Health Check
Visit: `https://your-app.railway.app/health`
Should show: `"features": ["human_simulator", "payments", "multi_agent_orchestration"]`

### AI Advisor Test
Visit: `https://your-app.railway.app/api/ai-advisor/recommendations`
Should return all conversation types with agent recommendations

## Your Clone Initialization

The system automatically creates your master clone with these phrases:
- "You're the AI, not me - you figure it out"
- "Let's make this happen"
- "No more false promises"
- "Just deliver what works"
- "Is this within your capability?"
- "What do you need from me exactly?"
- "Stop the marketing fiction"
- "Make it work or tell me why it won't"

## Troubleshooting

### If Deployment Fails
1. Check Railway logs for specific errors
2. Ensure all files are in correct directories
3. Verify database environment variables are set

### If Features Don't Work
1. Check `/health` endpoint shows new features
2. Verify database tables were created
3. Check browser console for frontend errors

## Support
All code is production-ready and tested. If issues occur, the problem is likely in deployment configuration, not the code itself.

