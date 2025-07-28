# AI Think Tank MVP

## 📋 项目概述

AI Think Tank MVP 是一个基于多智能体协作的AI项目咨询系统。通过5个专业AI Agent的协同工作，为用户提供从需求分析到技术选型的完整项目咨询服务。

### 🎯 **MVP版本特点**
- **轻量级设计**: 使用GPT-3.5-turbo模型，快速响应，成本友好
- **核心功能完整**: 涵盖项目咨询的完整工作流程
- **易于扩展**: 模块化设计，为后续升级到更复杂的模型和工业级功能奠定基础
- **演示就绪**: 开箱即用，适合演示和概念验证
市场分析报告（gemini输出）Visit Here: https://otismacos.github.io/AI-TaskForce-maket-analysis/


### 🎯 核心价值
- **智能需求分析** - 深度理解用户项目需求
- **专业任务规划** - 系统化分解项目任务
- **市场调研支持** - 提供竞品分析和市场洞察
- **PRD文档生成** - 自动生成产品需求文档
- **技术选型建议** - 推荐最适合的技术栈和工具

## 🏗️ 系统架构

### 整体架构图
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   用户界面层     │    │   API网关层      │    │   工作流编排层    │
│  (聊天界面)      │───▶│  (FastAPI)      │───▶│   (CrewAI)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   数据持久层     │◀───│   智能体层       │◀───│   消息解析层     │
│  (SQLite)       │    │   (5个Agent)    │    │  (LLM解析)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 核心组件

#### 1. **智能体层 (Agents)**
- **ChiefMindAgent** - 项目总指挥，负责需求分析和结果整合
- **TaskPlannerAgent** - 任务规划专家，分解项目任务
- **ResearcherAgent** - 市场研究员，进行竞品和技术调研
- **PRDWriterAgent** - 产品经理，编写产品需求文档
- **ToolFinderAgent** - 技术专家，推荐技术栈和工具

#### 2. **工作流编排层 (Workflow)**
- 基于CrewAI框架实现多智能体协作
- 6个核心任务节点，形成完整咨询流程
- 支持任务状态跟踪和结果持久化

#### 3. **API网关层 (API)**
- FastAPI框架提供RESTful API
- 统一的聊天接口，支持自然语言输入
- 智能消息解析，自动提取项目信息

#### 4. **数据持久层 (Database)**
- SQLAlchemy ORM管理数据模型
- SQLite数据库存储项目信息
- Alembic支持数据库迁移

## 🚀 功能特性

### 核心功能
1. **智能对话** - 支持自然语言输入，自动理解项目需求
2. **多智能体协作** - 5个专业Agent协同工作，各司其职
3. **完整工作流** - 从需求分析到技术选型的端到端服务
4. **文档生成** - 自动生成PRD、任务计划等技术文档
5. **技术推荐** - 基于项目特点推荐最适合的技术栈

### 技术特性
- **异步处理** - 支持并发请求处理
- **状态管理** - 实时跟踪工作流执行状态
- **数据持久化** - 完整保存项目咨询记录
- **模块化设计** - 易于扩展和维护
- **API优先** - 提供标准RESTful接口

## 📦 安装部署

### 环境要求
- Python 3.8+
- SQLite 3.x
- 8GB+ RAM (推荐)

### 快速开始

#### 1. 克隆项目
```bash
git clone <repository-url>
cd ai_thinktank_mvp
```

#### 2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

#### 3. 安装依赖
```bash
pip install -r requirements.txt
```

#### 4. 配置环境变量
```bash
# 创建 .env 文件
cp .env.example .env

# 编辑 .env 文件，配置OpenAI API
OPENAI_API_KEY=your_openai_api_key
OPENAI_API_BASE=https://api.openai.com/v1
```

#### 5. 初始化数据库
```bash
# 创建数据库表
python -c "from ai_thinktank_mvp.models.database import Base, engine; Base.metadata.create_all(bind=engine)"

# 或使用Alembic迁移（推荐）
alembic upgrade head
```

#### 6. 启动服务
```bash
uvicorn ai_thinktank_mvp.api.main:app --reload --host 0.0.0.0 --port 8000
```

### 访问服务
- API文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health

## 🎮 使用指南

### API接口

#### 1. 聊天咨询接口
```bash
POST /workflow/chat
Content-Type: application/json

{
  "message": "我想开发一个AI写作助手，我是程序员，预算10万，3个月上线"
}
```

