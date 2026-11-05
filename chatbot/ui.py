import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage
import uuid




# ---------Utility Func----------
def generate_uuid():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    st.session_state["thread_id"] = generate_uuid()
    if(chatbot.get_state(config=CONFIG).values):
        add_thread()
    else:
        st.session_state["chat_threads"][0] = st.session_state["thread_id"]
    st.session_state["message_history"] = []

def add_thread():
    st.session_state["chat_threads"].insert(0, st.session_state["thread_id"])




# ----------Sesssion setup----------
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_uuid()
    add_thread()

CONFIG = {"configurable":{"thread_id":st.session_state["thread_id"]}}



# ---------Sidebar----------
st.sidebar.title("LangGraph ChatBot")

if st.sidebar.button("New conversation"):
    reset_chat()

st.sidebar.header("Conversation History")


for i, thread in enumerate(st.session_state["chat_threads"]):
    if st.sidebar.button(thread):
        # if(chatbot.get_state(config=CONFIG).values):
        #     st.session_state["chat_threads"].pop(0)
        st.session_state["thread_id"] = st.session_state["chat_threads"][i]
        st.session_state["message_history"] = []
        for msg in chatbot.get_state(config=CONFIG).values["messages"]:

            if isinstance(msg, HumanMessage):
                st.session_state["message_history"].append({"role": "user", "content": msg.content})
                continue

            st.session_state["message_history"].append({"role": "assistant", "content": msg.content})




# ----------Main UI----------
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"]) 


user_input = st.chat_input("Type here")

if user_input:
    st.session_state["message_history"].append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)


    with st.chat_message("assistant"):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages"
            )
        )
        
    st.session_state["message_history"].append({"role": "assistant", "content": ai_message})
