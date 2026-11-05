from langgraph.graph import StateGraph, START, END

from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI

from langgraph.checkpoint.memory import InMemorySaver

from langgraph.graph.message import add_messages ## reducer helping to add messages in list

from dotenv import load_dotenv



llm =ChatOpenAI(model='gpt-5.6-luna')

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def chat_node(state: ChatState):
    messages = state["messages"]
    response = llm.invoke(messages)

    return {'messages': [response]}


# checkpointer
checkpointer = InMemorySaver()

graph = StateGraph(ChatState)
graph.add_node("chat_node",chat_node)

## edge
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)


chatbot = graph.compile(checkpointer = checkpointer)