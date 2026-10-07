# VoiceRAG - 会说话的知识库

**Voice-enabled Retrieval Augmented Generation for Ancient Chinese Texts**

一个完整的语音交互问答系统，专注于古籍知识问答场景。支持语音输入、知识库检索、智能问答和多语言语音输出。

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## 🎯 项目特点

- **完整的语音交互链路**：听（ASR）→ 知（RAG）→ 思（LLM）→ 说（TTS）
- **多语言支持**：普通话、粤语等多种语音选择
- **多引擎对比**：阿里云、讯飞等多个语音引擎
- **古籍优化**：专门处理多音字、通假字等古文特殊问题
- **智能匹配**：知识库 + LLM 混合问答策略
- **可扩展**：支持语音克隆和方言训练

---

## 📋 系统架构

```
用户语音输入
    ↓
语音识别 (ASR)
    ↓
问题理解 & 知识检索 (RAG)
    ↓
大模型生成 (LLM)
    ↓
语音合成 (TTS)
    ↓
语音输出 + 文字显示
```

---

## 🚀 快速开始

### 环境要求

- Python 3.10+
- 浏览器支持 Web Audio API

### 安装步骤

1. **克隆仓库**
```bash
git clone git@github.com:feelins/VoiceRAG.git
cd VoiceRAG
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置 API Key**

创建 `qwen.key` 文件，填入你的阿里云 API Key：
```
sk-your-api-key-here
```

或使用环境变量：
```bash
export DASHSCOPE_API_KEY="sk-your-api-key-here"
```

> 获取 API Key：[阿里云通义千问控制台](https://dashscope.console.aliyun.com/)
> 
> 详细配置说明请参考：[API_KEY_TEMPLATE.md](API_KEY_TEMPLATE.md)

4. **启动服务**
```bash
python app.py
```

5. **访问系统**

浏览器打开：http://localhost:5000

---

## 📚 功能特性

### 1. 语音识别（ASR）
- 支持普通话语音输入
- 16kHz 标准音频格式
- 前端自动格式转换

### 2. 知识库检索（RAG）
- 三层匹配策略：精确匹配 → 模糊匹配 → LLM 理解
- 支持 FastGPT 集成
- 本地知识库文件

### 3. 智能问答（LLM）
- 基于通义千问大模型
- 语义理解和问题重写
- 知识库增强生成

### 4. 语音合成（TTS）
- 多语音选择：普通话、粤语
- 多引擎支持：阿里云、讯飞
- 古文优化：多音字、通假字处理

### 5. 语音克隆（可选）
- 支持个性化语音训练
- 方言模型训练（如潮汕话）
- 使用 GPT-SoVITS 或 CosyVoice

---

## 📖 使用说明

### 基础使用

1. 打开网页界面
2. 选择语音类型（普通话/粤语）
3. 点击"🎤 语音提问"按钮
4. 对着麦克风说出问题
5. 点击"停止录音"
6. 等待系统识别和生成答案
7. 自动播放语音回答

### 文字输入

也可以直接在输入框中输入问题，点击"提问"按钮。

### 扩展知识库

编辑 `古籍知识库.txt` 文件，添加新的问答对：

```
问题：学而时习之是什么意思？
答案：「学而时习之」出自《论语》学而篇...
出处：《论语·学而第一》
```

---

## 📂 项目结构

```
VoiceRAG/
├── app.py                              # Flask 主程序
├── requirements.txt                    # Python 依赖
├── .gitignore                          # Git 忽略配置
├── API_KEY_TEMPLATE.md                 # API Key 配置模板
├── README.md                           # 本文件
│
├── templates/
│   └── index.html                      # 前端页面
│
├── static/
│   ├── audio/                          # 生成的音频文件
│   └── images/
│       └── scholar.svg                 # 学者图标
│
├── temp_recordings/                    # 临时录音文件
│
├── 古籍知识库.txt                       # 知识库数据
│
└── docs/                               # 文档
    ├── 语音交互系统文档.md               # 技术文档
    ├── 课堂演示Prompt.md                # 教学指南
    ├── 课程讲义纲要-会说话的人文智能体.md # 完整课程纲要
    ├── 古籍语音合成常见问题.md           # 坑点总结
    ├── 语音克隆与方言训练.md             # 训练教程
    ├── GPT-SoVITS多语种训练总结.md       # 多语种训练
    ├── FastGPT配置详细步骤.md           # FastGPT 配置
    └── 完整语音交互实现方案.md           # 实现方案
```

---

## 🛠️ 技术栈

**后端**
- Flask 3.0+ - Web 框架
- DashScope SDK - 阿里云语音服务
- Python 3.10+

**前端**
- 原生 JavaScript
- Web Audio API - 音频处理
- Fetch API - 网络请求

**AI 服务**
- 阿里云通义千问 - 语音识别、语音合成、大模型
- FastGPT（可选） - 知识库管理

---

## 📊 性能指标

- **端到端延迟**：5-10 秒
- **语音识别准确率**：>90%（普通话）
- **知识库匹配准确率**：>85%
- **语音合成自然度**：MOS >4.0

---

## 🎓 文档和教程

### 快速入门
- [API Key 配置指南](API_KEY_TEMPLATE.md)
- [快速开始教程](docs/语音交互系统文档.md)

### 进阶指南
- [古籍语音合成常见问题](docs/古籍语音合成常见问题.md)
- [FastGPT 知识库配置](docs/FastGPT配置详细步骤.md)
- [完整实现方案](docs/完整语音交互实现方案.md)

### 高级教程
- [语音克隆与方言训练](docs/语音克隆与方言训练.md)
- [GPT-SoVITS 多语种训练](docs/GPT-SoVITS多语种训练总结.md)

### 课程材料
- [完整课程讲义纲要](docs/课程讲义纲要-会说话的人文智能体.md)
- [课堂演示 Prompt](docs/课堂演示Prompt.md)

---

## 🔧 常见问题

### Q: 麦克风无法访问？
A: 检查浏览器权限设置，确保允许网站访问麦克风。HTTPS 环境下才能访问麦克风。

### Q: API 调用失败？
A: 
1. 检查 `qwen.key` 文件是否存在且格式正确
2. 检查 API Key 是否有效
3. 检查账户余额是否充足

### Q: 语音识别不准确？
A: 
1. 确保环境安静
2. 说话清晰，不要太快
3. 使用高质量麦克风
4. 检查网络连接

### Q: 找不到答案？
A: 
1. 检查问题是否在知识库范围内
2. 尝试换一种问法
3. 扩展知识库内容

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 开发指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

---

## 📝 待办事项

- [ ] 添加更多语音引擎支持（百度、腾讯）
- [ ] 实现流式 TTS
- [ ] 本地模型部署方案
- [ ] Docker 容器化
- [ ] 多轮对话支持
- [ ] 用户认证和权限管理
- [ ] 音频缓存优化
- [ ] 移动端适配

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

- [阿里云通义千问](https://tongyi.aliyun.com/) - 语音和大模型服务
- [FastGPT](https://github.com/labring/FastGPT) - 知识库管理工具
- [CosyVoice](https://github.com/FunAudioLLM/CosyVoice) - 开源语音合成
- [GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS) - 语音克隆工具

---

## 📧 联系方式

- **项目**: [https://github.com/feelins/VoiceRAG](https://github.com/feelins/VoiceRAG)
- **Issues**: [https://github.com/feelins/VoiceRAG/issues](https://github.com/feelins/VoiceRAG/issues)

---

## 🌟 Star History

如果这个项目对你有帮助，欢迎 Star ⭐

---

**最后更新**: 2026-10-07
