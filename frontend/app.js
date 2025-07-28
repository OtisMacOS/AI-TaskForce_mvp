// AI Think Tank MVP 前端应用
class AIThinkTankApp {
    constructor() {
        this.currentProject = null;
        this.isProcessing = false;
        this.apiBaseUrl = 'http://localhost:8000';
        
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.loadProjects();
    }
    
    bindEvents() {
        // 发送消息
        document.getElementById('sendBtn').addEventListener('click', () => this.sendMessage());
        document.getElementById('messageInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // 新建项目
        document.getElementById('newProjectBtn').addEventListener('click', () => this.showNewProjectModal());
        document.getElementById('cancelNewProject').addEventListener('click', () => this.hideNewProjectModal());
        document.getElementById('newProjectForm').addEventListener('submit', (e) => this.createProject(e));
        
        // 项目管理
        document.getElementById('projectsBtn').addEventListener('click', () => this.showProjectsList());
    }
    
    // 发送消息
    async sendMessage() {
        const messageInput = document.getElementById('messageInput');
        const message = messageInput.value.trim();
        
        if (!message || this.isProcessing) return;
        
        // 添加用户消息到聊天界面
        this.addMessage(message, 'user');
        messageInput.value = '';
        
        // 显示AI正在处理
        this.showTypingIndicator();
        this.isProcessing = true;
        
        try {
            // 调用API
            const response = await this.callWorkflowAPI(message);
            
            // 隐藏打字指示器
            this.hideTypingIndicator();
            
            // 添加AI响应
            this.addMessage(response.workflow_result, 'ai');
            
            // 更新工作流状态
            this.updateWorkflowStatus(response.individual_outputs);
            
            // 更新项目信息
            this.updateProjectInfo(response.project_id);
            
        } catch (error) {
            console.error('发送消息失败:', error);
            this.hideTypingIndicator();
            this.addMessage('抱歉，处理您的请求时出现了错误。请稍后重试。', 'ai', 'error');
        } finally {
            this.isProcessing = false;
        }
    }
    
    // 调用工作流API
    async callWorkflowAPI(message) {
        const response = await fetch(`${this.apiBaseUrl}/workflow/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message
            })
        });
        
        if (!response.ok) {
            throw new Error(`API调用失败: ${response.status}`);
        }
        
        return await response.json();
    }
    
    // 添加消息到聊天界面
    addMessage(content, sender, type = 'normal') {
        const chatMessages = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = 'chat-bubble';
        
        const isUser = sender === 'user';
        const bgColor = type === 'error' ? 'bg-red-50' : (isUser ? 'bg-green-50' : 'bg-blue-50');
        const icon = isUser ? 'fas fa-user' : 'fas fa-robot';
        const iconBg = isUser ? 'bg-green-500' : 'bg-blue-500';
        
        messageDiv.innerHTML = `
            <div class="flex items-start space-x-3">
                <div class="w-8 h-8 ${iconBg} rounded-full flex items-center justify-center">
                    <i class="${icon} text-white text-sm"></i>
                </div>
                <div class="flex-1">
                    <div class="${bgColor} rounded-lg p-4">
                        <p class="text-gray-800 whitespace-pre-wrap">${this.escapeHtml(content)}</p>
                    </div>
                </div>
            </div>
        `;
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // 显示打字指示器
    showTypingIndicator() {
        const chatMessages = document.getElementById('chatMessages');
        const typingDiv = document.createElement('div');
        typingDiv.id = 'typingIndicator';
        typingDiv.className = 'chat-bubble';
        
        typingDiv.innerHTML = `
            <div class="flex items-start space-x-3">
                <div class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
                    <i class="fas fa-robot text-white text-sm"></i>
                </div>
                <div class="flex-1">
                    <div class="bg-blue-50 rounded-lg p-4">
                        <div class="flex items-center space-x-2">
                            <div class="typing-indicator"></div>
                            <span class="text-gray-600 text-sm">AI正在思考中...</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // 隐藏打字指示器
    hideTypingIndicator() {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    // 更新工作流状态
    updateWorkflowStatus(individualOutputs) {
        const workflowSteps = document.querySelectorAll('#workflowStatus .workflow-step');
        
        workflowSteps.forEach((step, index) => {
            const agentName = step.querySelector('span').textContent;
            const statusSpan = step.querySelector('.text-xs');
            
            // 根据输出更新状态
            if (individualOutputs && individualOutputs[agentName.toLowerCase()]) {
                step.classList.remove('active');
                step.classList.add('completed');
                statusSpan.textContent = '已完成';
                statusSpan.className = 'text-xs text-green-600 font-medium';
            } else {
                step.classList.remove('completed', 'active');
                statusSpan.textContent = '待执行';
                statusSpan.className = 'text-xs text-gray-500';
            }
        });
    }
    
    // 更新项目信息
    updateProjectInfo(projectId) {
        if (projectId) {
            this.currentProject = projectId;
            const projectInfo = document.getElementById('projectInfo');
            
            // 更新项目状态
            const statusElement = projectInfo.querySelector('.text-gray-800.font-medium');
            if (statusElement) {
                statusElement.textContent = '进行中';
                statusElement.className = 'text-gray-800 font-medium text-blue-600';
            }
            
            // 更新创建时间
            const timeElement = projectInfo.querySelectorAll('.text-gray-800')[1];
            if (timeElement) {
                timeElement.textContent = new Date().toLocaleString();
            }
            
            // 更新任务数量
            const taskElement = projectInfo.querySelectorAll('.text-gray-800')[2];
            if (taskElement) {
                taskElement.textContent = '5'; // 5个智能体任务
            }
        }
    }
    
    // 显示新建项目模态框
    showNewProjectModal() {
        document.getElementById('newProjectModal').classList.remove('hidden');
        document.getElementById('newProjectModal').classList.add('flex');
    }
    
    // 隐藏新建项目模态框
    hideNewProjectModal() {
        document.getElementById('newProjectModal').classList.add('hidden');
        document.getElementById('newProjectModal').classList.remove('flex');
        document.getElementById('newProjectForm').reset();
    }
    
    // 创建新项目
    async createProject(event) {
        event.preventDefault();
        
        const projectName = document.getElementById('projectName').value;
        const projectDescription = document.getElementById('projectDescription').value;
        
        if (!projectName.trim()) {
            alert('请输入项目名称');
            return;
        }
        
        try {
            // 这里可以调用创建项目的API
            console.log('创建项目:', { projectName, projectDescription });
            
            // 添加项目创建消息
            this.addMessage(`项目 "${projectName}" 创建成功！现在可以开始描述您的项目需求了。`, 'ai');
            
            this.hideNewProjectModal();
            
        } catch (error) {
            console.error('创建项目失败:', error);
            alert('创建项目失败，请重试');
        }
    }
    
    // 显示项目列表
    showProjectsList() {
        // 这里可以实现项目列表页面
        alert('项目管理功能正在开发中...');
    }
    
    // 加载项目列表
    async loadProjects() {
        try {
            // 这里可以调用获取项目列表的API
            console.log('加载项目列表');
        } catch (error) {
            console.error('加载项目列表失败:', error);
        }
    }
    
    // HTML转义
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    // 模拟工作流执行（用于演示）
    simulateWorkflow() {
        const agents = ['ChiefMind', 'TaskPlanner', 'Researcher', 'PRDWriter', 'ToolFinder'];
        let currentIndex = 0;
        
        const interval = setInterval(() => {
            if (currentIndex < agents.length) {
                this.updateAgentStatus(agents[currentIndex], 'active');
                currentIndex++;
            } else {
                clearInterval(interval);
                // 完成所有任务
                agents.forEach(agent => {
                    this.updateAgentStatus(agent, 'completed');
                });
            }
        }, 2000);
    }
    
    // 更新智能体状态
    updateAgentStatus(agentName, status) {
        const workflowSteps = document.querySelectorAll('#workflowStatus .workflow-step');
        
        workflowSteps.forEach(step => {
            const stepName = step.querySelector('span').textContent;
            if (stepName === agentName) {
                const statusSpan = step.querySelector('.text-xs');
                
                step.classList.remove('active', 'completed');
                
                if (status === 'active') {
                    step.classList.add('active');
                    statusSpan.textContent = '执行中';
                    statusSpan.className = 'text-xs text-blue-600 font-medium';
                } else if (status === 'completed') {
                    step.classList.add('completed');
                    statusSpan.textContent = '已完成';
                    statusSpan.className = 'text-xs text-green-600 font-medium';
                }
            }
        });
    }
}

// 初始化应用
document.addEventListener('DOMContentLoaded', () => {
    window.app = new AIThinkTankApp();
    
    // 添加演示功能
    console.log('AI Think Tank MVP 前端应用已启动');
    console.log('提示：在聊天框中输入项目需求来测试功能');
    
    // 添加键盘快捷键
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + Enter 发送消息
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            window.app.sendMessage();
        }
        
        // Ctrl/Cmd + N 新建项目
        if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
            e.preventDefault();
            window.app.showNewProjectModal();
        }
    });
});

// 工具函数
const Utils = {
    // 格式化时间
    formatTime(date) {
        return new Date(date).toLocaleString('zh-CN');
    },
    
    // 生成唯一ID
    generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    },
    
    // 防抖函数
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // 节流函数
    throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        }
    }
}; 