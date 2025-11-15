"""Debug Info Page - Shows current configuration"""

import streamlit as st
import os
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(
    page_title="Debug Info",
    page_icon="🔧",
    layout="wide"
)

st.markdown("# 🔧 Debug Information")
st.markdown("This page shows the current configuration and settings.")

st.markdown("---")

# System Info
st.markdown("## 💻 System Information")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Environment:**")
    st.code(f"""
Python Version: {sys.version}
Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Working Directory: {os.getcwd()}
    """)

with col2:
    st.markdown("**Environment Variables:**")
    api_key = os.getenv("ANTHROPIC_API_KEY", "NOT SET")
    masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
    
    st.code(f"""
AI_MODEL: {os.getenv('AI_MODEL', 'NOT SET')}
API_KEY: {masked_key}
APP_ENV: {os.getenv('APP_ENV', 'NOT SET')}
    """)

st.markdown("---")

# AI Client Info
st.markdown("## 🤖 AI Client Configuration")

if 'ai_client' in st.session_state:
    ai_client = st.session_state.ai_client
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Model", ai_client.model)
    
    with col2:
        st.metric("Max Tokens", ai_client.max_tokens)
    
    with col3:
        st.metric("Temperature", ai_client.temperature)
    
    st.markdown("---")
    
    # Test the API
    st.markdown("## 🧪 Live API Test")
    
    if st.button("Test API Connection", type="primary"):
        with st.spinner("Testing API..."):
            try:
                response = ai_client.create_message(
                    system="You are a helpful assistant.",
                    messages=[{"role": "user", "content": "Say 'Working!' in one word."}],
                    max_tokens=10
                )
                
                st.success("✅ API Connection Successful!")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Response:**")
                    st.info(response["content"])
                
                with col2:
                    st.markdown("**Actual Model Used:**")
                    st.code(response.get("model", "Unknown"))
                    
                    st.markdown("**Token Usage:**")
                    st.code(f"""
Input Tokens: {response['usage']['input_tokens']}
Output Tokens: {response['usage']['output_tokens']}
Total: {response['usage']['input_tokens'] + response['usage']['output_tokens']}
                    """)
            
            except Exception as e:
                st.error(f"❌ API Test Failed: {str(e)}")
else:
    st.warning("AI Client not initialized. Go to Home page first.")

st.markdown("---")

# Database Info
st.markdown("## 💾 Database Information")

if 'db_manager' in st.session_state:
    db = st.session_state.db_manager
    st.info(f"Database URL: {db.db_url}")
    
    if 'student_manager' in st.session_state:
        students = st.session_state.student_manager.get_all_students()
        st.metric("Total Students", len(students))
else:
    st.warning("Database not initialized.")

st.markdown("---")

# Session State
with st.expander("📊 Session State (Click to expand)"):
    st.json({
        "current_student": str(st.session_state.get('current_student', None)),
        "current_session": st.session_state.get('current_session', None),
        "chat_messages_count": len(st.session_state.get('chat_messages', [])),
        "all_keys": list(st.session_state.keys())
    })

# Footer
st.markdown("---")
st.caption("This page is for debugging only. Remove it in production by deleting pages/99_Debug_Info.py")

