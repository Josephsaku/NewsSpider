# NewsSpider - 智能新闻爬取与问答系统

一个基于Python的智能新闻爬取系统，专门用于爬取深圳技术大学公文通网站新闻内容，并提供智能问答功能。

## 功能特性

- 📰 自动爬取新闻内容
- 📄 生成PDF文档
- 🤖 基于AI的智能问答
- 🌐 友好的Web界面
- 🔒 安全的配置管理

## 安装指南

### 1. 克隆项目
```bash
git clone <repository-url>
cd NewsSpider
```

### 2. 创建虚拟环境
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# 或 .venv\Scripts\activate  # Windows
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 配置环境
```bash
# 复制配置文件模板
cp config.py.template config.py

# 编辑 config.py 文件，填写您的配置信息
```
你还需要通过Ollama来下载embedding模型，默认使用`quentinz/bge-large-zh-v1.5:latest`
Ollama相关操作请自行查询，这里不展开说明

## 配置说明

在 `config.py` 中配置以下参数：

```python
# DeepSeek API 密钥（必需）
DEEPSEEK_API_KEY = "your_api_key_here"

# 目标网站配置 （必需）
TARGET_BASE_URL = "复制学校内部网网址"
TARGET_PAGE_URL = "复制学校公文通页面的网址"

# 其他可选配置保持默认即可
# 但我建议还是仔细看看需要的配置文件，默认可能会报错
```

### 获取 DeepSeek API 密钥

1. 访问 [DeepSeek官网](https://platform.deepseek.com/)
2. 注册账号并获取API密钥
3. 在配置文件中设置 `DEEPSEEK_API_KEY`

## 使用方法

### 启动系统
```bash
streamlit run spider/main.py
```

### 操作流程

1. **更新新闻**：
   - 输入要爬取的页数（建议1-2页）
   - 点击"更新文件"按钮
   - 等待爬取完成

2. **智能问答**：
   - 在问题输入框中输入查询内容
   - 点击"开始提问"按钮
   - 系统基于PDF内容提供回答