"""
古籍语音问答助手 - 集成语音识别版本（使用讯飞知识库）
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import time
import dashscope
from dashscope.audio.asr import Recognition
from dashscope.audio.tts_v2 import SpeechSynthesizer
from iflytek_kb_client import search_knowledge_base

app = Flask(__name__)

# 设置阿里云 API Key
def load_api_key():
    """从 qwen.key 文件读取 API Key"""
    key_file = 'qwen.key'
    if os.path.exists(key_file):
        with open(key_file, 'r', encoding='utf-8') as f:
            return f.read().strip()
    else:
        api_key = os.environ.get('DASHSCOPE_API_KEY')
        if api_key:
            return api_key
        else:
            raise Exception("未找到 API Key！请创建 qwen.key 文件或设置 DASHSCOPE_API_KEY 环境变量")

DASHSCOPE_API_KEY = load_api_key()
dashscope.api_key = DASHSCOPE_API_KEY

# 创建临时目录存储录音
UPLOAD_FOLDER = 'temp_recordings'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 支持的语音配置
VOICE_OPTIONS = {
    'mandarin_female': {
        'name': '普通话-女声',
        'voice': 'longxiaochun',
        'model': 'cosyvoice-v1'
    },
    'mandarin_male': {
        'name': '普通话-男声',
        'voice': 'longyuan',
        'model': 'cosyvoice-v1'
    },
    'cantonese': {
        'name': '粤语',
        'voice': 'longwan',
        'model': 'cosyvoice-v1'
    },
    'taiwanese': {
        'name': '台湾话',
        'voice': 'longjing',
        'model': 'cosyvoice-v1'
    },
    'english': {
        'name': '英语',
        'voice': 'longxiaoxia',
        'model': 'cosyvoice-v1'
    }
}

# ===== 语音识别函数 =====
def recognize_speech(audio_file_path):
    """
    使用阿里云语音识别
    :param audio_file_path: WAV 音频文件路径
    :return: 识别的文本，如果失败返回 None
    """
    try:
        print(f"开始识别音频: {audio_file_path}")

        # 创建识别器
        recognizer = Recognition(
            model='paraformer-realtime-v2',
            format='wav',
            sample_rate=16000,
            callback=None
        )

        # 调用识别
        result = recognizer.call(audio_file_path)

        if result.status_code == 200:
            # 解析结果
            text = result.output.get('text', '')
            print(f"识别结果: {text}")
            return text
        else:
            print(f"识别失败: {result.message}")
            return None

    except Exception as e:
        print(f"语音识别异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

# ===== 语音合成函数 =====
def synthesize_speech(text, voice_type='mandarin_female'):
    """
    使用阿里云语音合成
    :param text: 要合成的文本
    :param voice_type: 语音类型（从 VOICE_OPTIONS 中选择）
    :return: 合成的音频文件路径，如果失败返回 None
    """
    try:
        print(f"开始合成语音: {text[:50]}...")

        # 获取语音配置
        voice_config = VOICE_OPTIONS.get(voice_type, VOICE_OPTIONS['mandarin_female'])

        # 生成唯一的文件名
        output_filename = f"tts_{int(time.time() * 1000)}.mp3"
        output_path = os.path.join('static', 'audio', output_filename)

        # 确保目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # 创建合成器
        synthesizer = SpeechSynthesizer(
            model=voice_config['model'],
            voice=voice_config['voice']
        )

        # 调用合成
        audio = synthesizer.call(text)

        if audio:
            # 保存音频文件
            with open(output_path, 'wb') as f:
                f.write(audio)

            print(f"语音合成成功: {output_filename}")
            return output_filename
        else:
            print("语音合成失败: 未获取到音频数据")
            return None

    except Exception as e:
        print(f"语音合成异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

# ===== 知识库查询函数 =====
def find_answer(question):
    """
    使用讯飞星辰知识库获取答案

    :param question: 用户问题
    :return: 字典 {'answer': str, 'audio': None}
    """
    print(f"\n========== 问答处理 ==========")
    print(f"问题: {question}")

    try:
        print(f"→ 调用讯飞知识库查询...")
        answer = search_knowledge_base(question)

        if answer:
            print(f"✓ 知识库返回答案")
            return {
                'answer': answer,
                'audio': None  # 不使用预录音频
            }
        else:
            print(f"✗ 知识库未返回答案，使用默认回复")
            return {
                'answer': "抱歉，我暂时无法回答这个问题。您可以询问关于《论语》、孔子、《诗经》等古籍的问题。",
                'audio': None
            }

    except Exception as e:
        print(f"知识库查询异常：{str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'answer': "抱歉，系统出现问题，请稍后再试。",
            'audio': None
        }

# ===== Flask 路由 =====
@app.route('/')
def index():
    """首页"""
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    """处理文字问答"""
    data = request.json
    question = data.get('question', '')

    if not question:
        return jsonify({'error': '请输入问题'}), 400

    print(f"收到问题: {question}")

    # 模拟思考时间
    time.sleep(0.5)

    # 查找答案
    result = find_answer(question)

    return jsonify({
        'answer': result['answer'],
        'audio_file': result['audio']
    })

@app.route('/voice_ask', methods=['POST'])
def voice_ask():
    """处理语音问答"""
    try:
        # 获取上传的音频文件
        if 'audio' not in request.files:
            return jsonify({'error': '未找到音频文件'}), 400

        audio_file = request.files['audio']
        voice_type = request.form.get('voice_type', 'mandarin_female')

        if audio_file.filename == '':
            return jsonify({'error': '未选择文件'}), 400

        # 保存音频文件
        timestamp = int(time.time() * 1000)
        filename = f"recording_{timestamp}.wav"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        audio_file.save(filepath)

        print(f"音频文件已保存: {filepath}")

        # 1. 语音识别
        question = recognize_speech(filepath)

        if not question:
            return jsonify({'error': '语音识别失败'}), 500

        print(f"识别到问题: {question}")

        # 2. 获取答案
        result = find_answer(question)
        answer_text = result['answer']

        # 3. 语音合成
        audio_filename = synthesize_speech(answer_text, voice_type)

        # 4. 清理临时文件
        try:
            os.remove(filepath)
        except:
            pass

        return jsonify({
            'question': question,
            'answer': answer_text,
            'audio_file': audio_filename
        })

    except Exception as e:
        print(f"语音问答异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/audio/<filename>')
def get_audio(filename):
    """返回音频文件"""
    audio_path = os.path.join('static', 'audio', filename)

    if os.path.exists(audio_path):
        return send_file(audio_path, mimetype='audio/mpeg')
    else:
        return "音频未找到", 404

@app.route('/get_voices')
def get_voices():
    """获取支持的语音列表"""
    voices = [{'id': k, 'name': v['name']} for k, v in VOICE_OPTIONS.items()]
    return jsonify({'voices': voices})

if __name__ == '__main__':
    print("=" * 50)
    print("古籍语音问答助手 (使用讯飞知识库)")
    print("=" * 50)
    print("访问: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)
