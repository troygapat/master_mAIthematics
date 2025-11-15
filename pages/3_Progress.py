"""
Progress Page - Track student progress and analytics
"""

import streamlit as st
import sys
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(
    page_title="Progress - AI Math Tutor",
    page_icon="↗",
    layout="wide"
)

# Check if student is selected
if 'current_student' not in st.session_state or st.session_state.current_student is None:
    st.warning("Please select or create a student profile first!")
    if st.button("Go to Home"):
        st.switch_page("app.py")
    st.stop()

st.markdown("# ↗ Your Progress")
st.markdown(f"**Student:** {st.session_state.current_student.name} (Grade {st.session_state.current_student.grade_level})")

# Get student data
student_id = st.session_state.current_student.id
student_manager = st.session_state.student_manager
db_manager = st.session_state.db_manager

# Get comprehensive summary
summary = student_manager.get_student_summary(student_id)

if not summary or summary["statistics"]["total_sessions"] == 0:
    st.info("Start learning to see your progress here!")
    st.markdown("### ▸ Get Started")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▸ Start Chatting", use_container_width=True, type="primary"):
            st.switch_page("pages/1_Chat.py")
    with col2:
        if st.button("▸ Practice Problems", use_container_width=True, type="primary"):
            st.switch_page("pages/2_Practice.py")
    st.stop()

# Overview metrics
st.markdown("## ▸ Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Sessions",
        summary["statistics"]["total_sessions"],
        help="Number of tutoring sessions completed"
    )

with col2:
    st.metric(
        "Total Messages",
        summary["statistics"]["total_messages"],
        help="Total messages exchanged with tutor"
    )

with col3:
    st.metric(
        "Topics Worked",
        summary["statistics"]["topics_worked"],
        help="Number of different topics practiced"
    )

with col4:
    # Calculate average accuracy
    progress_records = db_manager.get_student_progress(student_id)
    if progress_records:
        avg_accuracy = sum(p.accuracy for p in progress_records) / len(progress_records)
        st.metric(
            "Avg. Accuracy",
            f"{round(avg_accuracy * 100)}%",
            help="Average accuracy across all topics"
        )
    else:
        st.metric("Avg. Accuracy", "N/A")

st.markdown("---")

