from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

from config import settings

model = ChatGroq(
    model=settings.groq_model,
    api_key=settings.groq_api_key.get_secret_value(),
)


class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def chat_node(state: ChatState) -> dict[str, list[BaseMessage]]:
    response = model.invoke(state["messages"])
    return {"messages": [response]}


workflow = StateGraph(ChatState)

workflow.add_node("chat_node", chat_node)
workflow.add_edge(START, "chat_node")
workflow.add_edge("chat_node", END)

memory_checkpointer = InMemorySaver()

chatbot = workflow.compile(checkpointer=memory_checkpointer)
