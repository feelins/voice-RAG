# API 配置文件模板

## 使用说明

1. 复制本文件并重命名为相应的 `.key` 文件
2. 填入你的实际 API Key
3. 确保 `.key` 文件已被 `.gitignore` 忽略

---

## qwen.key

阿里云通义千问 API Key

```
sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

申请地址：https://dashscope.console.aliyun.com/

---

## fastgpt.key（可选）

FastGPT API Key（如果使用 FastGPT API）

```
fastgpt-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## xunfei.key（可选）

讯飞开放平台配置（如果使用讯飞语音）

格式：
```json
{
  "APPID": "xxxxxxxx",
  "APIKey": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "APISecret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
}
```

申请地址：https://www.xfyun.cn/

---

## 环境变量方式（推荐）

也可以使用环境变量方式配置：

```bash
export DASHSCOPE_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export XUNFEI_APPID="xxxxxxxx"
export XUNFEI_API_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export XUNFEI_API_SECRET="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

或创建 `.env` 文件：

```
DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
XUNFEI_APPID=xxxxxxxx
XUNFEI_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
XUNFEI_API_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
