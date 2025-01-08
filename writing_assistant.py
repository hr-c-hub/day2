import streamlit as st
import requests
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# DeepSeek API配置
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
DEEPSEEK_API_URL = "https://api.deepseek.ai/v1/chat/completions"

def get_ai_response(prompt, mode):
    """调用DeepSeek API获取响应"""
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 根据不同模式设置不同的系统提示
    system_prompts = {
        "写作助手": "我是一个专业的写作助手，可以帮助你改进文章结构，提供写作建议。",
        "文章润色": "我是一个文章润色专家，可以帮助改进文章的表达，使其更加优美流畅。",
        "语法检查": "我是一个语法检查专家，将帮助检查并修正文章中的语法错误。",
        "标点符号": "我是一个标点符号专家，将帮助检查并修正文章中的标点符号使用。"
    }
    
    data = {
        "messages": [
            {"role": "system", "content": system_prompts[mode]},
            {"role": "user", "content": prompt}
        ],
        "model": "deepseek-chat",
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"发生错误: {str(e)}"

def test_api_connection():
    """测试API连接"""
    try:
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "messages": [
                {"role": "user", "content": "Hello"}
            ],
            "model": "deepseek-chat",
            "max_tokens": 10
        }
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
        response.raise_for_status()
        return True
    except Exception as e:
        st.error(f"API连接测试失败: {str(e)}")
        return False

def main():
    st.title("AI写作助手")
    
    # 添加API连接测试
    if not test_api_connection():
        st.error("无法连接到DeepSeek API，请检查API密钥和网络连接")
        return
    
    # 模式选择
    mode = st.selectbox(
        "选择功能模式",
        ["写作助手", "文章润色", "语法检查", "标点符号"]
    )
    
    # 输入区域
    user_input = st.text_area("请输入您的文本:", height=200)
    
    # 功能说明
    mode_descriptions = {
        "写作助手": "提供写作建议和改进方案",
        "文章润色": "优化文章表达，使其更加优美流畅",
        "语法检查": "检查并修正语法错误",
        "标点符号": "检查并修正标点符号使用"
    }
    
    st.info(f"当前模式: {mode} - {mode_descriptions[mode]}")
    
    # 提交按钮
    if st.button("提交"):
        if user_input:
            with st.spinner('处理中...'):
                # 根据不同模式设置不同的提示
                prompts = {
                    "写作助手": f"请为以下文本提供写作建议和改进方案：\n\n{user_input}",
                    "文章润色": f"请帮我润色以下文本，使其更加优美流畅：\n\n{user_input}",
                    "语法检查": f"请检查并修正以下文本中的语法错误：\n\n{user_input}",
                    "标点符号": f"请检查并修正以下文本中的标点符号使用：\n\n{user_input}"
                }
                
                response = get_ai_response(prompts[mode], mode)
                st.markdown("### AI反馈:")
                st.write(response)
        else:
            st.warning("请输入文本内容")

if __name__ == "__main__":
    main()