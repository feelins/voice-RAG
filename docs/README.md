# 项目说明

## 📋 项目简介

这是一个基于 AI 的古籍语音问答助手，展示了如何通过**低代码**方式整合多个 AI 能力：
- 🎤 **ASR（语音识别）**：听懂用户的语音问题
- 📚 **知识库**：理解问题并检索答案
- 🔊 **TTS（语音合成）**：用自然语音回答

## 🗂️ 项目结构

```
final_demo/
├── app.py                      # Flask 后端（200 行）
├── start_demo.py               # 一键启动脚本
├── qwen.key                    # API Key 配置文件（需自行创建）
├── requirements.txt            # Python 依赖
│
├── templates/
│   └── index.html             # 前端页面（568 行）
│
├── static/
│   ├── audio/                 # 音频文件存储
│   └── images/                # 图片资源
│       └── scholar.svg        # 学者形象
│
├── temp_recordings/           # 临时录音文件
│
├── demos/                     # 演示脚本（教学用）
│   ├── 01_asr_demo.py        # ASR 独立演示
│   ├── 02_tts_demo.py        # TTS 独立演示
│   ├── 03_kb_demo.py         # 知识库方案对比
│   └── 04_integration_demo.py # 三模块整合演示
│
├── test_audio/                # 测试音频文件
│
└── docs/                      # 文档
    ├── 课程PPT大纲.md
    ├── 现场演示方案.md
    ├── 学员快速上手指南.md
    └── README.md              # 本文件
```

## 🚀 快速开始

### 1. 环境要求
- Python 3.8 或更高版本
- Windows / macOS / Linux

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置 API Key
在项目根目录创建 `qwen.key` 文件：
```
sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

获取 Key：https://dashscope.console.aliyun.com/

### 4. 启动系统
```bash
# 方式 1：使用启动脚本（推荐）
python start_demo.py

# 方式 2：直接运行
python app.py
```

### 5. 访问系统
打开浏览器：http://localhost:5000

## 🎯 核心功能

### Web 界面
- ✅ 文字提问
- ✅ 语音提问（录音识别）
- ✅ 多音色支持（普通话、粤语）
- ✅ 对话历史记录
- ✅ 示例问题快速输入

### API 端点
- `GET /` - 首页
- `POST /ask` - 文字问答
- `POST /voice_ask` - 语音问答
- `GET /audio/<filename>` - 获取音频文件

## 📖 使用说明

### 文字提问
1. 在右侧文本框输入问题
2. 点击"📝 文字提问"
3. 查看左侧对话记录和语音回答

### 语音提问
1. 点击"🎤 语音提问"
2. 允许浏览器使用麦克风
3. 说出您的问题
4. 点击"⏹️ 停止录音"
5. 系统自动识别并回答

### 切换语音
在右侧"🎙️ 语音选择"下拉框选择不同音色：
- 普通话-女声
- 普通话-男声
- 粤语-女声（优雅）
- 粤语-女声（知性）
- 粤语-男声（欢脱）

## 🔧 自定义知识库

编辑 `app.py` 中的 `QA_DATABASE`（第 69-90 行）：

```python
QA_DATABASE = {
    "您的问题": {
        "answer": "答案内容",
        "audio": "default.mp3"
    },
    # 添加更多问答...
}
```

## 🧪 演示脚本说明

### 01_asr_demo.py
演示语音识别功能：
```bash
cd demos
python 01_asr_demo.py
```

### 02_tts_demo.py
演示语音合成功能，生成不同音色：
```bash
python 02_tts_demo.py
```

### 03_kb_demo.py
对比硬编码 vs LLM 两种知识库方案：
```bash
python 03_kb_demo.py
```

### 04_integration_demo.py
演示完整流程（ASR → 知识库 → TTS）：
```bash
python 04_integration_demo.py
```

## 🎓 教学用途

本项目专为教学设计：
- ✅ 代码简洁（后端 200 行）
- ✅ 逻辑清晰（模块化）
- ✅ 注释详细（易于理解）
- ✅ 渐进式（从单模块到整合）

适合：
- AI 应用开发入门课程
- 语音交互系统教学
- Python Web 开发实战
- 低代码 AI 整合案例

## 🔄 从 Demo 到生产

### 当前版本（Demo）
- 硬编码知识库（5 个问答）
- 单用户模式
- 本地运行

### 生产版本建议
1. **知识库升级**：
   - 接入 FastGPT
   - 支持文档上传
   - 向量检索 + LLM

2. **性能优化**：
   - 答案缓存
   - 流式识别
   - 异步处理

3. **功能扩展**：
   - 用户认证
   - 多轮对话
   - 使用统计

4. **部署优化**：
   - Docker 容器化
   - Nginx 反向代理
   - HTTPS 支持

## 🐛 常见问题

### 问题 1：启动失败
- 检查 Python 版本（≥ 3.8）
- 确认已安装依赖
- 查看是否有端口冲突（5000）

### 问题 2：API 调用失败
- 检查 qwen.key 文件是否存在
- 确认 Key 是否正确
- 检查网络连接

### 问题 3：录音不工作
- 检查麦克风权限
- 使用 Chrome/Edge 浏览器
- 确认使用 HTTPS 或 localhost

### 问题 4：音频不播放
- 检查浏览器自动播放策略
- 手动点击播放按钮
- 确认音频文件已生成

## 📊 技术栈

### 后端
- Flask 3.0+
- DashScope SDK（通义千问）
- Python 3.8+

### 前端
- 原生 HTML/CSS/JavaScript
- Web Audio API（录音）
- Fetch API（异步请求）

### AI 服务
- 通义千问 ASR（Paraformer）
- 通义千问 TTS（CosyVoice）
- 通义千问 LLM（Qwen-Turbo）

## 📄 许可证

本项目用于教学演示，请根据实际需求调整。

## 📞 联系方式

如有问题或建议，请联系：
- [讲师邮箱]
- [课程答疑群]

---

**祝使用愉快！** 🎉
