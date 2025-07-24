// REVOLUTIONARY AI RELAY - DYNAMIC FRONTEND INTERFACE
// Integrates with existing PromptLink design while adding 20-agent power

class RevolutionaryInterface {
    constructor() {
        this.currentSession = null;
        this.currentMode = null;
        this.statusPollingInterval = null;
        this.backendUrl = 'https://web-production-2816f.up.railway.app'; // Your Railway backend
        
        // Initialize interface
        this.initializeInterface();
    }
    
    initializeInterface() {
        console.log('🚀 Revolutionary AI Relay Interface Initialized');
        
        // Add revolutionary mode buttons to existing interface
        this.addRevolutionaryModeButtons();
        
        // Enhance existing agent boxes for dynamic updates
        this.enhanceAgentBoxes();
        
        // Add summary and report generation buttons
        this.addSummaryControls();
    }
    
    addRevolutionaryModeButtons() {
        // Find the existing Human Simulator section
        const humanSimulatorSection = document.querySelector('.human-simulator-section');
        
        if (humanSimulatorSection) {
            // Add revolutionary mode selector
            const revolutionaryModes = document.createElement('div');
            revolutionaryModes.className = 'revolutionary-modes';
            revolutionaryModes.innerHTML = `
                <div class="mode-selector">
                    <h3>🚀 Revolutionary AI Modes</h3>
                    <div class="mode-buttons">
                        <button class="mode-btn expert-panel-btn" onclick="revolutionaryInterface.startExpertPanel()">
                            🏛️ Expert Panel Mode
                            <span class="mode-desc">10 Independent Expert Pairs</span>
                        </button>
                        <button class="mode-btn conference-chain-btn" onclick="revolutionaryInterface.startConferenceChain()">
                            🔗 Conference Chain Mode
                            <span class="mode-desc">20 Agents with Sticky Context</span>
                        </button>
                    </div>
                </div>
            `;
            
            // Insert after human simulator controls
            humanSimulatorSection.appendChild(revolutionaryModes);
        }
    }
    
    enhanceAgentBoxes() {
        // Get existing agent boxes
        const agentBoxA = document.querySelector('[data-agent="A"]');
        const agentBoxB = document.querySelector('[data-agent="B"]');
        
        if (agentBoxA && agentBoxB) {
            // Add dynamic status indicators
            this.addStatusIndicators(agentBoxA, 'A');
            this.addStatusIndicators(agentBoxB, 'B');
            
            // Add progress tracking
            this.addProgressTracking();
        }
    }
    
    addStatusIndicators(agentBox, agentId) {
        // Add revolutionary status indicator
        const statusIndicator = document.createElement('div');
        statusIndicator.className = 'revolutionary-status';
        statusIndicator.id = `revolutionary-status-${agentId}`;
        statusIndicator.innerHTML = `
            <div class="status-badge">Ready</div>
            <div class="agent-info">
                <span class="current-agent">Select Mode</span>
                <span class="agent-specialty">Choose Revolutionary Mode</span>
            </div>
        `;
        
        // Insert at top of agent box
        agentBox.insertBefore(statusIndicator, agentBox.firstChild);
    }
    
    addProgressTracking() {
        // Add progress tracking section
        const progressSection = document.createElement('div');
        progressSection.className = 'revolutionary-progress';
        progressSection.id = 'revolutionary-progress';
        progressSection.innerHTML = `
            <div class="progress-header">
                <h4>🎯 Revolutionary Processing Status</h4>
                <div class="progress-controls">
                    <button class="btn-secondary" onclick="revolutionaryInterface.pauseProcessing()">Pause</button>
                    <button class="btn-danger" onclick="revolutionaryInterface.stopProcessing()">Stop</button>
                </div>
            </div>
            <div class="progress-bar-container">
                <div class="progress-bar" id="revolutionary-progress-bar">
                    <div class="progress-fill"></div>
                </div>
                <div class="progress-text">
                    <span id="progress-current">0</span> / <span id="progress-total">0</span> Agents
                </div>
            </div>
            <div class="current-processing">
                <div class="processing-info">
                    <span class="processing-label">Current:</span>
                    <span id="current-processing-agent">Ready to start</span>
                </div>
                <div class="estimated-time">
                    <span class="time-label">Est. Time:</span>
                    <span id="estimated-completion">--:--</span>
                </div>
            </div>
        `;
        
        // Insert before conversation area
        const conversationArea = document.querySelector('.conversation-area');
        if (conversationArea) {
            conversationArea.parentNode.insertBefore(progressSection, conversationArea);
        }
        
        // Initially hide progress section
        progressSection.style.display = 'none';
    }
    
