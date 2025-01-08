import streamlit as st
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_anthropic import ChatAnthropic
from utils.env_loader import load_env_vars, get_api_key

# Load environment variables and initialize bot
load_env_vars()
api_key = get_api_key("ANTHROPIC_API_KEY")

# Initialize state and graph
class State(TypedDict):
    messages: Annotated[list, add_messages]

@st.cache_resource
def init_chatbot():
    """Initialize the chatbot once and cache it"""
    graph_builder = StateGraph(State)
    llm = ChatAnthropic(
        api_key=api_key,
        model="claude-3-5-sonnet-20240620"
    )
    
    def chatbot(state: State):
        messages = state["messages"]
        response = llm.invoke(messages)
        # Ensure we're getting the actual response content
        return {"messages": [response]}
    
    graph_builder.add_node("chatbot", chatbot)
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_edge("chatbot", END)
    
    return graph_builder.compile()

# Page configuration
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="centered")

# Styling (keep your existing CSS)
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f2f6;
        color: black;
    }
    div[data-testid="stChatMessage"] {
        background-color: white;
        border: 1px solid #e0e0e0;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    div[data-testid="stChatMessage"] p {
        color: black !important;
    }
    div[data-testid="stChatMessage"][data-testid*="user"] {
        background-color: #2b313e;
    }
    div[data-testid="stChatMessage"][data-testid*="user"] p {
        color: white !important;
    }
    div[data-testid="stChatMessage"][data-testid*="assistant"] {
        background-color: white;
    }
    div[data-testid="stChatMessage"][data-testid*="assistant"] p {
        color: black !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize chatbot
graph = init_chatbot()

# Main title
st.title("AI Chatbot")

# Sidebar clear button
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("What's on your mind?")

if user_input:
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Create a proper message structure for Claude
                messages = [
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant."
                    },
                    {
                        "role": "user",
                        "content": user_input
                    }
                ]
                
                response = graph.invoke({
                    "messages": messages
                })
                
                # Extract the AI response content
                ai_message = response["messages"][-1]  # Get the last message
                assistant_response = ai_message.content  # Extract just the content
                
                # Display the response
                st.markdown(assistant_response)
                
                # Update session state
                st.session_state.messages.append({"role": "user", "content": user_input})
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.write("Full error details:", e)