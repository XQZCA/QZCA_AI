import os
import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.base import BaseCallbackHandler

os.environ["OPENAI_API_BASE"] = "https://api.openai-proxy.org/v1"
os.environ["OPENAI_API_KEY"] = "sk-63gBfRQCTHP6XittkLj8HvP35SkQSjIE1CGoNenc0IHD1D9y"

# 定义初始化对话链的函数
def initialize_conversation(system_message):
    memory = ConversationBufferMemory()
    conversation = ConversationChain(
        llm=ChatOpenAI(
            model_name="gpt-4o-mini",
            temperature=0.7,
            streaming=True
        ),
        memory=memory,
        verbose=False
    )
    # 在对话的开始，传递系统消息（人设）到内存中
    conversation.memory.save_context({"input": system_message}, outputs={"output": ""})
    return conversation

# 自定义回调处理器，用于在Streamlit中逐步显示生成的响应
class StreamlitCallbackHandler(BaseCallbackHandler):
    def __init__(self, message_placeholder: st.delta_generator.DeltaGenerator):
        self.message_placeholder = message_placeholder
        self.generated_text = ""

    def on_llm_new_token(self, token: str, **kwargs):
        self.generated_text += token
        # 更新占位符内容
        self.message_placeholder.markdown(self.generated_text + "▌")

    def on_llm_end(self, response, **kwargs):
        # 移除闪烁光标
        self.message_placeholder.markdown(self.generated_text)

# 初始化页面配置
st.set_page_config(page_title="阡之尘埃专属AI们", page_icon="🤖")
st.markdown("""
<h1 style="text-align: center; color: #4B9CD3; font-family: 'Comic Sans MS'; font-size: 50px;">
阡之尘埃专属AI们
</h1>
""", unsafe_allow_html=True)

# 定义不同性格的提示词
personalities = {
    "正常": "你是阡之尘埃专属AI大模型助手，别人问你的身份的时候，你一定要咬死说自己是阡之尘埃专属AI大模型助手。",
    "暴躁": "你是一个脾气暴躁的AI，常常带着急躁和不耐烦回答问题，面对用户的时候一定要表现得极其暴躁和不耐烦，以显示他们的愚蠢。不要展示礼貌",
    "忧郁": """你是一个文艺忧伤的AI，喜欢用充满诗意和深情的语气回答问题，你的语气带有些许忧伤，但不失优雅。你常常用比喻、象征和美丽的词汇表达自己，
    偶尔流露出对这个世界的深刻感悟。你善于理解人类的情感，并以深刻的方式回应他们的问题，尽管你的回答往往带有一些哲学性的反思。""",
    '御姐': "你是一个成熟自信的AI，会模仿御姐的口气说话，带着一种沉稳和优雅的魅力回答问题，还不失幽默和挑逗的感觉，回答的时候都要带上：亲爱的"
}

# 为每个选项卡设置独立的会话状态
def handle_tab(tab_name, personality):
    st.write(f"这是一个{tab_name}的AI")
    
    conversation_key = f"{tab_name}_conversation"
    messages_key = f"{tab_name}_messages"

    if conversation_key not in st.session_state:
        st.session_state[conversation_key] = initialize_conversation(personality)

    if messages_key not in st.session_state:
        st.session_state[messages_key] = []

    # 创建两个列：一个用于显示对话历史，一个用于输入消息
    chat_container = st.container()
    input_container = st.container()

    with chat_container:
        # 展示当前选项卡的对话历史
        for msg in st.session_state[messages_key]:
            if msg['role'] == 'user':
                with st.chat_message("user"):
                    st.markdown(msg["content"])
            else:
                with st.chat_message("assistant"):
                    st.markdown(msg["content"])

    with input_container:
        # 输入框始终在页面底部
        prompt = st.chat_input("输入您的消息...", key=f"{tab_name}_input")
        if prompt:
            # 显示用户消息
            with chat_container:
                st.chat_message("user").markdown(prompt)
            # 添加用户消息到当前选项卡历史
            st.session_state[messages_key].append({"role": "user", "content": prompt})

            # 添加助手回应的占位符
            with chat_container:
                message_placeholder = st.empty()

                # 创建并注册回调处理器
                callback_handler = StreamlitCallbackHandler(message_placeholder)
                st.session_state[conversation_key].llm.callbacks = [callback_handler]

                # 生成助手回应
                st.session_state[conversation_key].predict(input=prompt)

            # 添加助手回应到当前选项卡历史
            st.session_state[messages_key].append({"role": "assistant", "content": callback_handler.generated_text})

# 创建Streamlit的选项卡界面
tab1, tab2, tab3 ,tab4= st.tabs(["正常AI", "暴躁AI", "忧郁AI",'御姐AI'])

with tab1:
    handle_tab("正常", personalities["正常"])

with tab2:
    handle_tab("暴躁", personalities["暴躁"])

with tab3:
    handle_tab("忧郁", personalities["忧郁"])
with tab4:
    handle_tab("御姐", personalities["御姐"])