    addSummaryControls() {
        // Add summary generation controls
        const summaryControls = document.createElement('div');
        summaryControls.className = 'summary-controls';
        summaryControls.id = 'summary-controls';
        summaryControls.innerHTML = `
            <div class="summary-header">
                <h4>📊 Intelligent Summary & Analysis</h4>
            </div>
            <div class="summary-buttons">
                <button class="summary-btn executive-btn" onclick="revolutionaryInterface.generateExecutiveSummary()">
                    📋 Executive Summary
                </button>
                <button class="summary-btn technical-btn" onclick="revolutionaryInterface.generateTechnicalSynthesis()">
                    🔧 Technical Synthesis
                </button>
                <button class="summary-btn creative-btn" onclick="revolutionaryInterface.generateCreativeSynthesis()">
                    💡 Creative Synthesis
                </button>
                <button class="summary-btn business-btn" onclick="revolutionaryInterface.generateBusinessSynthesis()">
                    💼 Business Analysis
                </button>
                <button class="summary-btn comprehensive-btn" onclick="revolutionaryInterface.generateComprehensiveReport()">
                    📈 Comprehensive Report
                </button>
                <button class="summary-btn html-report-btn" onclick="revolutionaryInterface.generateHtmlReport()">
                    📄 HTML Report
                </button>
            </div>
        `;
        
        // Insert after progress section
        const progressSection = document.getElementById('revolutionary-progress');
        if (progressSection) {
            progressSection.parentNode.insertAfter(summaryControls, progressSection);
        }
        
        // Initially hide summary controls
        summaryControls.style.display = 'none';
    }
    
