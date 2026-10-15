"""
演示 2：语音合成（TTS）独立演示
"""

import dashscope
from dashscope.audio.tts_v2 import SpeechSynthesizer
import os

API_KEY = "在这里粘贴您的API Key"  # 使用同一个 Key
dashscope.api_key = API_KEY

def test_tts(text, voice_id='longxiaochun', output_file='output.mp3'):
    """测试语音合成"""
    print(f"\n正在合成: {text}")
    print(f"使用音色: {voice_id}")
    print("-" * 50)

    synthesizer = SpeechSynthesizer(
        model='cosyvoice-v1',
        voice=voice_id
    )

    audio_data = synthesizer.call(text)

    if isinstance(audio_data, bytes) and len(audio_data) > 0:
        with open(output_file, 'wb') as f:
            f.write(audio_data)

        file_size = len(audio_data) / 1024  # KB
        print(f"✅ 合成成功！")
        print(f"文件大小: {file_size:.1f} KB")
        print(f"保存位置: {output_file}")

        # 自动播放
        try:
            os.system(f'start {output_file}')  # Windows
            # os.system(f'open {output_file}')  # macOS
            # os.system(f'xdg-open {output_file}')  # Linux
        except:
            print("提示：请手动打开文件播放")

        return True
    else:
        print(f"❌ 合成失败")
        return False

if __name__ == '__main__':
    print("=" * 50)
    print("TTS (语音合成) 演示")
    print("=" * 50)

    # 测试文本
    text = "学而时习之，不亦说乎？有朋自远方来，不亦乐乎？"

    # 测试不同音色
    voices = {
        'longxiaochun': '普通话-女声',
        'longyuan': '普通话-男声',
        'longjiaxin_v3': '粤语-女声（优雅）',
    }

    print(f"\n测试文本: {text}")
    print(f"将生成 {len(voices)} 个不同音色的音频\n")

    for voice_id, voice_name in voices.items():
        print(f"\n【{voice_name}】")
        filename = f'output_{voice_id}.mp3'

        try:
            # 根据音色选择模型
            if 'v3' in voice_id:
                model = 'cosyvoice-v3-flash'
            else:
                model = 'cosyvoice-v1'

            synthesizer = SpeechSynthesizer(model=model, voice=voice_id)
            audio = synthesizer.call(text)

            if isinstance(audio, bytes):
                with open(filename, 'wb') as f:
                    f.write(audio)
                print(f"✅ 生成成功: {filename}")
            else:
                print(f"❌ 生成失败")
        except Exception as e:
            print(f"❌ 错误: {e}")

    print("\n" + "=" * 50)
    print("演示完成！请播放音频文件对比效果 🎵")
    print("=" * 50)
