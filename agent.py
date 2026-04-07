import os
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI 
from langchain_core.messages import SystemMessage, HumanMessage
from tools import search_flights, search_hotels, calculate_budget
from dotenv import load_dotenv

load_dotenv()

# 1. Đọc System Prompt
with open("system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# 2. Khai báo State
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# 3. Tools
tools_list = [search_flights, search_hotels, calculate_budget]

# Dùng model hỗ trợ tool calling
llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "http://localhost:3000",
        "X-Title": "TravelBuddy Agent"
    }
)

llm_with_tools = llm.bind_tools(tools_list)

# 4. Agent Node
def agent_node(state: AgentState):
    messages = state["messages"]

    # đảm bảo system prompt luôn đầu
    if not any(isinstance(m, SystemMessage) for m in messages):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
    
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# 5. Graph
builder = StateGraph(AgentState)
builder.add_node("agent", agent_node)
builder.add_node("tools", ToolNode(tools_list))

builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")

graph = builder.compile()

# 6. Chat loop
if __name__ == "__main__":
    print("=" * 60)
    print("TravelBuddy – ReAct Agent (Stable Tool Calling)")
    print("=" * 60)
    
    while True:
        user_input = input("\nBạn: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            break
        
        for chunk in graph.stream({"messages": [HumanMessage(content=user_input)]}):
            for node, values in chunk.items():
                if node == "agent":
                    last_msg = values["messages"][-1]
                    if last_msg.content:
                        print(f"\nTravelBuddy: {last_msg.content}")