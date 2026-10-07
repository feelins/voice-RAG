"""
古籍语音问答助手 - 集成语音识别版本
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import time
import dashscope
from dashscope.audio.asr import Recognition
from dashscope.audio.tts_v2 import SpeechSynthesizer
from dashscope import Generation

app = Flask(__name__)

# 设置阿里云 API Key
# 从文件读取 API Key
def load_api_key():
    """从 qwen.key 文件读取 API Key"""
    key_file = 'qwen.key'
    if os.path.exists(key_file):
        with open(key_file, 'r', encoding='utf-8') as f:
            return f.read().strip()
    else:
        # 尝试从环境变量读取
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
    'cantonese_female': {
        'name': '粤语-女声（优雅）',
        'voice': 'longjiaxin_v3',
        'model': 'cosyvoice-v3-flash'
    },
    'cantonese_female2': {
        'name': '粤语-女声（知性）',
        'voice': 'longjiayi_v3',
        'model': 'cosyvoice-v3-flash'
    },
    'cantonese_male': {
        'name': '粤语-男声（欢脱）',
        'voice': 'longanyue_v3',
        'model': 'cosyvoice-v3-flash'
    }
}

# ===== 固定问答库 =====
QA_DATABASE = {
    "学而时习之是什么意思": {
        "answer": "「学而时习之」出自《论语》学而篇。「学」是学习，「时」是时常，「习」是温习实践。这句话的意思是：学习了知识，并且时常温习实践，不也是很愉快的事吗？这体现了孔子强调的学习方法——学习与实践相结合。",
        "audio": "answer1.mp3"
    },
    "孔子的弟子有谁": {
        "answer": "孔子有众多弟子，其中最著名的是「孔门十哲」。包括：颜回（德行第一）、子贡（言语第一）、子路（政事第一）、曾参（传承儒学）、子张、子夏、冉有、仲弓等。其中颜回最受孔子器重，被称为「复圣」。",
        "audio": "answer2.mp3"
    },
    "什么是仁": {
        "answer": "「仁」是孔子思想的核心。简单说，「仁」就是爱人。孔子说「己所不欲，勿施于人」，这是仁的基本原则。仁包含仁爱、仁德、仁政等多个层面，要求人们关爱他人，推己及人，以道德修养达到理想人格。",
        "audio": "answer3.mp3"
    },
    "红楼梦第五回讲什么": {
        "answer": "抱歉，本系统专注于儒家经典和先秦古籍，《红楼梦》属于清代小说，不在我的知识范围内。您可以询问关于《论语》《孟子》《诗经》等经典的问题。",
        "audio": "answer4.mp3"
    },
    "诗经中有哪些著名篇目": {
        "answer": "《诗经》共三百零五篇，其中最著名的包括：《关雎》（「关关雎鸠，在河之洲」）、《蒹葭》（「蒹葭苍苍，白露为霜」）、《木瓜》（「投我以木瓜，报之以琼琚」）等。这些诗歌体现了古代人民的生活、情感和智慧。",
        "audio": "answer5.mp3"
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

        # 转换为绝对路径
        abs_path = os.path.abspath(audio_file_path)
        print(f"绝对路径: {abs_path}")

        # 检查文件是否存在
        if not os.path.exists(abs_path):
            print(f"文件不存在: {abs_path}")
            return None

        # 检查文件大小
        file_size = os.path.getsize(abs_path)
        print(f"文件大小: {file_size} bytes")

        if file_size < 1000:
            print("文件太小，可能是空文件")
            return None

        # 使用一句话识别 API
        from dashscope.audio.asr import Recognition

        # 创建 Recognition 实例 - 使用正确的模型名称
        recognizer = Recognition(
            model='paraformer-realtime-v2',
            format='wav',
            sample_rate=16000,
            callback=None
        )

        # 调用识别
        result = recognizer.call(abs_path)

        print(f"识别状态码: {result.status_code}")

        if result.status_code == 200:
            # 提取文本
            if hasattr(result, 'output') and result.output:
                # 尝试直接获取 text
                text = result.output.get('text', '')
                if text:
                    print(f"识别成功: {text}")
                    return text

                # 尝试从 sentence 获取（可能是字典）
                sentence = result.output.get('sentence', None)
                if sentence:
                    if isinstance(sentence, dict):
                        text = sentence.get('text', '')
                        if text:
                            print(f"识别成功: {text}")
                            return text
                    elif isinstance(sentence, list) and len(sentence) > 0:
                        # sentence 是列表，取第一个元素
                        first_sentence = sentence[0]
                        if isinstance(first_sentence, dict):
                            text = first_sentence.get('text', '')
                            if text:
                                print(f"识别成功: {text}")
                                return text

            # 尝试 get_sentence 方法
            if hasattr(result, 'get_sentence'):
                sentence = result.get_sentence()
                if sentence:
                    if isinstance(sentence, dict):
                        text = sentence.get('text', '')
                        if text:
                            print(f"识别成功: {text}")
                            return text
                    elif isinstance(sentence, list) and len(sentence) > 0:
                        first = sentence[0]
                        if isinstance(first, dict):
                            text = first.get('text', '')
                            if text:
                                print(f"识别成功: {text}")
                                return text

            print("识别成功但未获取到文本（可能音频无语音内容）")
            print(f"完整结果: {result}")
            print(f"output 内容: {result.output if hasattr(result, 'output') else 'None'}")
            return None
        else:
            error_msg = result.message if hasattr(result, 'message') else '未知错误'
            print(f"识别失败: {error_msg}")
            return None

    except Exception as e:
        print(f"语音识别异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

# ===== 语音合成函数 =====
def synthesize_speech(text, output_filename, voice_type='mandarin_female'):
    """
    使用阿里云语音合成
    :param text: 要合成的文本
    :param output_filename: 输出文件名（仅文件名，不含路径）
    :param voice_type: 语音类型，见 VOICE_OPTIONS
    :return: 成功返回文件名，失败返回 None
    """
    try:
        print(f"开始合成语音: {text[:50]}...")

        # 获取语音配置
        voice_config = VOICE_OPTIONS.get(voice_type, VOICE_OPTIONS['mandarin_female'])
        print(f"使用语音: {voice_config['name']} ({voice_config['voice']})")

        # 创建语音合成器
        synthesizer = SpeechSynthesizer(
            model=voice_config['model'],
            voice=voice_config['voice']
        )

        # 合成语音
        audio_data = synthesizer.call(text)

        if isinstance(audio_data, bytes) and len(audio_data) > 0:
            # 保存到 static/audio 目录
            output_path = os.path.join('static', 'audio', output_filename)

            with open(output_path, 'wb') as f:
                f.write(audio_data)

            file_size = os.path.getsize(output_path)
            print(f"语音合成成功: {output_path}, 大小: {file_size} bytes")
            return output_filename
        else:
            print("语音合成失败: 未获取到音频数据")
            return None

    except Exception as e:
        print(f"语音合成异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

# ===== 辅助函数 =====
def find_answer_in_kb(question):
    """在知识库中查找答案（精确匹配和模糊匹配）"""
    question = question.strip().replace("？", "").replace("?", "")

    # 精确匹配
    if question in QA_DATABASE:
        print(f"✓ 精确匹配成功: {question}")
        return QA_DATABASE[question]

    # 模糊匹配
    for key, value in QA_DATABASE.items():
        if key in question or question in key:
            print(f"✓ 模糊匹配成功: {question} → {key}")
            return value

    return None

def ask_llm_with_knowledge(question):
    """使用 LLM 理解问题并从知识库中查找答案"""
    try:
        # 构建知识库上下文
        knowledge_context = "\n".join([f"问：{k}\n答：{v['answer']}" for k, v in QA_DATABASE.items()])

        # 构建 prompt
        prompt = f"""你是一位古籍专家，专门回答关于中国古代典籍的问题。

