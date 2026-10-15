"""
演示 3：两种知识库方案对比
"""

import dashscope
from dashscope import Generation

API_KEY = "在这里粘贴您的API Key"
dashscope.api_key = API_KEY

# ===== 方案 1：硬编码（最简单）=====
QA_DATABASE = {
    "学而时习之是什么意思": "「学而时习之」出自《论语》学而篇。意思是：学习了知识，并且时常温习实践，不也是很愉快的事吗？",
    "孔子的弟子有谁": "孔子有众多弟子，其中最著名的是「孔门十哲」。包括：颜回（德行第一）、子贡、子路、曾参等。",
    "什么是仁": "「仁」是孔子思想的核心。简单说，「仁」就是爱人。孔子说「己所不欲，勿施于人」，这是仁的基本原则。",
}

def find_answer_v1(question):
    """方案1：字典查询（硬编码）"""
    # 去除问号
    q = question.strip().replace("？", "").replace("?", "")

    # 精确匹配
    if q in QA_DATABASE:
        return QA_DATABASE[q]

    # 模糊匹配
    for key, value in QA_DATABASE.items():
        if key in q or q in key:
            return value

    return "抱歉，我不知道这个问题"

# ===== 方案 2：使用 LLM（智能）=====
def find_answer_v2(question):
    """方案2：调用通义千问"""

    # 构建知识库上下文
    kb_text = "\n".join([f"问：{k}\n答：{v}" for k, v in QA_DATABASE.items()])

    prompt = f"""你是一位古籍专家，请根据知识库回答用户问题。

知识库：
{kb_text}

用户问题：{question}

注意：
1. 如果问题与知识库相关，基于知识库回答
2. 如果知识库没有相关信息，回答"抱歉，我暂时无法回答这个问题"
3. 直接给出答案，不要重复问题

请回答："""

    try:
        response = Generation.call(
            model='qwen-turbo',
            prompt=prompt,
            max_tokens=300
        )

        if response.status_code == 200:
            return response.output.text.strip()
        else:
            return f"查询失败: {response.message}"
    except Exception as e:
        return f"调用失败: {e}"

# ===== 对比测试 =====
if __name__ == '__main__':
    print("=" * 60)
    print("知识库方案对比演示")
    print("=" * 60)

    # 测试问题
    test_questions = [
        "学而时习之是什么意思",          # 精确匹配
        "学而时习之讲的是啥",            # 模糊表达
        "孔子认为学习要怎么做",          # 需要理解
        "孔子有哪些学生",                # 同义表达
        "红楼梦讲什么",                  # 超出知识库
    ]

    for i, question in enumerate(test_questions, 1):
        print(f"\n【测试 {i}】问题: {question}")
        print("-" * 60)

        # 方案1：硬编码
        answer1 = find_answer_v1(question)
        print(f"方案1（硬编码）:\n{answer1}\n")

        # 方案2：LLM
        answer2 = find_answer_v2(question)
        print(f"方案2（LLM智能）:\n{answer2}")

        print("=" * 60)

    print("\n总结：")
    print("✅ 方案1（硬编码）：快速、可控，但只能精确匹配")
    print("✅ 方案2（LLM）：灵活、智能，能理解多种表达")
    print("✅ 生产环境推荐：FastGPT（可视化 + 向量检索 + LLM）")
