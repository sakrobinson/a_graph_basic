import nbformat as nbf

nb = nbf.v4.new_notebook()

# Cell 1 - Imports
cell1 = nbf.v4.new_code_cell('''import os
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_anthropic import ChatAnthropic
from IPython.display import Image, display
from utils.env_loader import load_env_vars, get_api_key''')

# Cell 2 - Environment setup
cell2 = nbf.v4.new_code_cell('''# Load environment variables
load_env_vars()

# Get API key
api_key = get_api_key("ANTHROPIC_API_KEY")''')

# Cell 3 - State definition
cell3 = nbf.v4.new_code_cell('''class State(TypedDict):
    messages: Annotated[list, add_messages]''')

# Cell 4 - Graph setup
cell4 = nbf.v4.new_code_cell('''graph_builder = StateGraph(State)
llm = ChatAnthropic(
    api_key=api_key,
    model="claude-3-5-sonnet-20240620"
)

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}''')

# Cell 5 - Build graph
cell5 = nbf.v4.new_code_cell('''graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()''')

# Cell 6 - Display graph
cell6 = nbf.v4.new_code_cell('''try:
    display(Image(graph.get_graph().draw_mermaid_png()))
except Exception:
    print("Could not display graph - make sure you have graphviz installed")''')

# Add cells to notebook
nb.cells = [cell1, cell2, cell3, cell4, cell5, cell6]

# Write the notebook to a file
nbf.write(nb, 'intro_chatbot.ipynb') 