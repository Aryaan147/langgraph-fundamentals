import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage

CONFIG = {"configurable":{"thread_id":"thread-1"}}

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


user_input = st.chat_input("Type here")

if user_input:
    st.session_state["message_history"].append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    response = chatbot.invoke({"messages":user_input}, config=CONFIG)["messages"][-1].content
    st.session_state["message_history"].append({"role": "assistant", "content": response})
    
    with st.chat_message("assistant"):
        st.markdown(response)