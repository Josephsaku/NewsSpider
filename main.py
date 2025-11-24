import streamlit as st
from pdf_qa import get_response
from langchain.memory import ConversationBufferMemory
from get_text import update

st.header("公文通查询助手👀")
num = st.text_input("请输入你想查询的页数（注意：一页内容很多，一般1~2页足够查看最近信息）")
upgrade = st.button("更新文件")
question = st.text_input("请提问：")
query = st.button("开始提问")

if query:

    if 'memory' not in st.session_state:
        st.session_state['memory'] = ConversationBufferMemory(
            return_messages=True,
            memory_key='chat_history',
            output_key='answer'
        )

    if question:
        with st.spinner("查询时间较长，请耐心等待..."):
            response = get_response(st.session_state['memory'], question)
        st.write("### 查询结果：")
        st.write(response['answer'])
        st.session_state['chat_history'] = response['chat_history']
    else:
        st.info("请输入问题哦")
        st.stop()

if upgrade:
    if num:
        with st.spinner("更新文件较为耗时，请耐心等待...."):
            isover = update(int(num)+1)
        if isover:
            st.success("更新完成")
    else:
        st.info("请输入页数：")
        st.stop()


