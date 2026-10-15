"""
演示 1：语音识别（ASR）独立演示
展示如何：注册账号 → 获取 Key → 调用 API → 看到结果
"""

# ===== 步骤 1：配置 API Key =====
# 打开：https://dashscope.console.aliyun.com/
# 注册 → 开通服务 → 复制 API Key
API_KEY = "在这里粘贴您的API Key"  # 现场填入

# ===== 步骤 2：安装依赖 =====
# pip install dashscope

# ===== 步骤 3：最简调用 =====
import dashscope
from dashscope.audio.asr import Recognition

dashscope.api_key = API_KEY

def test_asr(audio_file):
    """测试语音识别"""
    print(f"\n正在识别: {audio_file}")
    print("-" * 50)

    recognizer = Recognition(
        model='paraformer-realtime-v2',
        format='wav',
        sample_rate=16000
    )

    result = recognizer.call(audio_file)

    if result.status_code == 200:
        text = result.output.get('text', '')
        print(f"✅ 识别成功！")
        print(f"识别结果: {text}")
        return text
    else:
        print(f"❌ 识别失败: {result.message}")
        return None

# ===== 步骤 4：运行测试 =====
if __name__ == '__main__':
    print("=" * 50)
    print("ASR (语音识别) 演示")
    print("=" * 50)

    # 使用预先录制的测试音频
    test_audio = '../test_audio/question1.wav'

    # 检查文件是否存在
    import os
    if not os.path.exists(test_audio):
        print(f"\n⚠️  测试音频不存在: {test_audio}")
        print("请先准备测试音频文件")
        print("\n提示：可以用手机录音，导出为 WAV 格式")
    else:
        result = test_asr(test_audio)

        if result:
            print("\n" + "=" * 50)
            print("演示完成！ASR 就是这么简单 🎉")
            print("=" * 50)
