# FastGPT 语音交互系统 - 快速搭建指南

> **目标**：1-2 天搭建一个完整的古籍语音问答系统
> **成本**：完全免费
> **难度**：⭐⭐（需要会用 Docker）

---

## 系统效果

学员对着麦克风说："学而时习之是什么意思？"
→ 系统检索古籍知识库
→ 生成回答并朗读出来
→ 屏幕显示原文出处

**差异化亮点**：古文 TTS 念对（多音字、生僻字、断句）

---

## 快速开始（三步走）

### 步骤 1：部署 FastGPT（30分钟）

```bash
# 1. 确保已安装 Docker
docker --version

# 2. 克隆 FastGPT
git clone https://github.com/labring/FastGPT.git
cd FastGPT/projects/app

# 3. 启动（使用官方快速启动配置）
bash quick-start.sh

# 4. 访问
# 浏览器打开 http://localhost:3000
# 默认账号：root
# 默认密码：1234（首次登录会要求修改）
```

**如果遇到问题**，查看 [docs/部署问题排查.md](docs/部署问题排查.md)

### 步骤 2：配置模型 API（10分钟）

**推荐 SiliconFlow（免费额度多）**：

1. 注册 https://cloud.siliconflow.cn/
2. 获取 API Key（免费送 2000 万 tokens）
3. FastGPT 里配置：
```
系统设置 → 模型管理 → 添加模型
- 名称：Qwen2.5-7B
- 基础模型：gpt-4
- API 地址：https://api.siliconflow.cn/v1
- API Key：sk-xxxxx
- 模型：Qwen/Qwen2.5-7B-Instruct
```

详见 [docs/模型配置指南.md](docs/模型配置指南.md)

### 步骤 3：导入知识库（15分钟）

```bash
# 使用准备好的古籍语料
cd E:\002_Personal_Works\projects\20260908-西安培训课\demo\fastgpt
# 语料在 data/corpus/ 目录
```

FastGPT 操作：
```
知识库 → 创建知识库 → 上传文档
- 上传 data/corpus/古籍语料合集.txt
- 分段长度：256
- 索引模式：高质量
```

详见 [docs/知识库配置.md](docs/知识库配置.md)

---

## 目录结构

```
fastgpt/
├── README.md                    # 本文件
├── data/                        # 数据文件
│   ├── corpus/                  # 古籍语料
│   │   ├── 古籍语料合集.txt
│   │   ├── 论语选段.txt
│   │   ├── 史记选段.txt
│   │   └── 资治通鉴选段.txt
│   └── demos/                   # TTS 对比音频
│       ├── 01_说字_原版.mp3
│       ├── 01_说字_优化.mp3
│       └── ... (5组对比)
├── tools/                       # 工具脚本
│   ├── guwen_tts_frontend.py   # 古文 TTS 前端处理
│   ├── generate_demos.py       # 生成对比音频
│   └── test_api.py             # API 测试脚本
├── workflow/                    # FastGPT 工作流配置
│   ├── 古籍问答.json            # 可导入的工作流
│   └── workflow_screenshot.png  # 工作流截图
├── docs/                        # 详细文档
│   ├── 部署问题排查.md
│   ├── 模型配置指南.md
│   ├── 知识库配置.md
│   ├── 工作流搭建.md
│   └── 语音接入.md
└── 学员交付包/                  # 课后给学员的材料
    ├── 快速上手指南.pdf
    ├── 常见问题.md
    └── 资源清单.md
```

---

## 核心功能

### 1. 完整的问答系统
- 语音/文字输入
- 知识库检索
- 拒答机制（无据不答）
- 引用溯源

### 2. 古文 TTS 优化
- 多音字消歧（"说" → yuè）
- 生僻字处理（"姥" → mǔ）
- 断句优化

### 3. 低代码搭建
- 拖拽式工作流
- 无需写代码（核心功能）
- 可视化调试

---

## 快速验证（5分钟测试）

部署完成后，测试这 5 个问题：

1. ✅ **正常问答**："学而时习之什么意思？"
   - 应该回答并引用《论语》

2. ✅ **拒答测试**："红楼梦第五回讲什么？"
   - 应该回复"未见记载"（语料外）

3. ✅ **多轮对话**："那有朋自远方来呢？"
   - 应该联系上文回答

4. ✅ **专有名词**："孔子的弟子有谁？"
   - 应该准确识别人名

5. ✅ **古文朗读**：点击"朗读"按钮
   - 播放答案音频

---

## 下一步

- [ ] 完成部署和测试
- [ ] 准备 TTS 对比音频 → [tools/generate_demos.py](tools/generate_demos.py)
- [ ] 搭建工作流 → [docs/工作流搭建.md](docs/工作流搭建.md)
- [ ] 接入语音 → [docs/语音接入.md](docs/语音接入.md)
- [ ] 准备课件

---

## 支持

- FastGPT 官方文档：https://doc.fastgpt.in/
- 问题反馈：提交 Issue
- 微信群：（课程群二维码）
