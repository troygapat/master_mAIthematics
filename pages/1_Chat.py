"""
Chat Page - Interactive tutoring conversation
"""

import streamlit as st
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.math_renderer import render_math_message

st.set_page_config(
    page_title="Chat - AI Math Tutor",
    page_icon="▸",
    layout="wide"
)

# Check if student is selected
if 'current_student' not in st.session_state or st.session_state.current_student is None:
    st.warning("Please select or create a student profile first!")
    if st.button("Go to Home"):
        st.switch_page("app.py")
    st.stop()

st.markdown("# ▸ Chat with Your Math Tutor")

# Custom CSS for upload button visibility - ONLY for upload button
st.markdown("""
<style>
    /* Only target the upload toggle button by its key */
    button[data-testid*="stButton"] p:has-text("Upload"),
    button:has-text("Upload") {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

# Session type selector
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown(f"**Student:** {st.session_state.current_student.name} (Grade {st.session_state.current_student.grade_level})")

with col2:
    session_type = st.selectbox(
        "Session Type",
        options=["general", "homework_help", "study_session", "test_prep"],
        format_func=lambda x: x.replace('_', ' ').title(),
        key="session_type_selector"
    )

# Initialize chat messages in session state
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []

if 'chat_session_id' not in st.session_state:
    st.session_state.chat_session_id = None

# Load existing session if needed
if st.session_state.current_session and st.session_state.chat_session_id != st.session_state.current_session:
    st.session_state.chat_session_id = st.session_state.current_session
    
    # Load messages from database
    session_manager = st.session_state.conversation_handler.session_manager
    messages = session_manager.get_session_messages(st.session_state.chat_session_id)
    
    st.session_state.chat_messages = [
        {
            "role": msg.role,
            "content": msg.content,
            "timestamp": msg.timestamp
        }
        for msg in messages
    ]

# Sidebar with session options
with st.sidebar:
    st.markdown("### ▸ Chat Options")
    
    if st.button("↻ New Conversation", use_container_width=True, type="primary"):
        st.session_state.chat_messages = []
        st.session_state.chat_session_id = None
        st.session_state.current_session = None
        st.rerun()
    
    st.markdown("---")
    
    # Quick prompts
    st.markdown("### ▸ Quick Start")
    
    if st.button("▸ Help with Homework", use_container_width=True, type="primary"):
        st.session_state.chat_input = "I need help with a homework problem."
    
    if st.button("▸ Study a Topic", use_container_width=True, type="primary"):
        st.session_state.chat_input = "I want to study a specific topic."
    
    if st.button("▸ Practice Problems", use_container_width=True, type="primary"):
        st.session_state.chat_input = "Can you give me some practice problems?"
    
    if st.button("▸ Test Preparation", use_container_width=True, type="primary"):
        st.session_state.chat_input = "I have a test coming up and need help preparing."
    
    st.markdown("---")
    
    # Chat History - Enhanced Display
    st.markdown("### ▸ Chat History")
    st.caption("Click to load previous conversations")
    
    student_id = st.session_state.current_student.id
    session_manager = st.session_state.conversation_handler.session_manager
    recent_sessions = session_manager.get_student_sessions(student_id, limit=10)
    
    if recent_sessions:
        for i, session in enumerate(recent_sessions):
            # Format session display
            session_label = session.topic or 'General Chat'
            session_time = session.start_time.strftime('%m/%d %I:%M %p')
            
            # Show current session with indicator
            is_current = (st.session_state.chat_session_id == session.id)
            
            with st.container():
                col_btn, col_info = st.columns([3, 1])
                
                with col_btn:
                    button_label = f"{'▶ ' if is_current else '▸ '}{session_label}"
                    if st.button(
                        button_label,
                        key=f"load_session_{session.id}",
                        use_container_width=True,
                        type="primary" if is_current else "secondary"
                    ):
                        st.session_state.current_session = session.id
                        st.rerun()
                
                with col_info:
                    st.caption(session_time)
    else:
        st.info("No previous chats yet")

# Display chat messages
st.markdown("---")

chat_container = st.container()

with chat_container:
    if not st.session_state.chat_messages:
        st.info(
            "👋 Hi! I'm your AI math tutor. I'm here to help you learn and understand math.\n\n"
            "You can ask me questions, work through problems together, or request study materials.\n\n"
            "What would you like to work on today?"
        )
    else:
        for message in st.session_state.chat_messages:
            role = message["role"]
            content = message["content"]
            
            if role == "student":
                with st.chat_message("user", avatar="👤"):
                    st.markdown(content)
            else:
                with st.chat_message("assistant", avatar="🤓"):
                    st.markdown(content)

# Chat input section
st.markdown("---")

# File upload section with "+" button
col_upload, col_input_area = st.columns([1, 10])

with col_upload:
    # Initialize upload state
    if 'show_upload' not in st.session_state:
        st.session_state.show_upload = False
    
    # "Upload" button to toggle upload with custom HTML for visibility
    upload_html = """
    <style>
    .upload-btn {
        background-color: #f3f4f6;
        color: #000000;
        border: 2px solid #9ca3af;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        font-size: 0.9rem;
        cursor: pointer;
        text-align: center;
        transition: all 0.2s;
        width: 100%;
    }
    .upload-btn:hover {
        background-color: #e5e7eb;
        border-color: #667eea;
    }
    </style>
    """
    st.markdown(upload_html, unsafe_allow_html=True)
    
    if st.button("Upload", key="upload_toggle", help="Upload files (images, PDFs, etc.)", use_container_width=True, type="secondary"):
        st.session_state.show_upload = not st.session_state.show_upload

# Show file uploader if toggled
if st.session_state.show_upload:
    st.markdown("### ▸ Upload Files")
    st.caption("▸ Mobile | Desktop | Camera - Multiple upload methods supported")
    
    # Create tabs for different upload methods
    tab1, tab2 = st.tabs(["▸ Choose Files", "▸ Upload Tips"])
    
    with tab1:
        # Drag and drop file uploader
        uploaded_files = st.file_uploader(
            "Drag and drop files here, or click to browse",
            type=["png", "jpg", "jpeg", "pdf", "txt", "doc", "docx", "heic"],
            accept_multiple_files=True,
            key="file_uploader",
            help="📱 On mobile: Tap to access camera or photo library\n💻 On desktop: Drag & drop or browse files"
        )
        
        if uploaded_files:
            st.success(f"✅ Successfully uploaded {len(uploaded_files)} file(s)")
            
            # Display uploaded files with previews
            st.markdown("#### Uploaded Files:")
            cols = st.columns(min(len(uploaded_files), 3))
            
            for idx, file in enumerate(uploaded_files):
                with cols[idx % 3]:
                    with st.container():
                        st.markdown(f"**{file.name}**")
                        st.caption(f"Size: {file.size // 1024} KB")
                        
                        # Show image preview for image files
                        if file.type.startswith('image'):
                            st.image(file, use_container_width=True)
                        else:
                            st.info(f"📄 {file.type.split('/')[-1].upper()}")
                        
                        # Individual action buttons
                        col_a, col_b = st.columns(2)
                        with col_a:
                            if st.button("✍️ Ask", key=f"ask_{idx}", use_container_width=True):
                                st.session_state.chat_input = f"I uploaded '{file.name}'. Can you help me understand this problem?"
                                st.session_state.show_upload = False
                                st.rerun()
                        
                        with col_b:
                            if st.button("× Remove", key=f"remove_{idx}", use_container_width=True):
                                st.info("Refresh to clear files")
            
            # Bulk action
            st.markdown("---")
            if st.button("▸ Ask about all files", type="primary", use_container_width=True):
                file_names = ", ".join([f.name for f in uploaded_files])
                st.session_state.chat_input = f"I've uploaded {len(uploaded_files)} files: {file_names}. Can you help me with these?"
                st.session_state.show_upload = False
                st.rerun()
    
    with tab2:
        st.markdown("""
        **📱 Mobile Upload:**
        - Tap the upload button to access camera or photo library
        - Take a photo directly or choose from gallery
        - Supports multiple file selection
        
        **💻 Desktop Upload:**
        - **Drag & Drop**: Simply drag files into the upload area
        - **Browse**: Click to open file browser
        - **Multi-select**: Hold Ctrl/Cmd to select multiple files
        
        **Supported File Types:**
        - 📸 Images: PNG, JPG, JPEG, HEIC
        - 📄 Documents: PDF, TXT, DOC, DOCX
        
        **Best Practices:**
        - ✅ Clear, well-lit photos
        - ✅ Full problem visible
        - ✅ Straight angle (not tilted)
        - ✅ High enough resolution to read text
        """)
    
    st.markdown("---")

# Use session state for input if set by quick start buttons
default_input = st.session_state.get('chat_input', '')
if default_input:
    del st.session_state.chat_input

user_input = st.chat_input(
    "Type your message here... (Click + to upload files)",
    key="chat_input_box"
)

# Handle default input from quick start
if default_input and not user_input:
    user_input = default_input

# Process user input
if user_input:
    # Add user message to display
    st.session_state.chat_messages.append({
        "role": "student",
        "content": user_input,
        "timestamp": datetime.now()
    })
    
    # Show user message immediately
    with chat_container:
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)
    
    # Show thinking indicator
    with chat_container:
        with st.chat_message("assistant", avatar="🤓"):
            with st.spinner("Thinking..."):
                # Get AI response
                try:
                    response = st.session_state.conversation_handler.handle_message(
                        student_id=st.session_state.current_student.id,
                        message=user_input,
                        session_id=st.session_state.chat_session_id,
                        session_type=session_type
                    )
                    
                    if response["success"]:
                        # Update session ID
                        st.session_state.chat_session_id = response["session_id"]
                        st.session_state.current_session = response["session_id"]
                        
                        # Add tutor response to display
                        st.session_state.chat_messages.append({
                            "role": "tutor",
                            "content": response["response"],
                            "timestamp": response["timestamp"]
                        })
                        
                        # Display response
                        st.markdown(response["response"])
                        
                        # Show token usage
                        with st.expander("▸ Response Info"):
                            st.caption(f"Tokens used: {response['tokens_used']}")
                    else:
                        st.error(f"Error: {response['error']}")
                
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
    
    # Rerun to update chat display
    st.rerun()

# Tips section
with st.expander("▸ Tips for Getting Help"):
    st.markdown("""
    **How to ask for help:**
    - Describe the problem clearly
    - Show any work you've already done
    - Ask specific questions about what you don't understand
    
    **What I can help with:**
    - Explaining concepts in simple terms
    - Walking through problems step-by-step
    - Providing practice problems
    - Test preparation strategies
    - Homework guidance (I'll guide you, not just give answers!)
    
    **Math formatting:**
    - Use ^ for exponents: x^2
    - Use / for fractions: 3/4
    - I'll show equations in proper math notation
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 0.8rem;'>"
    "Remember: Making mistakes is part of learning! Ask as many questions as you need."
    "</div>",
    unsafe_allow_html=True
)