    async startExpertPanel() {
        const prompt = this.getCurrentPrompt();
        if (!prompt) {
            this.showError('Please enter a prompt first');
            return;
        }
        
        console.log('🏛️ Starting Expert Panel Mode');
        this.currentMode = 'expert_panel';
        
        // Show progress tracking
        this.showProgressTracking('Expert Panel Mode', 10, 'pairs');
        
        // Update agent boxes
        this.updateAgentBox('A', 'Initializing...', 'Expert Panel Mode');
        this.updateAgentBox('B', 'Waiting...', 'Expert Panel Mode');
        
        try {
            const response = await fetch(`${this.backendUrl}/api/revolutionary/start-expert-panel`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    prompt: prompt
                })
            });
            
            const result = await response.json();
            
            if (result.status === 'started') {
                this.currentSession = result.session_id;
                this.startStatusPolling();
                console.log('✅ Expert Panel Mode started:', result.session_id);
            } else {
                this.showError('Failed to start Expert Panel Mode');
            }
            
        } catch (error) {
            console.error('❌ Error starting Expert Panel Mode:', error);
            this.showError('Network error starting Expert Panel Mode');
        }
    }
    
    async startConferenceChain() {
        const prompt = this.getCurrentPrompt();
        if (!prompt) {
            this.showError('Please enter a prompt first');
            return;
        }
        
        console.log('🔗 Starting Conference Chain Mode');
        this.currentMode = 'conference_chain';
        
        // Show progress tracking
        this.showProgressTracking('Conference Chain Mode', 20, 'agents');
        
        // Update agent boxes
        this.updateAgentBox('A', 'Initializing...', 'Conference Chain Mode');
        this.updateAgentBox('B', 'Waiting...', 'Conference Chain Mode');
        
        try {
            const response = await fetch(`${this.backendUrl}/api/revolutionary/start-conference-chain`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    prompt: prompt,
                    max_agents: 20
                })
            });
            
            const result = await response.json();
            
            if (result.status === 'started') {
                this.currentSession = result.session_id;
                this.startStatusPolling();
                console.log('✅ Conference Chain Mode started:', result.session_id);
            } else {
                this.showError('Failed to start Conference Chain Mode');
            }
            
        } catch (error) {
            console.error('❌ Error starting Conference Chain Mode:', error);
            this.showError('Network error starting Conference Chain Mode');
        }
    }
    
    startStatusPolling() {
        if (this.statusPollingInterval) {
            clearInterval(this.statusPollingInterval);
        }
        
        this.statusPollingInterval = setInterval(async () => {
            await this.updateSessionStatus();
        }, 2000); // Poll every 2 seconds
    }
    
    async updateSessionStatus() {
        if (!this.currentSession) return;
        
        try {
            const response = await fetch(`${this.backendUrl}/api/revolutionary/session-status/${this.currentSession}`);
            const result = await response.json();
            
            if (result.status === 'success') {
                const sessionData = result.session_data;
                this.updateInterfaceWithStatus(sessionData);
                
                if (sessionData.status === 'completed') {
                    this.onSessionCompleted(sessionData);
                }
            }
            
        } catch (error) {
            console.error('❌ Error polling session status:', error);
        }
    }
    
    updateInterfaceWithStatus(sessionData) {
        if (sessionData.mode === 'expert_panel') {
            this.updateExpertPanelStatus(sessionData);
        } else if (sessionData.mode === 'conference_chain') {
            this.updateConferenceChainStatus(sessionData);
        }
    }
    
    updateExpertPanelStatus(sessionData) {
        const currentPair = sessionData.current_pair || 0;
        const totalPairs = sessionData.total_pairs || 10;
        const currentAgents = sessionData.current_agents || ['Initializing...', 'Waiting...'];
        
        // Update progress bar
        this.updateProgressBar(currentPair, totalPairs);
        
        // Update agent boxes
        this.updateAgentBox('A', currentAgents[0], 'Expert Panel - Agent A');
        this.updateAgentBox('B', currentAgents[1], 'Expert Panel - Agent B');
        
        // Update current processing info
        document.getElementById('current-processing-agent').textContent = 
            `Pair ${currentPair}/${totalPairs}: ${currentAgents[0]} + ${currentAgents[1]}`;
    }
    
    updateConferenceChainStatus(sessionData) {
        const currentAgent = sessionData.current_agent || 0;
        const totalAgents = sessionData.total_agents || 20;
        const currentAgentName = sessionData.current_agent_name || 'Initializing...';
        
        // Update progress bar
        this.updateProgressBar(currentAgent, totalAgents);
        
        // For conference chain, show current agent in both boxes
        this.updateAgentBox('A', currentAgentName, 'Conference Chain - Current');
        this.updateAgentBox('B', 'Building Context...', 'Conference Chain - Next');
        
        // Update current processing info
        document.getElementById('current-processing-agent').textContent = 
            `Agent ${currentAgent}/${totalAgents}: ${currentAgentName}`;
    }
    
    updateProgressBar(current, total) {
        const progressFill = document.querySelector('.progress-fill');
        const progressCurrent = document.getElementById('progress-current');
        const progressTotal = document.getElementById('progress-total');
        
        if (progressFill && progressCurrent && progressTotal) {
            const percentage = (current / total) * 100;
            progressFill.style.width = `${percentage}%`;
            progressCurrent.textContent = current;
            progressTotal.textContent = total;
        }
    }
    
    updateAgentBox(agentId, agentName, specialty) {
        const statusElement = document.getElementById(`revolutionary-status-${agentId}`);
        if (statusElement) {
            const currentAgent = statusElement.querySelector('.current-agent');
            const agentSpecialty = statusElement.querySelector('.agent-specialty');
            const statusBadge = statusElement.querySelector('.status-badge');
            
            if (currentAgent) currentAgent.textContent = agentName;
            if (agentSpecialty) agentSpecialty.textContent = specialty;
            if (statusBadge) statusBadge.textContent = 'Processing';
        }
    }
    
    onSessionCompleted(sessionData) {
        console.log('✅ Revolutionary session completed!');
        
        // Stop polling
        if (this.statusPollingInterval) {
            clearInterval(this.statusPollingInterval);
            this.statusPollingInterval = null;
        }
        
        // Update interface
        this.updateAgentBox('A', 'Completed', 'Session Finished');
        this.updateAgentBox('B', 'Completed', 'Session Finished');
        
        // Show summary controls
        this.showSummaryControls();
        
        // Update status badges
        const statusBadges = document.querySelectorAll('.status-badge');
        statusBadges.forEach(badge => {
            badge.textContent = 'Completed';
            badge.style.background = '#00d4aa';
        });
        
        // Show completion notification
        this.showSuccess(`Revolutionary ${sessionData.mode.replace('_', ' ')} completed! ${sessionData.results?.length || 0} responses generated.`);
    }
    
    showProgressTracking(mode, total, unit) {
        const progressSection = document.getElementById('revolutionary-progress');
        if (progressSection) {
            progressSection.style.display = 'block';
            
            // Update labels
            const progressText = progressSection.querySelector('.progress-text');
            if (progressText) {
                progressText.innerHTML = `<span id="progress-current">0</span> / <span id="progress-total">${total}</span> ${unit}`;
            }
            
            // Reset progress bar
            const progressFill = progressSection.querySelector('.progress-fill');
            if (progressFill) {
                progressFill.style.width = '0%';
            }
        }
    }
    
    showSummaryControls() {
        const summaryControls = document.getElementById('summary-controls');
        if (summaryControls) {
            summaryControls.style.display = 'block';
        }
    }
    
    getCurrentPrompt() {
        // Get prompt from existing interface
        const promptInput = document.querySelector('textarea[placeholder*="guidance"], textarea[placeholder*="instructions"]');
        return promptInput ? promptInput.value.trim() : '';
    }
    
    showError(message) {
        console.error('❌', message);
        // You can integrate with existing notification system
        alert(`Error: ${message}`);
    }
    
    showSuccess(message) {
        console.log('✅', message);
        // You can integrate with existing notification system
        alert(`Success: ${message}`);
    }
    
    // Summary generation methods
    async generateExecutiveSummary() {
        await this.generateSummary('executive', '📋 Executive Summary');
    }
    
    async generateTechnicalSynthesis() {
        await this.generateSummary('technical', '🔧 Technical Synthesis');
    }
    
    async generateCreativeSynthesis() {
        await this.generateSummary('creative', '💡 Creative Synthesis');
    }
    
    async generateBusinessSynthesis() {
        await this.generateSummary('business', '💼 Business Analysis');
    }
    
    async generateComprehensiveReport() {
        await this.generateSummary('comprehensive', '📈 Comprehensive Report');
    }
    
    async generateSummary(type, title) {
        if (!this.currentSession) {
            this.showError('No completed session to summarize');
            return;
        }
        
        console.log(`📊 Generating ${title}...`);
        
        try {
            const response = await fetch(`${this.backendUrl}/api/summary/${type}/${this.currentSession}`);
            const result = await response.json();
            
            if (result.status === 'success') {
                this.displaySummary(title, result.summary || result.synthesis || result.comprehensive_report);
            } else {
                this.showError(`Failed to generate ${title}`);
            }
            
        } catch (error) {
            console.error(`❌ Error generating ${title}:`, error);
            this.showError(`Network error generating ${title}`);
        }
    }
    
    async generateHtmlReport() {
        if (!this.currentSession) {
            this.showError('No completed session to generate report');
            return;
        }
        
        console.log('📄 Generating HTML Report...');
        
        try {
            const response = await fetch(`${this.backendUrl}/api/revolutionary/generate-report/${this.currentSession}`);
            const result = await response.json();
            
            if (result.status === 'success') {
                // Open HTML report in new window
                const newWindow = window.open('', '_blank');
                newWindow.document.write(result.html_report);
                newWindow.document.close();
            } else {
                this.showError('Failed to generate HTML report');
            }
            
        } catch (error) {
            console.error('❌ Error generating HTML report:', error);
            this.showError('Network error generating HTML report');
        }
    }
    
    displaySummary(title, content) {
        // Create modal or dedicated area to display summary
        const modal = document.createElement('div');
        modal.className = 'summary-modal';
        modal.innerHTML = `
            <div class="summary-modal-content">
                <div class="summary-modal-header">
                    <h3>${title}</h3>
                    <button class="close-modal" onclick="this.closest('.summary-modal').remove()">×</button>
                </div>
                <div class="summary-modal-body">
                    <pre>${JSON.stringify(content, null, 2)}</pre>
                </div>
                <div class="summary-modal-footer">
                    <button class="btn-primary" onclick="revolutionaryInterface.copySummaryToClipboard(this)">Copy to Clipboard</button>
                    <button class="btn-secondary" onclick="this.closest('.summary-modal').remove()">Close</button>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
    }
    
    copySummaryToClipboard(button) {
        const summaryText = button.closest('.summary-modal').querySelector('pre').textContent;
        navigator.clipboard.writeText(summaryText).then(() => {
            this.showSuccess('Summary copied to clipboard!');
        });
    }
    
    pauseProcessing() {
        console.log('⏸️ Pause functionality not implemented yet');
        this.showError('Pause functionality coming soon');
    }
    
    stopProcessing() {
        if (this.statusPollingInterval) {
            clearInterval(this.statusPollingInterval);
            this.statusPollingInterval = null;
        }
        
        this.currentSession = null;
        this.currentMode = null;
        
        // Reset interface
        this.updateAgentBox('A', 'Stopped', 'Ready');
        this.updateAgentBox('B', 'Stopped', 'Ready');
        
        console.log('🛑 Processing stopped');
        this.showSuccess('Processing stopped');
    }
}

// Initialize the revolutionary interface when page loads
let revolutionaryInterface;

document.addEventListener('DOMContentLoaded', function() {
    revolutionaryInterface = new RevolutionaryInterface();
});

// CSS Styles for Revolutionary Interface (add to existing styles)
const revolutionaryStyles = `
<style>
.revolutionary-modes {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
    padding: 20px;
    margin: 20px 0;
    border: 1px solid rgba(0, 212, 170, 0.3);
}

.mode-buttons {
    display: flex;
    gap: 15px;
    margin-top: 15px;
}

.mode-btn {
    flex: 1;
    background: linear-gradient(45deg, #00d4aa, #00a085);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 15px;
    cursor: pointer;
    transition: all 0.3s ease;
    text-align: center;
}

.mode-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0, 212, 170, 0.3);
}

