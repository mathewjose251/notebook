/* Chat Widget Integration for Sanchari Mentors */

// Tawk.to Chat Widget Integration
function initializeChatWidget() {
    // Tawk.to widget script
    var Tawk_API = Tawk_API || {};
    var Tawk_LoadStart = new Date();
    
    // Custom styling for Sanchari Mentors
    Tawk_API.customStyle = {
        visibility: {
            desktop: {
                position: 'br',
                xOffset: 20,
                yOffset: 20
            },
            mobile: {
                position: 'br',
                xOffset: 10,
                yOffset: 10
            }
        },
        widget: {
            color: {
                theme: '#B91C1C', // Ruby red from our theme
                launcherText: '#FFFFFF',
                button: '#B91C1C',
                buttonText: '#FFFFFF',
                header: '#B91C1C',
                article: '#F97316' // Orange accent
            }
        }
    };

    // Custom messages for admin support
    Tawk_API.onLoad = function() {
        // Set custom greeting for admins
        if (window.location.pathname.includes('/admin/')) {
            Tawk_API.setAttributes({
                'name': 'Admin User',
                'department': 'Admin Support',
                'priority': 'high'
            });
        } else if (window.location.pathname.includes('/trainer/')) {
            Tawk_API.setAttributes({
                'name': 'Trainer User',
                'department': 'Trainer Support',
                'priority': 'medium'
            });
        } else {
            Tawk_API.setAttributes({
                'name': 'Student User',
                'department': 'Student Support',
                'priority': 'normal'
            });
        }
    };

    // Load the Tawk.to script
    (function() {
        var s1 = document.createElement("script");
        var s0 = document.getElementsByTagName("script")[0];
        s1.async = true;
        s1.src = 'https://embed.tawk.to/YOUR_TAWK_ID/default';
        s1.charset = 'UTF-8';
        s1.setAttribute('crossorigin', '*');
        s0.parentNode.insertBefore(s1, s0);
    })();
}

