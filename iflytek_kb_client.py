# -*- coding: utf-8 -*-
"""
讯飞星辰知识库客户端 - 修正版
"""
import requests
import json
import hmac
import hashlib
import base64
import time
from datetime import datetime


class IflytekKBClient:
    """讯飞星辰知识库客户端"""

    def __init__(self, api_key, api_secret, app_id, flow_id):
        self.api_key = api_key
        self.api_secret = api_secret
        self.app_id = app_id
        self.flow_id = flow_id
        self.base_url = "https://xingchen-api.xf-yun.com/workflow/v1/chat/completions"

    def _generate_signature(self, method, path, timestamp, host):
        """
        生成 HMAC 签名

        Args:
            method: HTTP方法 (POST)
            path: 请求路径
            timestamp: 时间戳
            host: 主机名

        Returns:
            str: Base64编码的签名
        """
        # 构造待签名字符串（包含 host）
        string_to_sign = f"host: {host}\ndate: {timestamp}\n{method} {path} HTTP/1.1"

        # 使用 HMAC-SHA256 签名
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            string_to_sign.encode('utf-8'),
            hashlib.sha256
        ).digest()

        # Base64 编码
        return base64.b64encode(signature).decode('utf-8')

    def search(self, query):
        """
        检索知识库

        Args:
            query: 查询问题

        Returns:
            str: 回答内容
        """
        # 生成时间戳（RFC1123格式）
        from email.utils import formatdate
        timestamp = formatdate(timeval=None, localtime=False, usegmt=True)

        # 主机名
        host = "xingchen-api.xf-yun.com"
        path = "/workflow/v1/chat/completions"

        # 生成签名
        signature = self._generate_signature("POST", path, timestamp, host)

        headers = {
            "Content-Type": "application/json",
            "Host": host,
            "Date": timestamp,
            "Authorization": f'api_key="{self.api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature}"'
        }

        data = {
            "flow_id": self.flow_id,
            "parameters": {"AGENT_USER_INPUT": query},
            "messages": [
                {
                    "role": "user",
                    "content": query
                }
            ],
            "stream": False
        }

        try:
            print(f"请求URL: {self.base_url}")
            print(f"请求数据: {json.dumps(data, ensure_ascii=False, indent=2)}")

            response = requests.post(
                self.base_url,
                headers=headers,
                json=data,
                timeout=30
            )

            print(f"响应状态码: {response.status_code}")
            print(f"响应内容: {response.text}")

            if response.status_code == 200:
                result = response.json()

                # 解析返回结果
                if result.get('code') == 0:
                    choices = result.get('choices', [])
                    if choices:
                        # 非流式响应内容可能在 message 或 delta 字段中
                        message = choices[0].get('message') or choices[0].get('delta') or {}
                        content = message.get('content', '')
                        if content:
                            return content
                        print(f"知识库返回为空")
                        return None
                    else:
                        print(f"知识库返回为空")
                        return None
                else:
                    error_msg = result.get('message', '未知错误')
                    print(f"知识库API返回错误：{error_msg}")
                    return None
            else:
                print(f"知识库API调用失败，状态码：{response.status_code}")
                print(f"响应内容：{response.text}")
                return None

        except Exception as e:
            print(f"知识库API调用异常：{str(e)}")
            import traceback
            traceback.print_exc()
            return None


# 加载配置
def load_iflytek_config():
    """从iflytek.key文件加载配置"""
    import os
    key_file = os.path.join('docs', 'iflytek.key')

    if not os.path.exists(key_file):
        raise Exception(f"未找到配置文件：{key_file}")

    with open(key_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 解析配置
    config = {}
    lines = content.split('\n')

    for i, line in enumerate(lines):
        if 'APPID' in line and ':' in line:
            config['app_id'] = lines[i+1].strip() if i+1 < len(lines) else line.split(':')[-1].strip()
        elif 'API Secret' in line and ('：' in line or ':' in line):
            # API Secret 值在下一行
            config['api_secret'] = lines[i+1].strip() if i+1 < len(lines) else line.split(':')[-1].strip()
        elif 'API Key' in line and ('：' in line or ':' in line):
            # API Key 值在下一行
            config['api_key'] = lines[i+1].strip() if i+1 < len(lines) else ''
        elif 'API Flowid' in line:
            config['flow_id'] = lines[i+1].strip() if i+1 < len(lines) else line.split()[-1].strip()

    print("加载的配置:")
    print(f"  app_id: {config.get('app_id')}")
    print(f"  api_key: {config.get('api_key')}")
    print(f"  api_secret: {config.get('api_secret')[:10]}...")
    print(f"  flow_id: {config.get('flow_id')}")

    return config


# 全局实例
_kb_client = None

def get_kb_client():
    """获取知识库客户端单例"""
    global _kb_client
    if _kb_client is None:
        config = load_iflytek_config()
        _kb_client = IflytekKBClient(
            api_key=config['api_key'],
            api_secret=config['api_secret'],
            app_id=config['app_id'],
            flow_id=config['flow_id']
        )
    return _kb_client


def search_knowledge_base(query):
    """
    检索知识库（简化接口）

    Args:
        query: 查询问题

    Returns:
        str: 回答内容，如果失败返回None
    """
    client = get_kb_client()
    return client.search(query)


# 测试代码
if __name__ == "__main__":
    print("=" * 50)
    print("测试讯飞知识库调用")
    print("=" * 50)

    # 测试知识库检索
    test_query = "学而时习之是什么意思"
    result = search_knowledge_base(test_query)

    print("\n" + "=" * 50)
    if result:
        print(f"✓ 查询成功")
        print(f"问题：{test_query}")
        print(f"回答：{result}")
    else:
        print("✗ 知识库检索失败")
    print("=" * 50)
