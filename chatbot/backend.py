from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage
from langchain_groq import ChatGroq
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
import sqlite3

from config import settings

# --------Iitializations--------
conn = sqlite3.connect("chatbot.db", check_same_thread=False)
memory_checkpointer = SqliteSaver(conn=conn)

model = ChatGroq(
    model=settings.groq_model,
    api_key=settings.groq_api_key.get_secret_value(),
)


# --------Chatbot---------
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def chat_node(state: ChatState) -> dict[str, list[BaseMessage]]:
    response = model.invoke(state["messages"])
    return {"messages": [response]}


workflow = StateGraph(ChatState)

workflow.add_node("chat_node", chat_node)
workflow.add_edge(START, "chat_node")
workflow.add_edge("chat_node", END)


chatbot = workflow.compile(checkpointer=memory_checkpointer)



# ---------util--------
def get_chat_threads():
    threads = []
    unique = set()
    for checkpoint in memory_checkpointer.list(None):
        thread = checkpoint.config["configurable"]["thread_id"]
        if thread not in unique:
            unique.add(thread)
            threads.append(thread)
    return threads