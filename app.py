"""
AI Math Tutor - Main Streamlit Application
High School Mathematics Tutoring System
"""

import streamlit as st
import os
from pathlib import Path

# Add src to path
import sys
sys.path.insert(0, str(Path(__file__).parent))

from src.database.db_manager import DatabaseManager
from src.ai.ai_client import AIClient
from src.core.student_manager import StudentManager
from src.core.conversation_handler import ConversationHandler
from src.utils.config import config

# Page configuration
st.set_page_config(
    page_title=config.app_name,
    page_icon="∫",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "AI Math Tutor - Designed by T.A.B."
    }
)

# Bluxstudio-Inspired Custom CSS
st.markdown("""
<style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container styling */
    .main {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
    }
    
    /* Header styling - Bluxstudio inspired */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 1rem;
        letter-spacing: -0.02em;
    }
    
    /* Subheader styling */
    .sub-header {
        font-size: 1.25rem;
        font-weight: 400;
        color: #6b7280;
        text-align: center;
        margin-bottom: 3rem;
        line-height: 1.6;
    }
    
    /* Button styling - Modern elevated look */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.875rem 2rem;
        font-weight: 600;
        font-size: 0.95rem;
        border-radius: 12px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        letter-spacing: 0.01em;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:active {
        transform: translateY(-1px);
    }
    
    
    /* Card styling - Clean and elevated */
    .element-container {
        transition: all 0.3s ease;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Metric styling - Bluxstudio inspired */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.875rem;
        font-weight: 500;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Sidebar styling - Fixed visibility */
    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 2px solid #e5e7eb;
    }
    
    [data-testid="stSidebar"] * {
        color: #1f2937 !important;
    }
    
    [data-testid="stSidebar"] .element-container {
        transition: all 0.2s ease;
    }
    
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4 {
        color: #667eea !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stMetricLabel"] {
        color: #6b7280 !important;
        font-size: 0.75rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stMetricValue"] {
        color: #667eea !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    
    /* ULTRA CRITICAL: Sidebar form inputs - NUCLEAR OPTION WITH FORCED LIGHT MODE */
    [data-testid="stSidebar"] .stTextInput>div>div>input,
    [data-testid="stSidebar"] .stSelectbox>div>div>select,
    [data-testid="stSidebar"] .stTextInput input,
    [data-testid="stSidebar"] .stSelectbox select,
    [data-testid="stSidebar"] input[type="text"],
    [data-testid="stSidebar"] input[type="email"],
    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] select,
    [data-testid="stSidebar"] textarea,
    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] select,
    aside[data-testid="stSidebar"] input,
    aside[data-testid="stSidebar"] select {
        background-color: #ffffff !important;
        background: #ffffff !important;
        background-image: none !important;
        color: #1f2937 !important;
        border: 2px solid #d1d5db !important;
        font-weight: 500 !important;
        padding: 0.5rem !important;
        -webkit-text-fill-color: #1f2937 !important;
        appearance: none !important;
        -webkit-appearance: none !important;
        -moz-appearance: none !important;
    }
    
    /* FORCE white background on wrapper divs too */
    [data-testid="stSidebar"] .stTextInput>div>div,
    [data-testid="stSidebar"] .stSelectbox>div>div,
    [data-testid="stSidebar"] .stTextInput>div,
    [data-testid="stSidebar"] .stSelectbox>div {
        background-color: transparent !important;
    }
    
    [data-testid="stSidebar"] input::placeholder,
    [data-testid="stSidebar"] .stTextInput input::placeholder {
        color: #9ca3af !important;
        opacity: 1 !important;
        -webkit-text-fill-color: #9ca3af !important;
    }
    
    [data-testid="stSidebar"] input:focus,
    [data-testid="stSidebar"] select:focus,
    [data-testid="stSidebar"] .stTextInput input:focus,
    [data-testid="stSidebar"] .stSelectbox select:focus {
        background-color: #ffffff !important;
        background: #ffffff !important;
        color: #1f2937 !important;
        border-color: #667eea !important;
        outline: none !important;
        -webkit-text-fill-color: #1f2937 !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2) !important;
    }
    
    /* Sidebar selectbox dropdown */
    [data-testid="stSidebar"] option,
    [data-testid="stSidebar"] select option {
        background-color: #ffffff !important;
        background: #ffffff !important;
        color: #1f2937 !important;
    }
    
    /* Sidebar form labels */
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stTextInput label,
    [data-testid="stSidebar"] .stSelectbox label {
        color: #1f2937 !important;
        font-weight: 600 !important;
    }
    
    /* Sidebar form button */
    [data-testid="stSidebar"] .stButton button,
    [data-testid="stSidebar"] button[type="submit"],
    [data-testid="stSidebar"] .stForm button {
        background-color: #667eea !important;
        background: #667eea !important;
        color: #ffffff !important;
        border: none !important;
        padding: 0.5rem 1rem !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stSidebar"] .stButton button:hover,
    [data-testid="stSidebar"] button[type="submit"]:hover {
        background-color: #764ba2 !important;
    }
    
    /* Input styling - FIXED CONTRAST */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>select {
        border-radius: 10px;
        border: 2px solid #e5e7eb;
        transition: all 0.3s ease;
        font-family: 'Inter', sans-serif;
        background-color: #ffffff !important;
        color: #1f2937 !important;
        font-weight: 500 !important;
    }
    
    .stTextInput>div>div>input::placeholder,
    .stTextArea>div>div>textarea::placeholder {
        color: #9ca3af !important;
        opacity: 1 !important;
    }
    
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus,
    .stSelectbox>div>div>select:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        background-color: #ffffff !important;
        color: #1f2937 !important;
    }
    
    /* Selectbox option text */
    .stSelectbox option {
        background-color: #ffffff !important;
        color: #1f2937 !important;
    }
    
    /* Fix form submit button */
    .stForm button[type="submit"] {
        background-color: #ffffff !important;
        color: #1f2937 !important;
        border: 2px solid #e5e7eb !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        font-weight: 600;
        font-size: 1rem;
        border-radius: 10px;
        background-color: #f8f9fa;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #f3f4f6;
    }
    
    /* Info/Success/Warning boxes */
    .stAlert {
        border-radius: 12px;
        border: none;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    /* Chat message styling */
    .stChatMessage {
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    /* Remove Streamlit branding elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def init_database():
    """Initialize database connection"""
    db_manager = DatabaseManager()
    db_manager.create_tables()
    return db_manager


@st.cache_resource
def init_ai_client():
    """Initialize AI client"""
    try:
        return AIClient(
            model=config.ai_model,
            max_tokens=config.ai_max_tokens,
            temperature=config.ai_temperature
        )
    except Exception as e:
        st.error(f"Failed to initialize AI client: {str(e)}")
        st.info("Please set your ANTHROPIC_API_KEY in the .env file")
        st.stop()


def initialize_session_state():
    """Initialize Streamlit session state"""
    if 'db_manager' not in st.session_state:
        st.session_state.db_manager = init_database()
    
    if 'ai_client' not in st.session_state:
        st.session_state.ai_client = init_ai_client()
    
    if 'student_manager' not in st.session_state:
        st.session_state.student_manager = StudentManager(st.session_state.db_manager)
    
    if 'conversation_handler' not in st.session_state:
        st.session_state.conversation_handler = ConversationHandler(
            st.session_state.db_manager,
            st.session_state.ai_client
        )
    
    if 'current_student' not in st.session_state:
        st.session_state.current_student = None
    
    if 'current_session' not in st.session_state:
        st.session_state.current_session = None


def render_sidebar():
    """Render sidebar with student selection and navigation"""
    with st.sidebar:
        # Modern sidebar header
        st.markdown("""
        <div style='text-align: center; padding: 1.5rem 0 1rem 0; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    margin: -1rem -1rem 1.5rem -1rem; border-radius: 0;'>
            <h2 style='margin: 0; font-size: 1.4rem; font-weight: 700; line-height: 1.3;'>
                <span style='color: white; font-size: 1.8rem; display: block; margin-bottom: 0.25rem;'>∫</span>
                <span style='color: white;'>master m</span><span style='color: #fff176; font-weight: 900;'>AI</span><span style='color: white;'>thematics</span>
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Student selection/creation
        st.markdown("### ▸ Student Profile")
        
        students = st.session_state.student_manager.get_all_students()
        
        if students:
            student_options = {f"{s.name} (Grade {s.grade_level})": s.id for s in students}
            student_options["+ Create New Student"] = None
            
            selected = st.selectbox(
                "Select Student",
                options=list(student_options.keys()),
                key="student_selector",
                label_visibility="collapsed"
            )
            
            if selected == "+ Create New Student":
                st.session_state.current_student = None
            else:
                student_id = student_options[selected]
                if not st.session_state.current_student or st.session_state.current_student.id != student_id:
                    st.session_state.current_student = st.session_state.student_manager.get_student(student_id)
        else:
            st.info("No students yet. Create your first student below!")
            st.session_state.current_student = None
        
        # Create new student
        if st.session_state.current_student is None:
            st.markdown("#### Create New Student")
            with st.form("create_student"):
                name = st.text_input("Name")
                grade = st.selectbox(
                    "Grade Level",
                    options=[9, 10, 11, 12],
                    format_func=lambda x: f"Grade {x}"
                )
                email = st.text_input("Email (optional)")
                
                submit = st.form_submit_button("Create Student")
                
                if submit and name:
                    try:
                        student = st.session_state.student_manager.create_student(
                            name=name,
                            grade_level=grade,
                            email=email if email else None
                        )
                        st.session_state.current_student = student
                        st.success(f"Welcome, {name}!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error creating student: {str(e)}")
        
        # Show current student info with modern styling
        if st.session_state.current_student:
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Student info card
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea10 0%, #764ba210 100%); 
                        padding: 1.25rem; border-radius: 12px; margin-bottom: 1.5rem;
                        border-left: 4px solid #667eea;'>
                <h4 style='color: #667eea; margin: 0 0 0.75rem 0; font-size: 0.875rem; 
                           text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;'>
                    ● Current Student
                </h4>
                <p style='color: #1f2937; margin: 0; font-size: 1.1rem; font-weight: 700;'>
                    {st.session_state.current_student.name}
                </p>
                <p style='color: #6b7280; margin: 0.25rem 0 0 0; font-size: 0.9rem;'>
                    Grade {st.session_state.current_student.grade_level}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Quick stats with better visibility
            summary = st.session_state.student_manager.get_student_summary(
                st.session_state.current_student.id
            )
            if summary:
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Sessions", summary["statistics"]["total_sessions"])
                with col2:
                    st.metric("Topics Worked", summary["statistics"]["topics_worked"])
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Navigation with modern styling
        st.markdown("""
        <div style='background: #f8f9fa; padding: 1rem; border-radius: 10px; margin-top: 1rem;'>
            <h4 style='color: #667eea; margin: 0 0 0.75rem 0; font-size: 0.875rem; 
                       text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;'>
                ≡ Navigation
            </h4>
            <p style='color: #1f2937; margin: 0.5rem 0; font-size: 0.9rem;'>
                • <strong>Chat</strong> - Talk with your tutor
            </p>
            <p style='color: #1f2937; margin: 0.5rem 0; font-size: 0.9rem;'>
                • <strong>Practice</strong> - Work on problems
            </p>
            <p style='color: #1f2937; margin: 0.5rem 0; font-size: 0.9rem;'>
                • <strong>Progress</strong> - View your stats
            </p>
        </div>
        """, unsafe_allow_html=True)


def render_home_page():
    """Render the home page - Bluxstudio inspired"""
    
    # Hero Section - DRAMATIC with Real Platonic Solid Images (ONE LINE)
    hero_html = """<div style='text-align: center; padding: 3rem 2rem; background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%); margin: -2rem -2rem 2rem -2rem; border-bottom: 1px solid #e5e7eb; overflow-x: auto;'><div style='max-width: 1400px; margin: 0 auto; display: flex; align-items: center; justify-content: center; gap: 3rem; flex-wrap: nowrap; min-width: fit-content;'><div style='flex-shrink: 0;'><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Dodecahedron.svg/240px-Dodecahedron.svg.png' alt='Dodecahedron' style='width: 120px; height: 120px; opacity: 0.75; filter: hue-rotate(240deg) saturate(1.4);' /></div><div style='flex: 0 1 auto; white-space: nowrap;'><h1 style='font-size: clamp(2.5rem, 5vw, 4rem); font-weight: 800; margin: 0; letter-spacing: -0.04em; line-height: 1; margin-bottom: 1rem;'><span style='color: #1f2937;'>master m</span><span style='font-weight: 900; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;'>AI</span><span style='color: #1f2937;'>thematics</span></h1><p style='font-size: clamp(0.9rem, 1.5vw, 1.15rem); color: #6b7280; font-weight: 400; line-height: 1.6; margin: 0;'>We're here to help you succeed • Designed by T.A.B.</p></div><div style='flex-shrink: 0;'><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Dodecahedron.svg/240px-Dodecahedron.svg.png' alt='Dodecahedron' style='width: 120px; height: 120px; opacity: 0.75; filter: hue-rotate(280deg) saturate(1.3);' /></div></div></div>"""
    
    st.markdown(hero_html, unsafe_allow_html=True)
    
    if st.session_state.current_student is None:
        # CTA Section
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.info("← Create or select a student profile in the sidebar to get started")
        
        # Feature Cards - DRAMATIC Bluxstudio style
        st.markdown("""
        <div style='text-align: center; margin: 3rem 0 2.5rem 0;'>
            <h2 style='font-size: 2.25rem; font-weight: 800; color: #1f2937; 
                       margin-bottom: 0.75rem; letter-spacing: -0.03em;'>
                Everything You Need to Excel
            </h2>
            <p style='font-size: 1.15rem; color: #6b7280; font-weight: 400; line-height: 1.6;'>
                Powerful AI tools designed for high school mathematics
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3, gap="large")
        
        with col1:
            st.markdown("""
            <div style='background: white; padding: 2.25rem; border-radius: 18px; height: 100%;
                        border: 2px solid #e5e7eb; box-shadow: 0 4px 16px rgba(0,0,0,0.06);
                        transition: all 0.3s ease;'>
                <div style='width: 60px; height: 60px; border-radius: 14px;
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            display: flex; align-items: center; justify-content: center;
                            font-size: 2rem; margin-bottom: 1.5rem; box-shadow: 0 4px 12px rgba(102,126,234,0.3);
                            color: white; font-weight: 700;'>💬</div>
                <h3 style='font-size: 1.35rem; font-weight: 800; color: #1f2937; 
                           margin-bottom: 0.85rem; letter-spacing: -0.01em;'>Interactive Chat</h3>
                <p style='color: #6b7280; font-size: 1rem; line-height: 1.7; margin-bottom: 1.25rem;'>
                    Get instant help with homework, concepts, and problem-solving through natural conversation.
                </p>
                <ul style='color: #6b7280; font-size: 0.925rem; padding-left: 1.5rem; margin: 0; line-height: 1.8;'>
                    <li style='margin-bottom: 0.6rem;'><strong>Real-time</strong> explanations</li>
                    <li style='margin-bottom: 0.6rem;'><strong>Step-by-step</strong> guidance</li>
                    <li><strong>Upload</strong> problem images</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background: white; padding: 2.25rem; border-radius: 18px; height: 100%;
                        border: 2px solid #e5e7eb; box-shadow: 0 4px 16px rgba(0,0,0,0.06);
                        transition: all 0.3s ease;'>
                <div style='width: 60px; height: 60px; border-radius: 14px;
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            display: flex; align-items: center; justify-content: center;
                            font-size: 2rem; margin-bottom: 1.5rem; box-shadow: 0 4px 12px rgba(102,126,234,0.3);
                            color: white; font-weight: 700;'>✎</div>
                <h3 style='font-size: 1.35rem; font-weight: 800; color: #1f2937; 
                           margin-bottom: 0.85rem; letter-spacing: -0.01em;'>Practice Problems</h3>
                <p style='color: #6b7280; font-size: 1rem; line-height: 1.7; margin-bottom: 1.25rem;'>
                    Work through AI-generated problem sets perfectly tailored to your skill level.
                </p>
                <ul style='color: #6b7280; font-size: 0.925rem; padding-left: 1.5rem; margin: 0; line-height: 1.8;'>
                    <li style='margin-bottom: 0.6rem;'><strong>Custom</strong> difficulty levels</li>
                    <li style='margin-bottom: 0.6rem;'><strong>Instant</strong> hints & solutions</li>
                    <li><strong>Individual</strong> workspaces</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style='background: white; padding: 2.25rem; border-radius: 18px; height: 100%;
                        border: 2px solid #e5e7eb; box-shadow: 0 4px 16px rgba(0,0,0,0.06);
                        transition: all 0.3s ease;'>
                <div style='width: 60px; height: 60px; border-radius: 14px;
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            display: flex; align-items: center; justify-content: center;
                            font-size: 2rem; margin-bottom: 1.5rem; box-shadow: 0 4px 12px rgba(102,126,234,0.3);
                            color: white; font-weight: 700;'>↗</div>
                <h3 style='font-size: 1.35rem; font-weight: 800; color: #1f2937; 
                           margin-bottom: 0.85rem; letter-spacing: -0.01em;'>Progress Tracking</h3>
                <p style='color: #6b7280; font-size: 1rem; line-height: 1.7; margin-bottom: 1.25rem;'>
                    Monitor your improvement with detailed analytics and personalized insights.
                </p>
                <ul style='color: #6b7280; font-size: 0.925rem; padding-left: 1.5rem; margin: 0; line-height: 1.8;'>
                    <li style='margin-bottom: 0.6rem;'><strong>Performance</strong> analytics</li>
                    <li style='margin-bottom: 0.6rem;'><strong>Topic mastery</strong> tracking</li>
                    <li><strong>Visual</strong> progress reports</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Topics Covered
        st.markdown("## ∑ Comprehensive Topic Coverage")
        st.caption("Master everything from Algebra to Calculus")
        
        topics = config.topics
        
        col1, col2 = st.columns(2)
        
        with col1:
            for category in list(topics.keys())[:3]:
                with st.expander(f"▸ {category.replace('_', ' ').title()}", expanded=False):
                    for topic in topics[category]:
                        st.write(f"• {topic}")
        
        with col2:
            for category in list(topics.keys())[3:]:
                with st.expander(f"▸ {category.replace('_', ' ').title()}", expanded=False):
                    for topic in topics[category]:
                        st.write(f"• {topic}")
    
    else:
        # Student is logged in - Modern dashboard
        student = st.session_state.current_student
        
        # Welcome message - Bluxstudio style
        st.markdown(f"""
        <div style='text-align: center; padding: 2.5rem 1.5rem 1.5rem 1.5rem;'>
            <h1 style='font-size: 2.5rem; font-weight: 700; color: #1f2937; 
                       letter-spacing: -0.02em; margin-bottom: 0.5rem;'>
                Welcome back, {student.name}
            </h1>
            <p style='font-size: 1.1rem; color: #6b7280; font-weight: 400;'>
                Grade {student.grade_level} • Ready to continue your math journey?
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick action buttons
        col1, col2, col3, col4 = st.columns([1, 1.5, 1.5, 1])
        with col2:
            if st.button("▶ Start Tutoring Session", use_container_width=True, type="primary"):
                st.switch_page("pages/1_Chat.py")
        with col3:
            if st.button("✎ Practice Problems", use_container_width=True):
                st.switch_page("pages/2_Practice.py")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Get student summary
        summary = st.session_state.student_manager.get_student_summary(student.id)
        
        if summary:
            # Stats cards - Modern metrics
            st.markdown("""
            <div style='text-align: center; margin-bottom: 1.5rem;'>
                <h2 style='font-size: 1.75rem; font-weight: 700; color: #1f2937;'>Your Stats</h2>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Sessions", summary["statistics"]["total_sessions"], help="Number of tutoring sessions")
            
            with col2:
                st.metric("Messages Sent", summary["statistics"]["total_messages"], help="Total messages in chat")
            
            with col3:
                st.metric("Topics Practiced", summary["statistics"]["topics_worked"], help="Unique topics you've worked on")
            
            with col4:
                st.metric("Grade Level", f"Grade {student.grade_level}", help="Your current grade")
            
            st.markdown("---")
            
            # Recent activity
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("### ◉ Recent Sessions")
                if summary["recent_sessions"]:
                    for session in summary["recent_sessions"][:5]:
                        with st.expander(
                            f"{session['topic'] or 'General Session'} - "
                            f"{session['start_time'].strftime('%m/%d %I:%M %p')}"
                        ):
                            st.write(f"**Type:** {session['session_type'].replace('_', ' ').title()}")
                            st.write(f"**Messages:** {session['message_count']}")
                            
                            if st.button(f"Continue Session", key=f"continue_{session['id']}"):
                                st.session_state.current_session = session['id']
                                st.switch_page("pages/1_Chat.py")
                else:
                    st.info("No sessions yet. Start chatting to begin!")
            
            with col2:
                st.markdown("### ↗ Progress Overview")
                if summary["progress"]:
                    for prog in summary["progress"][:5]:
                        st.write(f"**{prog['topic']}**")
                        st.progress(prog['accuracy'] / 100)
                        st.caption(f"{prog['accuracy']}% • {prog['skill_level']}")
                else:
                    st.info("Start practicing to track progress!")
        
        # Quick actions
        st.markdown("---")
        st.markdown("## ▸ Quick Actions")
        st.caption("Jump right into learning")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### ▶ Start Chatting")
            st.write("Ask questions and get help")
            if st.button("▶ Launch Chat", key="btn_chat", use_container_width=True, type="primary"):
                st.switch_page("pages/1_Chat.py")
        
        with col2:
            st.markdown("#### ▸ Practice Problems")
            st.write("Sharpen your skills")
            if st.button("▸ Start Practicing", key="btn_practice", use_container_width=True, type="primary"):
                st.switch_page("pages/2_Practice.py")
        
        with col3:
            st.markdown("#### ↗ View Progress")
            st.write("Track your improvement")
            if st.button("↗ See Analytics", key="btn_progress", use_container_width=True, type="primary"):
                st.switch_page("pages/3_Progress.py")


def main():
    """Main application entry point"""
    # Initialize
    initialize_session_state()
    
    # Render sidebar
    render_sidebar()
    
    # Render home page
    render_home_page()
    
    # Footer - Bluxstudio style
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; color: #9ca3af; font-size: 0.9rem; 
                padding: 2rem 0 1.5rem 0; border-top: 1px solid #e5e7eb; margin-top: 3rem;'>
        <strong style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                       background-clip: text; font-weight: 700;'>AI Math Tutor</strong> 
        <span style='color: #d1d5db;'>•</span> 
        Designed by <strong>Troy A. Brumfield</strong> 
        <span style='color: #d1d5db;'>•</span> 
        High School Mathematics
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

