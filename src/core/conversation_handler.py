"""Conversation handler - orchestrates AI tutoring conversations"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime

from ..database.db_manager import DatabaseManager
from ..ai.ai_client import AIClient, PromptBuilder
from .session_manager import SessionManager
from .student_manager import StudentManager


class ConversationHandler:
    """Handles tutoring conversations between student and AI"""
    
    def __init__(self, db_manager: DatabaseManager, ai_client: AIClient):
        """
        Initialize conversation handler
        
        Args:
            db_manager: Database manager instance
            ai_client: AI client instance
        """
        self.db = db_manager
        self.ai = ai_client
        self.session_manager = SessionManager(db_manager)
        self.student_manager = StudentManager(db_manager)
        self.prompt_builder = PromptBuilder()
    
    def handle_message(self, student_id: int, message: str,
                      session_id: int = None, session_type: str = "general") -> Dict:
        """
        Handle a student message and generate AI response
        
        Args:
            student_id: Student ID
            message: Student's message
            session_id: Optional existing session ID
            session_type: Type of session if creating new one
        
        Returns:
            Dict with response, session info, and metadata
        """
        # Get or create session
        if session_id:
            session = self.session_manager.get_session(session_id)
            if not session or not session.is_active:
                session = self.session_manager.start_session(student_id, session_type=session_type)
        else:
            session = self.session_manager.get_or_create_session(student_id, session_type=session_type)
        
        # Save student message
        student_msg = self.session_manager.add_message(
            session_id=session.id,
            role="student",
            content=message
        )
        
        # Get student info for context
        student = self.student_manager.get_student(student_id)
        
        # Build system prompt with student context
        system_prompt = self.prompt_builder.build_system_prompt(
            student_name=student.name,
            grade_level=student.grade_level
        )
        
        # Get conversation history
        conversation_history = self.session_manager.get_conversation_history(
            session_id=session.id,
            limit=40  # Keep reasonable context window
        )
        
        # Truncate if needed to fit token limits
        conversation_history = self.ai.truncate_conversation_history(
            conversation_history,
            max_tokens=6000
        )
        
        try:
            # Generate AI response
            ai_response = self.ai.generate_with_context(
                system=system_prompt,
                user_message=message,
                conversation_history=conversation_history[:-1]  # Exclude the message we just added
            )
            
            response_content = ai_response["content"]
            tokens_used = ai_response["usage"]["input_tokens"] + ai_response["usage"]["output_tokens"]
            
            # Save AI response
            tutor_msg = self.session_manager.add_message(
                session_id=session.id,
                role="tutor",
                content=response_content,
                tokens_used=tokens_used
            )
            
            # Update student last active
            self.student_manager.update_last_active(student_id)
            
            return {
                "success": True,
                "response": response_content,
                "session_id": session.id,
                "message_id": tutor_msg.id,
                "tokens_used": tokens_used,
                "timestamp": datetime.utcnow()
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "session_id": session.id,
                "timestamp": datetime.utcnow()
            }
    
    def start_homework_help(self, student_id: int, problem: str) -> Dict:
        """
        Start a homework help session
        
        Args:
            student_id: Student ID
            problem: The homework problem
        
        Returns:
            Response dict with AI's initial help
        """
        # Create new homework help session
        session = self.session_manager.start_session(
            student_id=student_id,
            topic="Homework Help",
            session_type="homework_help"
        )
        
        # Format the homework help prompt
        formatted_prompt = self.prompt_builder.format_homework_help_prompt(problem)
        
        # Handle as regular message
        return self.handle_message(
            student_id=student_id,
            message=formatted_prompt,
            session_id=session.id,
            session_type="homework_help"
        )
    
    def start_study_session(self, student_id: int, topic: str,
                           student_level: str = "developing") -> Dict:
        """
        Start a study session for a specific topic
        
        Args:
            student_id: Student ID
            topic: Topic to study
            student_level: Student's current level with the topic
        
        Returns:
            Response dict with study materials
        """
        # Create new study session
        session = self.session_manager.start_session(
            student_id=student_id,
            topic=topic,
            session_type="study_session"
        )
        
        # Format study session prompt
        formatted_prompt = self.prompt_builder.format_study_session_prompt(topic, student_level)
        
        # Handle as regular message
        return self.handle_message(
            student_id=student_id,
            message=formatted_prompt,
            session_id=session.id,
            session_type="study_session"
        )
    
    def request_practice_problems(self, student_id: int, topic: str,
                                 difficulty: str = "medium", count: int = 5) -> Dict:
        """
        Request practice problems for a topic
        
        Args:
            student_id: Student ID
            topic: Topic for practice
            difficulty: Difficulty level
            count: Number of problems
        
        Returns:
            Response dict with practice problems
        """
        # Get or create practice session
        session = self.session_manager.get_or_create_session(
            student_id=student_id,
            topic=topic,
            session_type="practice"
        )
        
        # Format practice request prompt
        formatted_prompt = self.prompt_builder.format_practice_request_prompt(
            topic, difficulty, count
        )
        
        # Handle as regular message
        return self.handle_message(
            student_id=student_id,
            message=formatted_prompt,
            session_id=session.id,
            session_type="practice"
        )
    
    def start_test_prep(self, student_id: int, test_topics: List[str],
                       days_until_test: int) -> Dict:
        """
        Start test preparation session
        
        Args:
            student_id: Student ID
            test_topics: List of topics on the test
            days_until_test: Days until the test
        
        Returns:
            Response dict with test prep plan
        """
        # Create test prep session
        session = self.session_manager.start_session(
            student_id=student_id,
            topic="Test Preparation",
            session_type="test_prep"
        )
        
        # Format test prep prompt
        formatted_prompt = self.prompt_builder.format_test_prep_prompt(
            test_topics, days_until_test
        )
        
        # Handle as regular message
        return self.handle_message(
            student_id=student_id,
            message=formatted_prompt,
            session_id=session.id,
            session_type="test_prep"
        )
    
    def get_conversation(self, session_id: int) -> Dict:
        """
        Get full conversation for a session
        
        Args:
            session_id: Session ID
        
        Returns:
            Session summary with all messages
        """
        return self.session_manager.get_session_summary(session_id)
    
    def end_conversation(self, session_id: int):
        """End a conversation session"""
        self.session_manager.end_session(session_id)