.mode-desc {
    display: block;
    font-size: 0.9em;
    opacity: 0.8;
    margin-top: 5px;
}

.revolutionary-status {
    background: rgba(0, 212, 170, 0.1);
    border-radius: 8px;
    padding: 10px;
    margin-bottom: 15px;
    border-left: 4px solid #00d4aa;
}

.status-badge {
    background: #00d4aa;
    color: white;
    padding: 4px 12px;
    border-radius: 15px;
    font-size: 0.8em;
    font-weight: bold;
    display: inline-block;
    margin-bottom: 8px;
}

.agent-info {
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.current-agent {
    font-weight: bold;
    color: #00d4aa;
}

.agent-specialty {
    font-size: 0.9em;
    color: #888;
}

.revolutionary-progress {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
    padding: 20px;
    margin: 20px 0;
    border: 1px solid rgba(0, 212, 170, 0.3);
}

.progress-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
}

.progress-controls {
    display: flex;
    gap: 10px;
}

.progress-bar-container {
    margin-bottom: 15px;
}

.progress-bar {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    height: 20px;
    overflow: hidden;
    position: relative;
}

.progress-fill {
    background: linear-gradient(45deg, #00d4aa, #00a085);
    height: 100%;
    width: 0%;
    transition: width 0.3s ease;
}

.progress-text {
    text-align: center;
    margin-top: 8px;
    font-weight: bold;
}

.current-processing {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(255, 255, 255, 0.05);
    padding: 10px;
    border-radius: 5px;
}

.summary-controls {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
    padding: 20px;
    margin: 20px 0;
    border: 1px solid rgba(0, 212, 170, 0.3);
}

.summary-buttons {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 10px;
    margin-top: 15px;
}

.summary-btn {
    background: rgba(0, 212, 170, 0.2);
    color: white;
    border: 1px solid #00d4aa;
    border-radius: 8px;
    padding: 12px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.summary-btn:hover {
    background: rgba(0, 212, 170, 0.4);
    transform: translateY(-1px);
}

.summary-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.summary-modal-content {
    background: #1a1a2e;
    border-radius: 10px;
    max-width: 80%;
    max-height: 80%;
    overflow: auto;
    border: 1px solid #00d4aa;
}

.summary-modal-header {
    background: linear-gradient(45deg, #00d4aa, #00a085);
    color: white;
    padding: 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.summary-modal-body {
    padding: 20px;
    max-height: 400px;
    overflow-y: auto;
}

.summary-modal-footer {
    padding: 15px;
    border-top: 1px solid rgba(0, 212, 170, 0.3);
    display: flex;
    gap: 10px;
    justify-content: flex-end;
}

.close-modal {
    background: none;
    border: none;
    color: white;
    font-size: 24px;
    cursor: pointer;
}
</style>
`;

// Inject styles
document.head.insertAdjacentHTML('beforeend', revolutionaryStyles);

