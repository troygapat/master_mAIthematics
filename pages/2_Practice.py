"""
Practice Page - Practice problems and exercises
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.config import config
from src.utils.math_renderer import create_problem_card

st.set_page_config(
    page_title="Practice - AI Math Tutor",
    page_icon="▸",
    layout="wide"
)

# Check if student is selected
if 'current_student' not in st.session_state or st.session_state.current_student is None:
    st.warning("Please select or create a student profile first!")
    if st.button("Go to Home"):
        st.switch_page("app.py")
    st.stop()

st.markdown("# ▸ Practice Problems")
st.markdown(f"**Student:** {st.session_state.current_student.name}")

# Initialize practice state
if 'practice_problems' not in st.session_state:
    st.session_state.practice_problems = []

if 'current_problem_index' not in st.session_state:
    st.session_state.current_problem_index = 0

if 'show_solutions' not in st.session_state:
    st.session_state.show_solutions = {}

# Sidebar - Generate problems
with st.sidebar:
    st.markdown("### ▸ Generate Practice")
    
    # Topic selection
    topics_config = config.topics
    all_categories = list(topics_config.keys())
    
    selected_category = st.selectbox(
        "Subject Area",
        options=all_categories,
        format_func=lambda x: x.replace('_', ' ').title()
    )
    
    if selected_category:
        topics_in_category = topics_config[selected_category]
        selected_topic = st.selectbox(
            "Specific Topic",
            options=topics_in_category
        )
    else:
        selected_topic = None
    
    # Difficulty and count
    difficulty = st.select_slider(
        "Difficulty",
        options=["easy", "medium", "hard", "challenge"],
        value="medium"
    )
    
    problem_count = st.slider(
        "Number of Problems",
        min_value=3,
        max_value=10,
        value=5
    )
    
    # Generate button
    if st.button("▶ Generate Problems", type="primary", use_container_width=True):
        if selected_topic:
            with st.spinner(f"Generating {problem_count} problems... This may take 10-20 seconds"):
                try:
                    # Request practice problems from AI with optimized settings
                    ai_client = st.session_state.ai_client
                    from src.ai.ai_client import PromptBuilder
                    
                    # Build prompt
                    prompt_builder = PromptBuilder()
                    system_prompt = prompt_builder.build_system_prompt(
                        student_name=st.session_state.current_student.name,
                        grade_level=st.session_state.current_student.grade_level
                    )
                    
                    practice_prompt = prompt_builder.format_practice_request_prompt(
                        topic=selected_topic,
                        difficulty=difficulty,
                        count=problem_count
                    )
                    
                    # Generate with higher token limit for practice problems
                    response = ai_client.create_message(
                        system=system_prompt,
                        messages=[{"role": "user", "content": practice_prompt}],
                        max_tokens=3000  # Increased for multiple problems
                    )
                    
                    if response["content"]:
                        # Store the response content
                        st.session_state.practice_content = response["content"]
                        st.session_state.practice_topic = selected_topic
                        st.session_state.practice_difficulty = difficulty
                        st.success(f"{problem_count} problems generated successfully!")
                        st.rerun()
                    else:
                        st.error("No content received from AI")
                
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please select a topic first!")
    
    st.markdown("---")
    
    # View previous practice sets
    st.markdown("### ◉ Previous Practice")
    
    db_manager = st.session_state.db_manager
    materials = db_manager.get_study_materials(
        student_id=st.session_state.current_student.id,
        material_type="practice_set"
    )
    
    if materials:
        for material in materials[:5]:
            if st.button(
                f"{material.topic}",
                key=f"load_material_{material.id}",
                use_container_width=True
            ):
                st.session_state.practice_content = material.content.get("content", "")
                st.session_state.practice_topic = material.topic
                st.session_state.practice_difficulty = material.difficulty_level
                db_manager.increment_material_usage(material.id)
                st.rerun()
    else:
        st.info("No previous practice sets yet")

# Main content area
col1, col2 = st.columns([3, 1])

with col1:
    if 'practice_content' in st.session_state and st.session_state.practice_content:
        # Header with custom styling
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem;'>
            <h2 style='color: white; margin: 0;'>{st.session_state.practice_topic}</h2>
            <p style='color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 0.9rem;'>
                {st.session_state.current_student.name}'s Practice Set • 
                {st.session_state.practice_difficulty.title()} Level
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Parse problems and solutions from AI content
        import re
        content = st.session_state.practice_content
        
        # Split by Solutions heading
        split_patterns = [
            r'\n#+\s*Solutions?\s*\n',
            r'\n\*\*Solutions?\*\*\s*\n',
            r'\n##\s*Solutions?\s*\n',
            r'\nSOLUTIONS?\s*\n'
        ]
        
        problems_part = content
        solutions_part = None
        
        for pattern in split_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                problems_part = content[:match.start()]
                solutions_part = content[match.end():]
                break
        
        # Parse individual problems
        problem_pattern = r'\*\*Problem\s*(\d+)[:\.]?\*\*\s*(.*?)(?=\*\*Problem\s*\d+|\Z)'
        problems = re.findall(problem_pattern, problems_part, re.DOTALL | re.IGNORECASE)
        
        if not problems:
            # Fallback: try to split by numbers or dashes
            problem_splits = re.split(r'\n(?:\d+[\.\)]|\-{3,})\s*', problems_part)
            problems = [(str(i+1), prob.strip()) for i, prob in enumerate(problem_splits) if prob.strip()]
        
        # Parse solutions
        solutions_dict = {}
        if solutions_part:
            solution_pattern = r'\*\*(?:Problem\s*)?(\d+)[:\.]?\s*(?:Solution)?[:\.]?\*\*\s*(.*?)(?=\*\*(?:Problem\s*)?\d+|\Z)'
            solutions = re.findall(solution_pattern, solutions_part, re.DOTALL | re.IGNORECASE)
            solutions_dict = {num: sol.strip() for num, sol in solutions}
        
        # Initialize problem states
        if 'problem_completed' not in st.session_state:
            st.session_state.problem_completed = {}
        if 'show_solution' not in st.session_state:
            st.session_state.show_solution = {}
        if 'problem_feedback' not in st.session_state:
            st.session_state.problem_feedback = {}
        if 'answer_correct' not in st.session_state:
            st.session_state.answer_correct = {}
        
        # Display each problem in a custom card
        for idx, (prob_num, prob_text) in enumerate(problems):
            # Clean up problem text
            prob_text = re.sub(r'<br\s*/?>', '\n', prob_text.strip())
            prob_text = re.sub(r'<[^>]+>', '', prob_text)
            prob_text = re.sub(r'\*\*', '', prob_text)  # Remove markdown bold markers
            prob_text = re.sub(r'^[\-\_\*]{2,}', '', prob_text, flags=re.MULTILINE)  # Remove --- or *** lines
            prob_text = prob_text.strip()
            
            # Streamlined problem header
            st.markdown(f"""
            <div style='display: inline-flex; align-items: center; margin-bottom: 0.75rem; margin-top: 1.5rem;'>
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            color: white; width: 32px; height: 32px; border-radius: 8px; 
                            display: flex; align-items: center; justify-content: center; 
                            font-weight: 600; font-size: 1rem; margin-right: 0.75rem;'>
                    {prob_num}
                </div>
                <span style='font-size: 1.1rem; font-weight: 600; color: #667eea;'>Problem {prob_num}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Problem content - LARGER FONT
            st.markdown(f"""
            <div style='font-size: 1.15rem; line-height: 1.7; color: #1f2937; margin-bottom: 1rem; font-weight: 500;'>
                {prob_text}
            </div>
            """, unsafe_allow_html=True)
            
            # Interactive answer submission area
            problem_key = f"{prob_num}_{idx}"
            
            # Answer input
            col_answer, col_check = st.columns([3, 1])
            
            with col_answer:
                answer = st.text_input(
                    f"Your answer for Problem {prob_num}",
                    key=f"answer_{problem_key}",
                    placeholder="Type your final answer here...",
                    label_visibility="collapsed"
                )
            
            with col_check:
                check_button = st.button(
                    "Check",
                    key=f"check_{problem_key}",
                    use_container_width=True,
                    type="primary"
                )
            
            # Work area
            work = st.text_area(
                "Show your work (optional)",
                height=80,
                placeholder="Show your steps here...",
                key=f"work_{problem_key}",
                label_visibility="collapsed"
            )
            
            # Check answer with AI tutor
            if check_button and answer:
                with st.spinner("Checking your answer..."):
                    try:
                        ai_client = st.session_state.ai_client
                        from src.ai.ai_client import PromptBuilder
                        
                        # Get the solution for comparison
                        solution = solutions_dict.get(prob_num, "")
                        
                        # Build tutoring prompt
                        prompt_builder = PromptBuilder()
                        system_prompt = prompt_builder.build_system_prompt(
                            student_name=st.session_state.current_student.name,
                            grade_level=st.session_state.current_student.grade_level
                        )
                        
                        check_prompt = f"""I'm working on this problem:
{prob_text}

My answer: {answer}

{f"My work: {work}" if work else ""}

Can you check if my answer is correct? If it's right, confirm it briefly. If it's wrong, help me understand what I did wrong and guide me toward the correct answer. Don't just give me the answer - help me learn.

The correct solution is: {solution}"""
                        
                        response = ai_client.create_message(
                            system=system_prompt,
                            messages=[{"role": "user", "content": check_prompt}],
                            max_tokens=1000
                        )
                        
                        if response["content"]:
                            # Store feedback
                            st.session_state.problem_feedback[problem_key] = response["content"]
                            
                            # Check if correct (simple heuristic)
                            feedback_lower = response["content"].lower()
                            is_correct = any(word in feedback_lower[:200] for word in ["correct", "right", "exactly", "perfect", "yes"])
                            st.session_state.answer_correct[problem_key] = is_correct
                            
                            if is_correct:
                                st.session_state.problem_completed[problem_key] = True
                            
                            st.rerun()
                    
                    except Exception as e:
                        st.error(f"Error checking answer: {str(e)}")
            
            # Display feedback if exists
            if problem_key in st.session_state.problem_feedback:
                is_correct = st.session_state.answer_correct.get(problem_key, False)
                
                if is_correct:
                    st.markdown(f"""
                    <div style='background-color: #e8f5e9; padding: 1rem; 
                                border-radius: 8px; margin-top: 1rem; 
                                border-left: 4px solid #4caf50;'>
                        <strong style='color: #2e7d32;'>✓ Tutor Feedback:</strong>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style='background-color: #fff3e0; padding: 1rem; 
                                border-radius: 8px; margin-top: 1rem; 
                                border-left: 4px solid #ff9800;'>
                        <strong style='color: #e65100;'>▸ Tutor Feedback:</strong>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown(st.session_state.problem_feedback[problem_key])
            
            # Action buttons row
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                if st.button("Try Again", key=f"reset_{problem_key}", use_container_width=True):
                    # Clear feedback and answer
                    if problem_key in st.session_state.problem_feedback:
                        del st.session_state.problem_feedback[problem_key]
                    if problem_key in st.session_state.answer_correct:
                        del st.session_state.answer_correct[problem_key]
                    st.rerun()
            
            with col_b:
                # Show solution button
                if prob_num in solutions_dict:
                    if st.button(
                        "Show Solution" if not st.session_state.show_solution.get(problem_key) else "Hide Solution",
                        key=f"sol_btn_{problem_key}",
                        use_container_width=True,
                        type="secondary"
                    ):
                        st.session_state.show_solution[problem_key] = \
                            not st.session_state.show_solution.get(problem_key, False)
                        st.rerun()
            
            with col_c:
                if st.button("Ask Tutor", key=f"help_{problem_key}", use_container_width=True):
                    st.session_state.help_problem = prob_text
                    st.switch_page("pages/1_Chat.py")
            
            # Show solution if toggled
            if st.session_state.show_solution.get(problem_key) and prob_num in solutions_dict:
                solution_text = solutions_dict[prob_num]
                solution_text = re.sub(r'<br\s*/?>', '\n', solution_text)
                solution_text = re.sub(r'<[^>]+>', '', solution_text)
                
                st.markdown(f"""
                <div style='background-color: #f3f4f6; padding: 1rem; 
                            border-radius: 8px; margin-top: 1rem; 
                            border-left: 4px solid #667eea;'>
                    <strong style='color: #667eea;'>▸ Complete Solution:</strong>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(solution_text)
            
            st.markdown("<br>", unsafe_allow_html=True)
        
        # Progress summary
        completed_count = sum(1 for v in st.session_state.problem_completed.values() if v)
        total_count = len(problems)
        
        if total_count > 0:
            progress_pct = completed_count / total_count
            
            st.markdown("---")
            st.markdown("### ↗ Your Progress")
            
            col_prog1, col_prog2 = st.columns([3, 1])
            
            with col_prog1:
                st.progress(progress_pct)
            
            with col_prog2:
                st.metric("Completed", f"{completed_count}/{total_count}")
            
            if completed_count == total_count:
                st.success("Amazing! You've completed all problems!")
                st.balloons()
        
        # Action buttons
        st.markdown("---")
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            if st.button("▸ Ask Tutor", use_container_width=True, type="primary"):
                st.session_state.current_session = None
                st.switch_page("pages/1_Chat.py")
        
        with col_b:
            if st.button("↻ New Set", use_container_width=True, type="primary"):
                st.session_state.practice_content = None
                st.session_state.problem_completed = {}
                st.session_state.show_solution = {}
                st.session_state.problem_feedback = {}
                st.session_state.answer_correct = {}
                st.rerun()
        
        with col_c:
            if st.button("▸ Save Progress", use_container_width=True, type="primary"):
                st.success("Progress saved!")
    
    else:
        # No practice content yet
        st.info("← Select a topic and generate practice problems to get started")
        
        # Show example of what they can do
        st.markdown("### ▸ What You Can Practice")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("#### ▸ Types of Problems")
            st.markdown("""
            - Multiple choice questions
            - Short answer problems
            - Word problems
            - Step-by-step solutions
            - Challenge problems
            """)
        
        with col_b:
            st.markdown("#### ∑ Available Topics")
            for category in list(topics_config.keys())[:3]:
                topics = topics_config[category]
                st.markdown(f"**{category.replace('_', ' ').title()}**")
                for topic in topics[:3]:
                    st.markdown(f"• {topic}")

with col2:
    st.markdown("### ↗ Your Stats")
    
    # Get progress data
    progress_records = st.session_state.db_manager.get_student_progress(
        st.session_state.current_student.id
    )
    
    if progress_records:
        # Show recent topics
        st.markdown("#### Recent Topics")
        for prog in progress_records[:5]:
            st.metric(
                prog.topic,
                f"{round(prog.accuracy * 100)}%",
                f"{prog.attempts} attempts"
            )
    else:
        st.info("Start practicing to see your stats!")
    
    st.markdown("---")
    
    # Tips
    with st.expander("▸ Practice Tips"):
        st.markdown("""
        **How to practice effectively:**
        
        1. Start with easier problems
        2. Work through each step carefully
        3. Check your answers
        4. Review mistakes to learn
        5. Gradually increase difficulty
        
        **Don't forget:**
        - Show your work
        - Take your time
        - Ask for help when stuck
        - Practice regularly
        """)

# Footer
st.markdown("---")
st.markdown(
        "<div style='text-align: center; color: gray; font-size: 0.8rem;'>"
        "Practice makes progress. Every problem you solve makes you stronger."
        "</div>",
    unsafe_allow_html=True
)