知识库内容：
{knowledge_context}

用户问题：{question}

请根据知识库内容回答用户的问题。注意：
1. 如果问题与知识库中的某个问题相似（例如同音字、近义词），请使用知识库中的答案
2. 如果知识库中没有相关信息，请回答"抱歉，我暂时无法回答这个问题。您可以询问关于《论语》、孔子、《诗经》等古籍的问题。"
3. 直接给出答案，不要重复问题

请回答："""

        print(f"→ 调用 LLM 理解问题...")

        response = Generation.call(
            model='qwen-turbo',
            prompt=prompt,
            max_tokens=500
        )

        if response.status_code == 200:
            answer = response.output.text.strip()
            print(f"✓ LLM 回答成功")
            return {
                "answer": answer,
                "audio": "default.mp3"
            }
        else:
            print(f"✗ LLM 调用失败: {response.message}")
            return None

    except Exception as e:
        print(f"✗ LLM 异常: {str(e)}")
        return None

def find_answer(question):
    """
    混合方案：先尝试知识库匹配，再用 LLM 理解
    """
    print(f"\n========== 问答处理 ==========")
    print(f"问题: {question}")

    # 方案 1: 先尝试知识库精确/模糊匹配
    kb_result = find_answer_in_kb(question)
    if kb_result:
        print(f"✓ 使用知识库答案")
        return kb_result

    # 方案 2: 知识库没找到，使用 LLM 理解
    print(f"→ 知识库未找到，尝试 LLM 理解...")
    llm_result = ask_llm_with_knowledge(question)
    if llm_result:
        return llm_result

    # 方案 3: 兜底回答
    print(f"✗ 所有方案失败，返回默认回答")
    return {
        "answer": "抱歉，我暂时无法回答这个问题。您可以询问关于《论语》、孔子、《诗经》等古籍的问题。",
        "audio": "default.mp3"
    }

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
    time.sleep(1)

    # 查找答案
    result = find_answer(question)

    return jsonify({
        'answer': result['answer'],
        'audio_file': result['audio']
    })

@app.route('/audio/<filename>')
def get_audio(filename):
    """返回音频文件"""
    audio_path = os.path.join('static', 'audio', filename)
    abs_path = os.path.abspath(audio_path)

    print(f"请求音频: {filename}")
    print(f"相对路径: {audio_path}")
    print(f"绝对路径: {abs_path}")
    print(f"文件存在: {os.path.exists(audio_path)}")
    print(f"当前工作目录: {os.getcwd()}")

    if os.path.exists(audio_path):
        return send_file(audio_path, mimetype='audio/mpeg')
    else:
        # 返回默认音频
        default_path = os.path.join('static', 'audio', 'default.mp3')
        if os.path.exists(default_path):
            return send_file(default_path, mimetype='audio/mpeg')
        return "音频未找到", 404

@app.route('/get_questions')
def get_questions():
    """获取预设问题列表"""
    questions = list(QA_DATABASE.keys())
    return jsonify({'questions': questions})

@app.route('/get_voice_options')
def get_voice_options():
    """获取可用的语音选项"""
    options = []
    for key, config in VOICE_OPTIONS.items():
        options.append({
            'value': key,
            'name': config['name']
        })
    return jsonify({'voices': options})

@app.route('/voice_ask', methods=['POST'])
def voice_ask():
    """处理语音问答 - 真实语音识别和合成"""
    recognized_text = None

    # 接收音频文件
    if 'audio' not in request.files:
        return jsonify({'error': '未接收到音频文件'}), 400

    audio_file = request.files['audio']
    voice_type = request.form.get('voice_type', 'mandarin_female')  # 获取语音类型
    print(f"收到语音文件: {audio_file.filename}, 语音类型: {voice_type}")

    # 保存音频文件为 WAV
    timestamp = int(time.time() * 1000)
    temp_filename = f"recording_{timestamp}.wav"
    temp_path = os.path.join(UPLOAD_FOLDER, temp_filename)

    try:
        # 保存上传的音频
        audio_file.save(temp_path)
        print(f"音频已保存: {temp_path}")

        # 调用语音识别
        recognized_text = recognize_speech(temp_path)

        if not recognized_text:
            return jsonify({'error': '语音识别失败，未识别到文字。请说清楚一些或检查麦克风。'}), 400

        print(f"识别文本: {recognized_text}")

        # 查找答案
        result = find_answer(recognized_text)
        answer_text = result['answer']

        # 生成语音合成文件名
        tts_filename = f"tts_{timestamp}.mp3"

        # 调用语音合成（传入语音类型）
        audio_file = synthesize_speech(answer_text, tts_filename, voice_type)

        if not audio_file:
            # 如果合成失败，使用默认音频
            print("语音合成失败，使用默认音频")
            audio_file = 'minimax_tts.mp3'

        return jsonify({
            'recognized_text': recognized_text,
            'answer': answer_text,
            'audio_file': audio_file
        })

    except Exception as e:
        print(f"处理语音时出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'处理失败: {str(e)}'}), 500

    finally:
        # 清理临时文件（可选）
        # if os.path.exists(temp_path):
        #     os.remove(temp_path)
        pass

if __name__ == '__main__':
    print("=" * 50)
    print("古籍语音问答助手 - 演示版")
    print("=" * 50)
    print("访问: http://localhost:5000")
    print("=" * 50)

    # 检查必要的目录
    os.makedirs('static/audio', exist_ok=True)
    os.makedirs('static/images', exist_ok=True)
    os.makedirs('templates', exist_ok=True)

    app.run(host='127.0.0.1', port=5000, debug=True)