#### 2. 查询工作流状态
```bash
GET /workflow/status/{project_id}
```

### 使用示例

#### 示例1：AI写作助手项目
```bash
curl -X POST "http://localhost:8000/workflow/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "我想开发一个AI写作助手，我是程序员，预算10万，3个月上线"
  }'
```

#### 示例2：电商平台项目
```bash
curl -X POST "http://localhost:8000/workflow/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "我要开发一个B2B电商平台，团队5人，计划6个月完成，预算50万"
  }'
```

### 工作流执行过程
1. **需求分析** - ChiefMind分析用户需求，输出细化需求
2. **任务规划** - TaskPlanner分解项目任务，制定计划
3. **市场调研** - Researcher调研竞品和技术趋势
4. **PRD编写** - PRDWriter生成产品需求文档
5. **工具选型** - ToolFinder推荐技术栈和工具
6. **结果评估** - ChiefMind整合所有结果，提供最终建议

## 📊 项目进度

### 🎯 整体进度：**95% 完成**

#### ✅ 已完成的核心功能 (100%)

##### 1. **Agent相关模块** (100%)
- ✅ **TaskPlannerAgent** - 任务规划专家，分解项目任务
- ✅ **ResearcherAgent** - 市场研究员，进行竞品和技术调研
- ✅ **PRDWriterAgent** - 产品经理，编写产品需求文档
- ✅ **ToolFinderAgent** - 技术专家，推荐技术栈和工具
- ✅ **ChiefMindAgent** - 项目总指挥，负责需求分析和结果整合

##### 2. **工作流编排** (100%)
- ✅ CrewAI多Agent协作工作流
- ✅ 6个核心任务节点完整实现
- ✅ 智能判断机制，区分简单对话和项目需求
- ✅ 工作流数据持久化

##### 3. **API层设计** (90%)
- ✅ 统一聊天接口 `/chat`
- ✅ 智能消息解析器
- ✅ 工作流状态查询接口
- ✅ FastAPI异步处理
- ✅ CORS中间件配置

##### 4. **数据库设计** (95%)
- ✅ SQLAlchemy ORM模型
- ✅ 数据库连接和会话管理
- ✅ Alembic迁移工具配置
- ✅ Project、Task、AgentOutput模型

##### 5. **前端交互功能** (100%)
- ✅ 现代化聊天界面，支持消息气泡和打字指示器
- ✅ 项目管理功能，项目创建和状态跟踪
- ✅ 工作流可视化，实时状态展示
- ✅ 响应式设计，支持桌面和移动设备

##### 6. **环境与配置** (100%)
- ✅ 环境变量配置管理
- ✅ 小爱OpenAI集成
- ✅ 项目依赖管理
- ✅ MIT开源许可证

#### ⏳ 进行中的工作 (80%)

##### 1. **集成与端到端流程** (80%)
- ✅ 端到端流程API实现
- ⏳ 查询产出接口完善
- ⏳ 状态跟踪增强

#### 🔄 待完成的任务 (10-20%)

##### 1. **测试与验证** (90%)
- ✅ 基础功能测试、Agent单元测试、数据库CRUD测试
- ⏳ 端到端测试（需要API密钥）
- ⏳ 性能测试优化

##### 2. **功能优化** (0%)
- ⏳ 数据库模型优化
- ⏳ 多模型支持（GPT-4、Claude、Vertex AI）
- ⏳ API接口完善
- ⏳ 工作流优化

##### 3. **部署和运维** (0%)
- ⏳ Docker容器化
- ⏳ 环境配置管理
- ⏳ 日志和监控

##### 4. **文档完善** (30%)
- ⏳ API文档完善
- ⏳ 部署文档
- ⏳ 用户使用指南

### 🎯 下一步优先级

#### **立即执行** (本周内)
1. **数据库模型优化** - 添加user_goal和user_context字段
2. **多模型支持** - 支持GPT-4、Claude等高级模型
3. **API接口完善** - 统一异常处理和错误码

#### **短期目标** (下周内)
1. **工作流优化** - 实时状态跟踪和错误恢复
2. **环境配置管理** - 统一配置和日志系统
3. **性能优化** - LLM调用和数据库查询优化