// Alternative: Custom Chat Widget for Admin Support
function createCustomChatWidget() {
    // Create chat widget HTML
    const chatWidget = document.createElement('div');
    chatWidget.id = 'sanchari-chat-widget';
    chatWidget.innerHTML = `
        <div class="chat-widget-container">
            <div class="chat-widget-button" onclick="toggleChat()">
                <i class="fas fa-comments"></i>
                <span class="chat-badge">Admin Support</span>
            </div>
            <div class="chat-widget-window" id="chatWindow" style="display: none;">
                <div class="chat-header">
                    <h4><i class="fas fa-headset"></i> Sanchari Admin Support</h4>
                    <button onclick="toggleChat()" class="chat-close">×</button>
                </div>
                <div class="chat-body">
                    <div class="chat-messages" id="chatMessages">
                        <div class="message bot-message">
                            <div class="message-content">
                                <p>👋 Hi! I'm here to help you manage your training and mentors. How can I assist you today?</p>
                                <div class="quick-actions">
                                    <button onclick="sendQuickMessage('How do I create a new training session?')" class="quick-btn">
                                        <i class="fas fa-plus"></i> Create Training
                                    </button>
                                    <button onclick="sendQuickMessage('How do I manage mentors?')" class="quick-btn">
                                        <i class="fas fa-users"></i> Manage Mentors
                                    </button>
                                    <button onclick="sendQuickMessage('How do I view reports?')" class="quick-btn">
                                        <i class="fas fa-chart-bar"></i> View Reports
                                    </button>
                                    <button onclick="sendQuickMessage('How do I send notifications?')" class="quick-btn">
                                        <i class="fas fa-bell"></i> Send Notifications
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="chat-input-container">
                        <input type="text" id="chatInput" placeholder="Type your message..." onkeypress="handleEnter(event)">
                        <button onclick="sendMessage()" class="send-btn">
                            <i class="fas fa-paper-plane"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Add CSS styles
    const chatStyles = document.createElement('style');
    chatStyles.textContent = `
        .chat-widget-container {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 1000;
            font-family: var(--font-primary);
        }

        .chat-widget-button {
            background: var(--gradient-primary);
            color: white;
            border-radius: 50px;
            padding: 15px 20px;
            cursor: pointer;
            box-shadow: var(--shadow-warm);
            display: flex;
            align-items: center;
            gap: 10px;
            transition: var(--transition-normal);
            animation: pulse 2s infinite;
        }

        .chat-widget-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(185, 28, 28, 0.3);
        }

        .chat-badge {
            background: rgba(255, 255, 255, 0.2);
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 600;
        }

        .chat-widget-window {
            position: absolute;
            bottom: 70px;
            right: 0;
            width: 350px;
            height: 500px;
            background: white;
            border-radius: var(--radius-lg);
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
            display: flex;
            flex-direction: column;
            overflow: hidden;
            animation: slideUp 0.3s ease-out;
        }

        .chat-header {
            background: var(--gradient-primary);
            color: white;
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .chat-header h4 {
            margin: 0;
            font-size: 1rem;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .chat-close {
            background: none;
            border: none;
            color: white;
            font-size: 1.5rem;
            cursor: pointer;
            padding: 0;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: var(--transition-fast);
        }

        .chat-close:hover {
            background: rgba(255, 255, 255, 0.2);
        }

        .chat-body {
            flex: 1;
            display: flex;
            flex-direction: column;
        }

        .chat-messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            max-height: 350px;
        }

        .message {
            margin-bottom: 15px;
            animation: fadeIn 0.3s ease-in;
        }

        .message-content {
            background: #F3F4F6;
            padding: 12px 16px;
            border-radius: 18px;
            max-width: 80%;
        }

        .bot-message .message-content {
            background: var(--gradient-secondary);
            color: white;
            margin-left: 0;
        }

        .user-message .message-content {
            background: var(--primary-ruby);
            color: white;
            margin-left: auto;
        }

        .quick-actions {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
            margin-top: 12px;
        }

        .quick-btn {
            background: rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
            color: white;
            padding: 8px 12px;
            border-radius: 8px;
            font-size: 0.8rem;
            cursor: pointer;
            transition: var(--transition-fast);
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .quick-btn:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-1px);
        }

        .chat-input-container {
            padding: 15px 20px;
            border-top: 1px solid #E5E7EB;
            display: flex;
            gap: 10px;
            align-items: center;
        }

        #chatInput {
            flex: 1;
            border: 2px solid #E5E7EB;
            border-radius: 20px;
            padding: 10px 15px;
            outline: none;
            transition: var(--transition-fast);
        }

        #chatInput:focus {
            border-color: var(--primary-blue);
        }

        .send-btn {
            background: var(--gradient-primary);
            border: none;
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: var(--transition-fast);
        }

        .send-btn:hover {
            transform: scale(1.1);
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }

        @media (max-width: 768px) {
            .chat-widget-window {
                width: 300px;
                height: 400px;
            }
            
            .quick-actions {
                grid-template-columns: 1fr;
            }
        }
    `;

    document.head.appendChild(chatStyles);
    document.body.appendChild(chatWidget);
}

// Chat functionality
function toggleChat() {
    const chatWindow = document.getElementById('chatWindow');
    if (chatWindow.style.display === 'none') {
        chatWindow.style.display = 'block';
    } else {
        chatWindow.style.display = 'none';
    }
}

function sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    if (message) {
        addMessage(message, 'user');
        input.value = '';
        
        // Simulate bot response
        setTimeout(() => {
            const response = generateBotResponse(message);
            addMessage(response, 'bot');
        }, 1000);
    }
}

function sendQuickMessage(message) {
    addMessage(message, 'user');
    setTimeout(() => {
        const response = generateBotResponse(message);
        addMessage(response, 'bot');
    }, 1000);
}

function addMessage(text, sender) {
    const messagesContainer = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    messageDiv.innerHTML = `
        <div class="message-content">
            <p>${text}</p>
        </div>
    `;
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function generateBotResponse(userMessage) {
    const responses = {
        'How do I create a new training session?': `
            <p>To create a new training session:</p>
            <ol>
                <li>Go to <strong>Admin Dashboard</strong></li>
                <li>Click on <strong>Classes</strong> in the sidebar</li>
                <li>Click <strong>"Create New Class"</strong></li>
                <li>Fill in the training details</li>
                <li>Select interested students will be notified automatically</li>
                <li>Google Meet link will be generated automatically</li>
            </ol>
            <p>Need help with any specific step?</p>
        `,
        'How do I manage mentors?': `
            <p>To manage mentors/trainers:</p>
            <ul>
                <li><strong>View All Trainers:</strong> Admin → Trainers</li>
                <li><strong>Add New Trainer:</strong> Click "Add Trainer" button</li>
                <li><strong>Edit Trainer:</strong> Click on trainer name</li>
                <li><strong>Assign Classes:</strong> Go to Classes → Assign Trainer</li>
                <li><strong>View Performance:</strong> Reports → Trainer Analytics</li>
            </ul>
        `,
        'How do I view reports?': `
            <p>Access comprehensive reports:</p>
            <ul>
                <li><strong>Student Progress:</strong> Reports → Student Analytics</li>
                <li><strong>Attendance:</strong> Reports → Attendance Reports</li>
                <li><strong>Platform Analytics:</strong> Dashboard → Analytics Section</li>
                <li><strong>Export Data:</strong> Click "Export" on any report</li>
            </ul>
        `,
        'How do I send notifications?': `
            <p>Send notifications to users:</p>
            <ul>
                <li><strong>Bulk Notifications:</strong> Communications → Send Announcement</li>
                <li><strong>Training Alerts:</strong> Auto-sent when publishing new training</li>
                <li><strong>Custom Messages:</strong> Select users and compose message</li>
                <li><strong>Email Templates:</strong> Use pre-built templates</li>
            </ul>
        `
    };

    // Check for exact matches first
    if (responses[userMessage]) {
        return responses[userMessage];
    }

    // Check for partial matches
    const lowerMessage = userMessage.toLowerCase();
    if (lowerMessage.includes('training') || lowerMessage.includes('class')) {
        return responses['How do I create a new training session?'];
    } else if (lowerMessage.includes('mentor') || lowerMessage.includes('trainer')) {
        return responses['How do I manage mentors?'];
    } else if (lowerMessage.includes('report') || lowerMessage.includes('analytics')) {
        return responses['How do I view reports?'];
    } else if (lowerMessage.includes('notification') || lowerMessage.includes('email')) {
        return responses['How do I send notifications?'];
    }

    // Default response
    return `
        <p>I understand you're asking about: "${userMessage}"</p>
        <p>Here are some common admin tasks I can help with:</p>
        <ul>
            <li>Creating and managing training sessions</li>
            <li>Managing mentors and trainers</li>
            <li>Viewing reports and analytics</li>
            <li>Sending notifications to users</li>
        </ul>
        <p>Could you please be more specific about what you'd like to do?</p>
    `;
}

function handleEnter(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

// Initialize chat widget when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Only show chat widget on admin and trainer pages
    if (window.location.pathname.includes('/admin/') || window.location.pathname.includes('/trainer/')) {
        createCustomChatWidget();
    }

    var chatWidget = document.getElementById('sanchari-chat-widget');
    var chatToggle = chatWidget.querySelector('.chat-widget-button');
    var chatBody = chatWidget.querySelector('.chat-widget-window');
    var isOpen = true;
    chatToggle.addEventListener('click', function() {
        isOpen = !isOpen;
        chatBody.style.display = isOpen ? 'block' : 'none';
        chatWidget.style.height = isOpen ? '' : '60px';
        chatToggle.innerHTML = isOpen ? '<i class="fas fa-comments"></i>' : '<i class="fas fa-comment-dots"></i>';
    });

    // Optionally, focus input when opened
    if (chatBody && chatBody.querySelector('input[type="text"]')) {
        chatToggle.addEventListener('click', function() {
            if (isOpen) {
                setTimeout(function() {
                    chatBody.querySelector('input[type="text"]').focus();
                }, 200);
            }
        });
    }
});

// Export functions for global use
window.toggleChat = toggleChat;
window.sendMessage = sendMessage;
window.sendQuickMessage = sendQuickMessage;
window.handleEnter = handleEnter;

// Chat Widget with Close and Minimize functionality
class ChatWidget {
    constructor() {
        this.isOpen = false;
        this.isMinimized = false;
        this.createWidget();
        this.bindEvents();
    }

    createWidget() {
        // Create main container
        this.container = document.createElement('div');
        this.container.id = 'chat-widget-container';
        this.container.innerHTML = `
            <div id="chat-widget" class="chat-widget">
                <div class="chat-header">
                    <div class="chat-title">
                        <i class="fas fa-comments"></i>
                        <span>Chat with us</span>
                    </div>
                    <div class="chat-controls">
                        <button id="minimize-btn" class="chat-btn minimize-btn" title="Minimize">
                            <i class="fas fa-minus"></i>
                        </button>
                        <button id="close-btn" class="chat-btn close-btn" title="Close">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                </div>
                <div id="chat-body" class="chat-body">
                    <div class="chat-messages" id="chat-messages">
                        <div class="message bot-message">
                            <div class="message-content">
                                <i class="fas fa-robot"></i>
                                <div class="message-text">
                                    <p>👋 Hi! I'm your AI assistant. How can I help you today?</p>
                                    <div class="quick-replies">
                                        <button class="quick-reply" data-message="I want to learn about courses">📚 Courses</button>
                                        <button class="quick-reply" data-message="How do I get started?">🚀 Get Started</button>
                                        <button class="quick-reply" data-message="Contact support">📞 Support</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="chat-input-container">
                        <input type="text" id="chat-input" placeholder="Type your message..." maxlength="500">
                        <button id="send-btn" class="send-btn">
                            <i class="fas fa-paper-plane"></i>
                        </button>
                    </div>
                </div>
            </div>
            <div id="chat-toggle" class="chat-toggle">
                <i class="fas fa-comments"></i>
                <span class="notification-badge" id="notification-badge" style="display: none;">1</span>
            </div>
        `;
        
        document.body.appendChild(this.container);
    }

    bindEvents() {
        // Toggle chat
        document.getElementById('chat-toggle').addEventListener('click', () => {
            this.toggleChat();
        });

        // Close button
        document.getElementById('close-btn').addEventListener('click', () => {
            this.closeChat();
        });

        // Minimize button
        document.getElementById('minimize-btn').addEventListener('click', () => {
            this.toggleMinimize();
        });

        // Send message
        document.getElementById('send-btn').addEventListener('click', () => {
            this.sendMessage();
        });

        // Enter key to send
        document.getElementById('chat-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });

        // Quick replies
        document.querySelectorAll('.quick-reply').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const message = e.target.dataset.message;
                this.addMessage(message, 'user');
                this.handleQuickReply(message);
            });
        });
    }

    toggleChat() {
        const chatWidget = document.getElementById('chat-widget');
        const chatToggle = document.getElementById('chat-toggle');
        
        if (this.isOpen) {
            chatWidget.style.display = 'none';
            chatToggle.style.display = 'flex';
            this.isOpen = false;
        } else {
            chatWidget.style.display = 'flex';
            chatToggle.style.display = 'none';
            this.isOpen = true;
            this.hideNotification();
            document.getElementById('chat-input').focus();
        }
    }

    closeChat() {
        const chatWidget = document.getElementById('chat-widget');
        const chatToggle = document.getElementById('chat-toggle');
        
        chatWidget.style.display = 'none';
        chatToggle.style.display = 'flex';
        this.isOpen = false;
        this.isMinimized = false;
    }

    toggleMinimize() {
        const chatBody = document.getElementById('chat-body');
        const minimizeBtn = document.getElementById('minimize-btn');
        
        if (this.isMinimized) {
            chatBody.style.display = 'block';
            minimizeBtn.innerHTML = '<i class="fas fa-minus"></i>';
            this.isMinimized = false;
        } else {
            chatBody.style.display = 'none';
            minimizeBtn.innerHTML = '<i class="fas fa-plus"></i>';
            this.isMinimized = true;
        }
    }

    addMessage(text, sender) {
        const messagesContainer = document.getElementById('chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const icon = sender === 'user' ? 'fas fa-user' : 'fas fa-robot';
        const messageContent = sender === 'user' ? text : this.generateResponse(text);
        
        messageDiv.innerHTML = `
            <div class="message-content">
                <i class="${icon}"></i>
                <div class="message-text">
                    <p>${messageContent}</p>
                </div>
            </div>
        `;
        
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    sendMessage() {
        const input = document.getElementById('chat-input');
        const message = input.value.trim();
        
        if (message) {
            this.addMessage(message, 'user');
            input.value = '';
            
            // Simulate bot response
            setTimeout(() => {
                this.addMessage(message, 'bot');
            }, 1000);
        }
    }

    handleQuickReply(message) {
        setTimeout(() => {
            let response = '';
            switch(message) {
                case 'I want to learn about courses':
                    response = 'Great! We offer various courses in programming, design, and business. You can browse our course catalog or speak with a mentor for personalized guidance.';
                    break;
                case 'How do I get started?':
                    response = 'Getting started is easy! 1) Sign up for an account, 2) Browse our courses, 3) Enroll in a course that interests you, 4) Connect with mentors. Would you like me to help you with any specific step?';
                    break;
                case 'Contact support':
                    response = 'Our support team is here to help! You can reach us at support@sanchari.com or call us at +1-800-SANCHARI. We typically respond within 2 hours.';
                    break;
                default:
                    response = 'Thanks for your message! I\'ll connect you with a human representative shortly.';
            }
            this.addMessage(response, 'bot');
        }, 1000);
    }

    generateResponse(userMessage) {
        const responses = [
            "That's a great question! Let me connect you with one of our mentors who can help you better.",
            "I understand your interest. Our platform offers personalized learning paths. Would you like to explore our course catalog?",
            "Thanks for reaching out! I'm here to help you succeed in your learning journey.",
            "That's an interesting point. Let me get you in touch with our support team for detailed assistance.",
            "I appreciate your question. Our mentors are experts in this area and would be happy to help you."
        ];
        
        return responses[Math.floor(Math.random() * responses.length)];
    }

    showNotification() {
        const badge = document.getElementById('notification-badge');
        badge.style.display = 'block';
    }

    hideNotification() {
        const badge = document.getElementById('notification-badge');
        badge.style.display = 'none';
    }
}

// Initialize chat widget when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ChatWidget();
});

