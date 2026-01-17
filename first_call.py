import os
import requests
import dashscope
from dotenv import load_dotenv
from dashscope import Generation
from dashscope.api_entities.dashscope_response import Message

# 加载环境变量
load_dotenv()

print("=== 开始测试完全免费的API调用 ===\n")

# ----- 1. 调用 通义千问 API -----
print("=== 开始调用阿里云通义千问 API (使用官方SDK) ===")
try:
    # 1. 设置API Key (这是dashscope的专用设置方式)
    dashscope.api_key = os.getenv("ALIYUN_API_KEY")
    # 2. 使用 Message 类正确构建消息列表
    messages = [
        Message(role='user', content='你好，通义千问！请用一句话介绍你的特长。')
    ]
    # 3. 发起调用
    response = Generation.call(
        model='qwen-plus',  # 或 'qwen-turbo', 'qwen-max'
        messages=messages,
        stream = False
    )
    print(f"[INFO] 请求ID: {response.request_id}")
    print(f"[INFO] 使用Token数: {response.usage.total_tokens}")
    # 4. 检查并打印结果
    # ========== 【核心修正】根据实际响应结构提取回复 ==========
    if response.status_code == 200:
        # 方式1：直接访问 output.text (DashScope标准格式)
        reply_text = response.output.text
        print(f"通义千问回复: {reply_text}\n")
    else:
        print(f'错误代码: {response.code}， 错误信息: {response.message}\n')
except Exception as e:
    print(f"请求过程出错: {e}\n")

# ----- 2. 调用 智谱AI GLM-4-Flash API -----
print("2. 正在调用 智谱AI GLM-4-Flash API...")
try:
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('ZHIPU_API_KEY')}"
    }
    data = {
        "model": "glm-4-flash",
        "messages": [{"role": "user", "content": "你好，GLM！请用一句话介绍你的特长。"}],
        "stream": False
    }
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    if response.status_code == 200 and 'choices' in result:
        print(f"   智谱AI回复: {result['choices'][0]['message']['content']}\n")
    else:
        print(f"   智谱AI调用异常: {result}\n")
except Exception as e:
    print(f"   智谱AI调用失败: {e}\n")

print("=== 免费API调用测试结束 ===")