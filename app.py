import streamlit as st
from dotenv import load_dotenv
import os
from rag_pipeline import WebRAG

load_dotenv()

st.set_page_config(page_title="Chat with Website", page_icon="🌐")
st.title("🌐 Chat with Any Website")

# Initialize session state
if 'rag' not in st.session_state:
    st.session_state.rag = WebRAG()
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'website_loaded' not in st.session_state:
    st.session_state.website_loaded = False

# Sidebar for website input
with st.sidebar:
    st.header("Load Website")
    website_url = st.text_input("Enter website URL:", placeholder="https://example.com")
    
    if st.button("Load Website"):
        if website_url:
            with st.spinner("Loading and processing website..."):
                try:
                    st.session_state.rag.load_website(website_url)
                    st.session_state.website_loaded = True
                    st.session_state.messages = []
                    st.success("Website loaded successfully!")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a URL")

# Main chat interface
if st.session_state.website_loaded:
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if question := st.chat_input("Ask a question about the website..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)
        
        # Get response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.rag.ask(question)
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.info("👈 Enter a website URL in the sidebar to get started!")