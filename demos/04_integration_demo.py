"""
演示 4：三模块整合（命令行版）
展示：ASR → 知识库 → TTS 的完整流程
"""

import dashscope
from dashscope.audio.asr import Recognition
from dashscope.audio.tts_v2 import SpeechSynthesizer
import os
import time

API_KEY = "在这里粘贴您的API Key"
dashscope.api_key = API_KEY

# ===== 知识库（简化版）=====
QA_DATABASE = {
    "学而时习之是什么意思": "「学而时习之」出自《论语》学而篇。意思是：学习了知识，并且时常温习实践，不也是很愉快的事吗？这体现了孔子强调的学习方法——学习与实践相结合。",
    "孔子的弟子有谁": "孔子有众多弟子，其中最著名的是「孔门十哲」。包括：颜回（德行第一）、子贡（言语第一）、子路（政事第一）、曾参（传承儒学）等。",
    "什么是仁": "「仁」是孔子思想的核心。简单说，「仁」就是爱人。孔子说「己所不欲，勿施于人」，这是仁的基本原则。仁包含仁爱、仁德、仁政等多个层面。",
}

# ===== 模块 1: ASR =====
def asr(audio_file):
    """语音识别模块"""
    print("🎤 正在识别语音...")

    try:
        recognizer = Recognition(
            model='paraformer-realtime-v2',
            format='wav',
            sample_rate=16000
        )
        result = recognizer.call(audio_file)

        if result.status_code == 200:
            text = result.output.get('text', '')
            print(f"✅ 识别成功: {text}")
            return text
        else:
            print(f"❌ 识别失败: {result.message}")
            return None
    except Exception as e:
        print(f"❌ 识别异常: {e}")
        return None

# ===== 模块 2: 知识库 =====
def kb(question):
    """知识库查询模块"""
    print("📚 正在查询知识库...")
    time.sleep(0.5)  # 模拟查询时间

    # 去除问号
    q = question.strip().replace("？", "").replace("?", "")

    # 精确匹配
    if q in QA_DATABASE:
        answer = QA_DATABASE[q]
        print(f"✅ 找到答案")
        return answer

    # 模糊匹配
    for key, value in QA_DATABASE.items():
        if key in q or q in key:
            print(f"✅ 找到相似答案")
            return value

    # 未找到
    answer = "抱歉，我暂时无法回答这个问题。您可以询问关于《论语》、孔子等古籍的问题。"
    print("⚠️  未找到答案，返回默认回复")
    return answer

# ===== 模块 3: TTS =====
def tts(text, output='answer.mp3'):
    """语音合成模块"""
    print("🔊 正在合成语音...")

    try:
        synthesizer = SpeechSynthesizer(
            model='cosyvoice-v1',
            voice='longxiaochun'
        )
        audio_data = synthesizer.call(text)

        if isinstance(audio_data, bytes) and len(audio_data) > 0:
            with open(output, 'wb') as f:
                f.write(audio_data)
            print(f"✅ 语音合成成功: {output}")
            return output
        else:
            print("❌ 合成失败")
            return None
    except Exception as e:
        print(f"❌ 合成异常: {e}")
        return None

# ===== 完整流程 =====
def main(audio_file):
    """完整问答流程"""
    print("\n" + "=" * 60)
    print("古籍语音问答系统 - 命令行演示版")
    print("=" * 60)

    # 检查文件
    if not os.path.exists(audio_file):
        print(f"\n❌ 音频文件不存在: {audio_file}")
        return

    print(f"\n输入音频: {audio_file}\n")

    # 步骤 1: ASR（语音识别）
    print("【步骤 1/3】语音识别")
    print("-" * 60)
    question = asr(audio_file)
    if not question:
        print("\n❌ 识别失败，流程中止")
        return

    # 步骤 2: 知识库查询
    print("\n【步骤 2/3】知识库查询")
    print("-" * 60)
    answer = kb(question)
    print(f"\n答案内容:\n{answer}")

    # 步骤 3: TTS（语音合成）
    print("\n【步骤 3/3】语音合成")
    print("-" * 60)
    audio_output = tts(answer)

    if audio_output:
        print("\n✅ 流程完成！正在播放语音...")
        try:
            os.system(f'start {audio_output}')  # Windows
        except:
            print("提示：请手动播放 answer.mp3")

    print("\n" + "=" * 60)
    print("演示结束 🎉")
    print("=" * 60)
    print("\n这就是完整系统的核心逻辑！")
    print("加上 Flask 后端 + HTML 前端 = 完整的 Web 应用\n")

if __name__ == '__main__':
    # 使用测试音频
    test_audio = '../test_audio/question1.wav'

    # 如果没有测试音频，提示创建
    if not os.path.exists(test_audio):
        print("\n⚠️  测试音频不存在")
        print("请准备一个 WAV 格式的音频文件（16kHz，单声道）")
        print(f"保存到: {test_audio}")
        print("\n或者修改脚本中的 test_audio 变量指向您的音频文件\n")
    else:
        main(test_audio)
