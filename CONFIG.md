# 🔧 AI Think Tank MVP 配置说明

## 🎯 统一配置：小爱OpenAI接口

### 📋 环境变量配置

创建 `.env` 文件并配置以下变量：

```bash
# ===== 小爱OpenAI接口配置 =====
OPENAI_API_BASE=https://xiaoai.plus/v1
OPENAI_API_KEY=sk-your-xiaoai-api-key-here
OPENAI_MODEL=gpt-4o-mini

# ===== 数据库配置 =====
DATABASE_URL=sqlite:///./ai_thinktank.db

# ===== 应用配置 =====
ENVIRONMENT=development
DEBUG=true
API_PORT=8000
FRONTEND_PORT=3000
```

### 🔑 获取小爱OpenAI API密钥

1. 访问 [小爱AI官网](https://xiaoai.plus)
2. 注册并登录账户
3. 在控制台获取API密钥
4. 将密钥填入 `.env` 文件

### 🚀 快速配置步骤

#### 1. 创建环境配置文件
```bash
# 在项目根目录创建 .env 文件
touch .env
```

#### 2. 编辑配置文件
```bash
# 使用你喜欢的编辑器
nano .env
# 或
vim .env
```

#### 3. 填入配置信息
```bash
# 小爱OpenAI配置
OPENAI_API_BASE=https://xiaoai.plus/v1
OPENAI_API_KEY=sk-your-actual-api-key
OPENAI_MODEL=gpt-4o-mini

# 其他配置
DATABASE_URL=sqlite:///./ai_thinktank.db
ENVIRONMENT=development
DEBUG=true
```

### 📁 配置文件位置

- **项目根目录**: `.env` (环境变量)
- **API配置**: `ai_thinktank_mvp/api/config.py`
- **LLM模块**: `llm_module.py`

### 🔄 配置更新

#### 已更新的文件：
1. ✅ `llm_module.py` - 默认使用小爱接口
2. ✅ `ai_thinktank_mvp/api/config.py` - 统一配置
3. ✅ 所有Agent使用统一LLM配置

#### 配置特点：
- **统一接口**: 所有组件使用相同的小爱OpenAI配置
- **灵活切换**: 通过环境变量可以轻松切换不同模型
- **默认优化**: 默认使用 `gpt-4o-mini` 模型，性价比高

### 🎯 推荐配置

#### 开发环境
```bash
OPENAI_MODEL=gpt-4o-mini  # 快速响应，成本低
DEBUG=true
ENVIRONMENT=development
```

#### 生产环境
```bash
OPENAI_MODEL=gpt-4o  # 更高质量输出
DEBUG=false
ENVIRONMENT=production
```

### 🔍 配置验证

#### 1. 检查配置是否正确
```bash
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print(f'API Base: {os.getenv(\"OPENAI_API_BASE\")}')
print(f'Model: {os.getenv(\"OPENAI_MODEL\")}')
print(f'API Key: {os.getenv(\"OPENAI_API_KEY\")[:10]}...')
"
```

#### 2. 测试API连接
```bash
python -c "
from llm_module import chat_completion
try:
    result = chat_completion([{'role': 'user', 'content': 'Hello'}])
    print('✅ API连接成功')
    print(f'回复: {result}')
except Exception as e:
    print(f'❌ API连接失败: {e}')
"
```

### 🛠️ 故障排除

#### 常见问题：

1. **API密钥错误**
   - 检查 `.env` 文件中的 `OPENAI_API_KEY`
   - 确保密钥格式正确 (以 `sk-` 开头)

2. **网络连接问题**
   - 检查网络连接
   - 确认可以访问 `https://xiaoai.plus`

3. **模型不可用**
   - 检查账户余额
   - 确认模型名称正确

4. **配置不生效**
   - 重启应用服务器
   - 检查 `.env` 文件位置

### 📞 支持

- **小爱AI官网**: https://xiaoai.plus
- **API文档**: https://xiaoai.plus/docs
- **技术支持**: 联系小爱AI客服

---

*配置完成后，所有AI智能体将统一使用小爱OpenAI接口！* 🎉 