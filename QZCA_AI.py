import streamlit as st
import os
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# 设置 OpenAI API 地址和密钥
os.environ["OPENAI_API_BASE"] = "https://api.openai-proxy.org/v1"
os.environ["OPENAI_API_KEY"] = "sk-63gBfRQCTHP6XittkLj8HvP35SkQSjIE1CGoNenc0IHD1D9y"

# 初始化页面配置
st.set_page_config(page_title="阡之尘埃专属AI", page_icon="🤖")

# 显示大艺术字标题
st.markdown("""
<h1 style="text-align: center; color: #4B9CD3; font-family: 'Comic Sans MS'; font-size: 60px;">
阡之尘埃专属AI
</h1>
""", unsafe_allow_html=True)

# 提示用户输入
st.markdown("""
<div style="text-align: center; font-size: 24px; color: #555;">
你好！可以开始和我对话了。输入 '退出' 结束对话。
</div>
""", unsafe_allow_html=True)

# 会话状态存储
if 'history' not in st.session_state:
    st.session_state.history = []
    
if 'conversation' not in st.session_state:
    # 初始化 OpenAI 的模型接口
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)
    
    # 创建一个内存对象，存储对话历史
    memory = ConversationBufferMemory()

    # 创建一个对话链（Conversation Chain），传入内存
    st.session_state.conversation = ConversationChain(llm=llm, memory=memory)

# 输入框和显示区域
user_input = st.text_input("你说：", "")

if user_input:
    # 获取模型回应
    response = st.session_state.conversation.predict(input=user_input)

    # 存储对话历史
    st.session_state.history.append(f"用户：{user_input}")
    st.session_state.history.append(f"模型：{response}")

    # 显示对话历史
    for message in st.session_state.history:
        if message.startswith("用户"):
            st.markdown(f"<p style='color: #0066CC; font-size: 20px; text-align: left;'>{message}</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p style='color: #4B9CD3; font-size: 20px; text-align: left;'>{message}</p>", unsafe_allow_html=True)
            st.markdown(f"{'---'*30}")

# 提供退出功能
if user_input.lower() == "退出":
    st.session_state.history.clear()
    st.write("对话结束，再见！")
