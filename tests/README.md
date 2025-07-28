# AI Think Tank MVP - 测试文件

## 📁 测试文件结构

本文件夹包含AI Think Tank MVP项目的所有测试文件和配置。

### 🧪 测试文件说明

#### 核心功能测试
- **test_simple.py** - 基础功能测试，验证模块导入、数据库连接等
- **test_agents.py** - Agent单元测试，验证所有5个智能体的功能
- **test_database_crud.py** - 数据库CRUD测试，验证数据模型的增删改查
- **test_basic_workflow.py** - 工作流基础测试，验证CrewAI工作流结构

#### 配置和集成测试
- **test_config.py** - 配置测试，验证环境变量和LLM连接
- **test_taskplanner_agent.py** - TaskPlanner Agent专项测试

#### 文档和报告
- **test_summary_report.md** - 测试执行总结报告
- **CONFIG.md** - 配置说明文档

### 🚀 运行测试

#### 1. 基础功能测试
```bash
cd tests
python test_simple.py
```

#### 2. Agent单元测试
```bash
python test_agents.py
```

#### 3. 数据库测试
```bash
python test_database_crud.py
```

#### 4. 配置测试
```bash
python test_config.py
```

### 📊 测试覆盖范围

- ✅ **模块导入测试** - 验证所有模块可以正确导入
- ✅ **数据库连接测试** - 验证SQLAlchemy连接和模型定义
- ✅ **Agent创建测试** - 验证所有5个智能体可以正确创建
- ✅ **Agent方法测试** - 验证智能体的核心方法功能
- ✅ **数据库CRUD测试** - 验证Project、Task、AgentOutput模型的完整操作
- ✅ **工作流结构测试** - 验证CrewAI工作流的基础结构
- ✅ **配置管理测试** - 验证环境变量和LLM配置

### 🎯 测试环境要求

- Python 3.8+
- 虚拟环境已激活
- 依赖包已安装
- 环境变量已配置（.env文件）

### 📝 注意事项

1. **API密钥**: 部分测试需要有效的OpenAI API密钥
2. **数据库**: 测试会创建临时数据库文件
3. **网络连接**: LLM相关测试需要网络连接
4. **测试顺序**: 建议按顺序运行测试文件

### 🔄 持续集成

这些测试文件为后续的CI/CD流程提供了基础，可以集成到自动化测试流程中。 