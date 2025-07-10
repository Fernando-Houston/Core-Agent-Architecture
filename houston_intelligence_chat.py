#!/usr/bin/env python3
"""
Houston Intelligence Platform - Interactive Chat Interface
Quick testing interface for Houston real estate intelligence
"""

import streamlit as st
import requests
import json
from datetime import datetime
from typing import Dict, List
import os

# Voice features disabled for cloud deployment
SPEECH_AVAILABLE = False
TTS_AVAILABLE = False

# Configuration
# Hardcoded for Streamlit deployment
API_BASE_URL = "https://core-agents-6d4f5.up.railway.app"
API_VERSION = "v1"

# Page config
st.set_page_config(
    page_title="Houston Intelligence Platform",
    page_icon="🏗️",
    layout="wide"
)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'voice_enabled' not in st.session_state:
    st.session_state.voice_enabled = False

def query_api(endpoint: str, method: str = "GET", data: Dict = None) -> Dict:
    """Query the Houston Intelligence API"""
    url = f"{API_BASE_URL}/api/{API_VERSION}/{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url)
        else:
            response = requests.post(url, json=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API Error: {response.status_code}"}
    except Exception as e:
        return {"error": f"Connection error: {str(e)}"}

def process_query(query: str) -> Dict:
    """Process natural language query through the API"""
    return query_api("query", "POST", {"query": query})

def get_voice_input():
    """Get voice input from microphone"""
    if not SPEECH_AVAILABLE:
        st.error("Speech recognition not available. Install with: pip install SpeechRecognition pyaudio")
        return None
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("🎤 Listening...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            return text
        except:
            return None

def speak_response(text: str):
    """Convert text to speech"""
    if not TTS_AVAILABLE:
        return
    
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Main UI
st.title("🏗️ Houston Intelligence Platform")
st.markdown("### AI-Powered Real Estate Intelligence Chat")

# Sidebar with quick actions
with st.sidebar:
    st.header("🚀 Quick Actions")
    
    # API Status
    health = query_api("health")
    if "status" in health:
        st.success(f"✅ API Status: {health['status']}")
    else:
        st.error("❌ API Offline")
    
    st.divider()
    
    # Quick query buttons
    st.subheader("📋 Example Queries")
    
    example_queries = [
        "What are the latest building permits in Houston?",
        "Show me investment opportunities in Houston Heights",
        "What's the market trend in River Oaks?",
        "Find distressed properties with tax issues",
        "Top developers by permit activity",
        "Environmental risks in Sugar Land"
    ]
    
    for query in example_queries:
        if st.button(query, key=query):
            st.session_state.messages.append({"role": "user", "content": query})
            
    st.divider()
    
    # Data Sources Status
    st.subheader("📊 Data Sources")
    stats = query_api("stats")
    if "stats" in stats:
        st.metric("Total Agents", stats['stats'].get('total_agents', 0))
        st.metric("Knowledge Files", stats['stats'].get('knowledge_files', 0))
        st.metric("Data Sources", stats['stats'].get('data_sources', 0))
    
    st.divider()
    
    # Voice Toggle
    st.subheader("🎤 Voice Features")
    voice_input = st.checkbox("Enable Voice Input", value=st.session_state.voice_enabled)
    voice_output = st.checkbox("Enable Voice Output", value=False)

# Main chat interface
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 Chat Interface")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if voice_input:
        col_text, col_voice = st.columns([5, 1])
        with col_text:
            user_input = st.chat_input("Ask about Houston real estate...")
        with col_voice:
            if st.button("🎤"):
                voice_text = get_voice_input()
                if voice_text:
                    user_input = voice_text
                    st.session_state.messages.append({"role": "user", "content": user_input})
    else:
        user_input = st.chat_input("Ask about Houston real estate...")
    
    # Process user input
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.chat_message("user"):
            st.write(user_input)
        
        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                response = process_query(user_input)
                
                if "response" in response:
                    answer = response['response'].get('answer', 'No response')
                    st.write(answer)
                    
                    # Show sources if available
                    if 'sources' in response['response']:
                        with st.expander("📚 Sources"):
                            for source in response['response']['sources']:
                                st.write(f"- {source}")
                    
                    # Voice output if enabled
                    if voice_output:
                        speak_response(answer[:200])  # Limit voice to 200 chars
                    
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    error_msg = response.get('error', 'Unknown error')
                    st.error(f"Error: {error_msg}")

with col2:
    st.subheader("🔍 Quick Insights")
    
    # Latest insights
    insights = query_api("insights/latest")
    if "insights" in insights:
        for insight in insights['insights'][:5]:
            with st.container():
                st.write(f"**{insight.get('title', 'Insight')}**")
                st.write(f"_{insight.get('summary', '')[:100]}..._")
                st.caption(f"Source: {insight.get('agent', 'Unknown')}")
                st.divider()
    
    # Recent permits
    if st.button("📋 Show Recent Permits"):
        permits = query_api("permits/recent?limit=5")
        if "permits" in permits:
            for permit in permits['permits']:
                st.write(f"**{permit.get('address')}**")
                st.write(f"Type: {permit.get('type')}")
                st.write(f"Value: ${permit.get('value', 0):,.0f}")
                st.divider()

# Footer with API endpoints
with st.expander("🛠️ API Endpoints for Testing"):
    st.code(f"""
# Base URL: {API_BASE_URL}

# Natural Language Query
POST /api/v1/query
{{"query": "Your question here"}}

# Get Recent Permits
GET /api/v1/permits/recent?limit=10

# Get Neighborhood Analysis
GET /api/v1/neighborhoods/Houston Heights

# Find Investment Opportunities
POST /api/v1/opportunities/investment
{{"budget_min": 1000000, "budget_max": 5000000}}

# Get Market Trends
GET /api/v1/market/trends

# Search Across Intelligence
POST /api/v1/search
{{"keywords": ["permits", "residential"]}}
    """)

# Testing tips
st.info("""
**🧪 Testing Tips:**
- Try natural language questions about Houston real estate
- Click example queries in the sidebar
- Test specific neighborhoods and property types
- Ask about permits, developers, market trends
- Request investment opportunities with budget constraints
""")

# Error handling for missing dependencies
if (voice_input or voice_output) and (not SPEECH_AVAILABLE or not TTS_AVAILABLE):
    st.warning("""
    **Voice features are disabled. To enable them locally:**
    ```bash
    pip install SpeechRecognition pyttsx3 pyaudio
    ```
    Note: Voice features don't work on Streamlit Cloud due to browser limitations.
    """)

# Update API URL reminder
if API_BASE_URL == "https://your-app.railway.app":
    st.error("⚠️ Update API_URL with your Railway deployment URL!")
    st.code("""
    # Set your Railway URL:
    export API_URL="https://your-actual-app.railway.app"
    
    # Or update in the code:
    API_BASE_URL = "https://your-actual-app.railway.app"
    """)