# Topic mastery section
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("## ▸ Topic Mastery")
    
    if progress_records:
        # Create dataframe for visualization
        progress_data = []
        for prog in progress_records:
            progress_data.append({
                "Topic": prog.topic,
                "Subtopic": prog.subtopic or "",
                "Accuracy": prog.accuracy * 100,
                "Attempts": prog.attempts,
                "Skill Level": prog.skill_level,
                "Last Practiced": prog.last_practiced
            })
        
        df = pd.DataFrame(progress_data)
        
        # Sort by accuracy
        df = df.sort_values("Accuracy", ascending=True)
        
        # Create horizontal bar chart
        fig = px.bar(
            df,
            y="Topic",
            x="Accuracy",
            orientation='h',
            color="Accuracy",
            color_continuous_scale=["#ff4444", "#ffaa00", "#44ff44"],
            range_color=[0, 100],
            title="Accuracy by Topic",
            labels={"Accuracy": "Accuracy (%)"}
        )
        
        fig.update_layout(
            height=400,
            showlegend=False,
            xaxis_range=[0, 100]
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed topic breakdown
        st.markdown("### 📋 Detailed Breakdown")
        
        for i, row in df.iterrows():
            with st.expander(f"{row['Topic']} - {row['Accuracy']:.0f}% ({row['Skill Level'].title()})"):
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    st.metric("Accuracy", f"{row['Accuracy']:.1f}%")
                
                with col_b:
                    st.metric("Attempts", int(row['Attempts']))
                
                with col_c:
                    st.metric("Skill Level", row['Skill Level'].title())
                
                st.caption(f"Last practiced: {row['Last Practiced'].strftime('%m/%d/%Y %I:%M %p')}")
                
                # Quick action
                if st.button(f"Practice {row['Topic']}", key=f"practice_{i}"):
                    st.session_state.practice_topic = row['Topic']
                    st.switch_page("pages/2_Practice.py")
    else:
        st.info("No progress data yet. Start practicing to track your progress!")

with col2:
    st.markdown("## ▸ Skill Levels")
    
    if progress_records:
        # Count skill levels
        skill_counts = {}
        for prog in progress_records:
            level = prog.skill_level
            skill_counts[level] = skill_counts.get(level, 0) + 1
        
        # Create pie chart
        fig = go.Figure(data=[go.Pie(
            labels=list(skill_counts.keys()),
            values=list(skill_counts.values()),
            hole=.3,
            marker=dict(colors=['#ff6b6b', '#ffd93d', '#6bcf7f', '#4ecdc4'])
        )])
        
        fig.update_layout(
            title="Topics by Skill Level",
            height=300,
            showlegend=True,
            legend=dict(orientation="v")
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Skill level legend
        st.markdown("**Skill Levels:**")
        st.markdown("""
        - 🔴 **Beginner** - Just starting
        - 🟡 **Developing** - Making progress
        - 🟢 **Proficient** - Strong understanding
        - 🔵 **Advanced** - Mastery level
        """)
    else:
        st.info("Progress data will appear here")

# Recent activity timeline
st.markdown("---")
st.markdown("## ▸ Recent Activity")

recent_sessions = summary["recent_sessions"]

if recent_sessions:
    for session in recent_sessions:
        session_date = session['start_time'].strftime('%B %d, %Y at %I:%M %p')
        
        with st.container():
            col_a, col_b, col_c = st.columns([2, 1, 1])
            
            with col_a:
                st.markdown(f"**{session['topic'] or 'General Session'}**")
                st.caption(session_date)
            
            with col_b:
                st.caption(f"Type: {session['session_type'].replace('_', ' ').title()}")
            
            with col_c:
                st.caption(f"Messages: {session['message_count']}")
            
            if st.button("View Session", key=f"view_session_{session['id']}"):
                st.session_state.current_session = session['id']
                st.switch_page("pages/1_Chat.py")
        
        st.markdown("---")
else:
    st.info("No sessions yet")

# Study recommendations
st.markdown("## ▸ Recommendations")

if progress_records:
    # Find topics that need work (lowest accuracy)
    weak_topics = sorted(progress_records, key=lambda x: x.accuracy)[:3]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### ▸ Focus On")
        for prog in weak_topics:
            st.markdown(f"**{prog.topic}**")
            st.progress(prog.accuracy)
            st.caption(f"{round(prog.accuracy * 100)}% accuracy")
    
    with col2:
        st.markdown("### ⚡ Quick Wins")
        # Topics close to mastery (70-85% accuracy)
        almost_there = [p for p in progress_records if 0.70 <= p.accuracy < 0.85]
        if almost_there:
            for prog in almost_there[:3]:
                st.markdown(f"**{prog.topic}**")
                st.caption(f"{round(prog.accuracy * 100)}% - Almost there!")
        else:
            st.info("Keep practicing!")
    
    with col3:
        st.markdown("### 🏆 Mastered")
        # High accuracy topics (>= 85%)
        mastered = [p for p in progress_records if p.accuracy >= 0.85]
        if mastered:
            for prog in mastered[:3]:
                st.markdown(f"**{prog.topic}** ✅")
                st.caption(f"{round(prog.accuracy * 100)}% accuracy")
        else:
            st.info("Keep working towards mastery!")

# Action buttons
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    if st.button("▸ Generate Practice for Weak Topics", type="primary", use_container_width=True):
        if progress_records:
            weakest = min(progress_records, key=lambda x: x.accuracy)
            st.session_state.practice_topic = weakest.topic
            st.switch_page("pages/2_Practice.py")
        else:
            st.warning("No progress data yet")

with col2:
    if st.button("▸ Ask Tutor for Study Plan", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Chat.py")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 0.8rem;'>"
    "Consistent practice is the key to mastery. Keep up the great work! 🌟"
    "</div>",
    unsafe_allow_html=True
)

