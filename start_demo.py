"""
一键启动演示系统
适合现场演示和学员实操
"""

import os
import sys

def check_api_key():
    """检查并配置 API Key"""
    key_file = 'qwen.key'

    if os.path.exists(key_file):
        with open(key_file, 'r', encoding='utf-8') as f:
            key = f.read().strip()
            if key and len(key) > 20:
                print("✅ API Key 已配置")
                return True

    print("\n" + "=" * 60)
    print("⚠️  未找到 API Key 配置")
    print("=" * 60)
    print("\n请按以下步骤获取 API Key：")
    print("1. 打开：https://dashscope.console.aliyun.com/")
    print("2. 注册阿里云账号（如果还没有）")
    print("3. 开通「模型服务灵积」")
    print("4. 在控制台复制 API Key")
    print("\n" + "=" * 60)

    # 交互式输入
    choice = input("\n是否现在输入 API Key？(y/n): ").strip().lower()

    if choice == 'y':
        print("\n请粘贴您的 API Key（格式如：sk-xxxxxxxx）：")
        key = input().strip()

        if key and len(key) > 20:
            with open(key_file, 'w', encoding='utf-8') as f:
                f.write(key)
            print(f"\n✅ API Key 已保存到 {key_file}")
            return True
        else:
            print("\n❌ Key 格式不正确")
            return False
    else:
        print("\n提示：您也可以手动创建 'qwen.key' 文件，将 Key 粘贴进去")
        return False

def check_dependencies():
    """检查依赖包"""
    print("\n检查依赖包...")

    required_packages = {
        'flask': 'Flask',
        'dashscope': 'DashScope'
    }

    missing = []

    for package, display_name in required_packages.items():
        try:
            __import__(package)
            print(f"  ✅ {display_name}")
        except ImportError:
            print(f"  ❌ {display_name} 未安装")
            missing.append(package)

    if missing:
        print("\n缺少依赖包，请运行以下命令安装：")
        print(f"  pip install {' '.join(missing)}")
        return False

    print("✅ 依赖包完整")
    return True

def check_directories():
    """检查并创建必要的目录"""
    dirs = [
        'static/audio',
        'static/images',
        'templates',
        'temp_recordings'
    ]

    for d in dirs:
        os.makedirs(d, exist_ok=True)

    return True

def main():
    print("\n" + "=" * 60)
    print("古籍语音问答助手 - 演示系统")
    print("=" * 60)

    # 检查 API Key
    if not check_api_key():
        print("\n❌ 启动中止：需要配置 API Key")
        input("\n按回车键退出...")
        sys.exit(1)

    # 检查依赖
    if not check_dependencies():
        print("\n❌ 启动中止：缺少依赖包")
        input("\n按回车键退出...")
        sys.exit(1)

    # 检查目录
    check_directories()

    # 启动服务
    print("\n" + "=" * 60)
    print("🚀 正在启动服务...")
    print("=" * 60)
    print("\n访问地址：http://localhost:5000")
    print("按 Ctrl+C 停止服务\n")
    print("=" * 60 + "\n")

    # 运行 Flask 应用
    try:
        os.system('python app.py')
    except KeyboardInterrupt:
        print("\n\n服务已停止")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")
        input("\n按回车键退出...")