#### **中期目标** (下月内)
1. **测试完善** - 端到端测试和压力测试
2. **文档完善** - API文档和部署指南
3. **工业级功能** - 复杂交互和工业级文档生成

## 🛠️ 技术栈

### 后端技术
- **Python 3.8+** - 主要开发语言
- **FastAPI** - 现代Web框架
- **CrewAI** - 多智能体协作框架
- **SQLAlchemy** - ORM数据库操作
- **Alembic** - 数据库迁移工具
- **Pydantic** - 数据验证和序列化

### 模型架构演进
- **MVP阶段**: GPT-3.5-turbo - 轻量级，快速响应
- **进阶阶段**: GPT-4 - 更复杂的推理和文档生成
- **工业级阶段**: 多模型架构 - Claude、Vertex AI等，支持更复杂的交互和工业级文档生成

### AI/ML技术
- **OpenAI GPT-3.5-turbo** - MVP版本使用的大语言模型
- **OpenAI GPT-4** - 计划升级的高级模型（支持更复杂的推理）
- **Claude/Vertex AI** - 计划支持的多模型架构
- **LangChain** - LLM应用框架
- **Prompt Engineering** - 提示词工程

### 数据库
- **SQLite** - 轻量级数据库
- **SQLAlchemy ORM** - 对象关系映射

### 开发工具
- **uvicorn** - ASGI服务器
- **pytest** - 测试框架
- **black** - 代码格式化
- **flake8** - 代码检查

## 📁 项目结构

```
ai_thinktank_mvp/
├── agents/                 # 智能体模块
│   ├── __init__.py
│   ├── agent_factory.py   # Agent工厂
│   ├── base.py           # 基础Agent类
│   ├── chiefmind.py      # 总指挥Agent
│   ├── taskplanner.py    # 任务规划Agent
│   ├── researcher.py     # 研究员Agent
│   ├── prdwriter.py      # PRD编写Agent
│   └── toolfinder.py     # 工具选型Agent
├── api/                   # API层
│   ├── __init__.py
│   ├── main.py           # FastAPI应用入口
│   ├── config.py         # 配置管理
│   └── workflow_api.py   # 工作流API
├── models/               # 数据模型
│   ├── __init__.py
│   ├── database.py       # 数据库配置
│   └── project.py        # 项目数据模型
├── workflows/            # 工作流模块
│   ├── __init__.py
│   └── crewai_workflow.py # CrewAI工作流
├── utils/                # 工具模块
│   ├── __init__.py
│   └── message_parser.py # 消息解析器
├── db/                   # 数据库文件
├── alembic/              # 数据库迁移
├── tests/                # 测试文件
│   ├── test_agents.py    # Agent单元测试
│   ├── test_database_crud.py # 数据库CRUD测试
│   ├── test_simple.py    # 基础功能测试
│   ├── test_basic_workflow.py # 工作流测试
│   ├── test_config.py    # 配置测试
│   └── test_summary_report.md # 测试报告
├── frontend/             # 前端界面
│   ├── index.html        # 主页面
│   ├── app.js           # 前端逻辑
│   └── server.py        # 前端服务器
├── requirements.txt      # 依赖包
└── README.md            # 项目文档
```

## 🤝 贡献指南

### 开发环境设置
1. Fork项目到你的GitHub账户
2. 克隆你的Fork到本地
3. 创建功能分支：`git checkout -b feature/your-feature`
4. 提交更改：`git commit -am 'Add some feature'`
5. 推送分支：`git push origin feature/your-feature`
6. 创建Pull Request

### 代码规范
- 使用Python PEP 8代码风格
- 添加适当的注释和文档字符串
- 编写单元测试覆盖新功能
- 确保所有测试通过

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系方式

- 项目维护者：[Otis K]
- 邮箱：[Otis_da@163.com]
- 项目地址：[https://github.com/OtisMacOS/AI-TaskForce_mvp]

## 🙏 致谢

感谢以下开源项目和社区的支持：
- [CrewAI](https://github.com/joaomdmoura/crewAI) - 多智能体协作框架
- [FastAPI](https://fastapi.tiangolo.com/) - 现代Web框架
- [SQLAlchemy](https://www.sqlalchemy.org/) - Python ORM
- [OpenAI](https://openai.com/) - 大语言模型服务

---

**AI Think Tank MVP** - 让AI为你的项目提供专业咨询服务 🚀
