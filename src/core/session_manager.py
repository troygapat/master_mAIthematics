"""Session management module"""

from typing import Optional, List, Dict, Tuple
from datetime import datetime

from ..database.db_manager import DatabaseManager
from ..database.models import Session, Message


class SessionManager:
    """Manages tutoring sessions"""
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize session manager
        
        Args:
            db_manager: Database manager instance
        """
        self.db = db_manager
    
    def start_session(self, student_id: int, topic: str = None,
                     session_type: str = "general") -> Session:
        """
        Start a new tutoring session
        
        Args:
            student_id: Student ID
            topic: Optional topic for the session
            session_type: Type of session (general, homework_help, study_session, test_prep, practice)
        
        Returns:
            Created session object
        """
        # End any active sessions first
        active_session = self.db.get_active_session(student_id)
        if active_session:
            self.end_session(active_session.id)
        
        # Create new session
        session = self.db.create_session(
            student_id=student_id,
            topic=topic,
            session_type=session_type
        )
        
        return session
    
    def get_or_create_session(self, student_id: int, topic: str = None,
                             session_type: str = "general") -> Session:
        """
        Get active session or create new one
        
        Args:
            student_id: Student ID
            topic: Optional topic
            session_type: Type of session
        
        Returns:
            Session object (existing or new)
        """
        # Check for active session
        active_session = self.db.get_active_session(student_id)
        
        if active_session:
            return active_session
        
        # Create new session
        return self.start_session(student_id, topic, session_type)
    
    def end_session(self, session_id: int):
        """End a session"""
        self.db.end_session(session_id)
    
    def get_session(self, session_id: int) -> Optional[Session]:
        """Get session by ID"""
        return self.db.get_tutoring_session(session_id)
    
    def get_student_sessions(self, student_id: int, limit: int = 10) -> List[Session]:
        """Get student's recent sessions"""
        return self.db.get_student_sessions(student_id, limit=limit)
    
    def add_message(self, session_id: int, role: str, content: str,
                   message_metadata: Dict = None, tokens_used: int = None) -> Message:
        """
        Add a message to a session
        
        Args:
            session_id: Session ID
            role: Message role ('student' or 'tutor')
            content: Message content
            message_metadata: Optional metadata dict
            tokens_used: Token count for this message
        
        Returns:
            Created message object
        """
        if role not in ['student', 'tutor']:
            raise ValueError("Role must be 'student' or 'tutor'")
        
        message = self.db.add_message(
            session_id=session_id,
            role=role,
            content=content,
            message_metadata=message_metadata,
            tokens_used=tokens_used
        )
        
        return message
    
    def get_session_messages(self, session_id: int, limit: int = None) -> List[Message]:
        """Get messages for a session"""
        return self.db.get_session_messages(session_id, limit=limit)
    
    def get_conversation_history(self, session_id: int, limit: int = 50) -> List[Dict[str, str]]:
        """
        Get conversation history formatted for AI
        
        Args:
            session_id: Session ID
            limit: Maximum messages to retrieve
        
        Returns:
            List of message dicts with 'role' and 'content'
        """
        messages = self.db.get_session_messages(session_id, limit=limit)
        
        # Format for AI (role must be 'user' or 'assistant')
        formatted = []
        for msg in messages:
            formatted.append({
                "role": "user" if msg.role == "student" else "assistant",
                "content": msg.content
            })
        
        return formatted
    
    def get_session_summary(self, session_id: int) -> Dict:
        """
        Get comprehensive summary of a session
        
        Args:
            session_id: Session ID
        
        Returns:
            Dict with session info and statistics
        """
        session = self.get_session(session_id)
        if not session:
            return None
        
        messages = self.get_session_messages(session_id)
        
        # Calculate statistics
        student_messages = [m for m in messages if m.role == "student"]
        tutor_messages = [m for m in messages if m.role == "tutor"]
        
        total_tokens = sum(m.tokens_used for m in messages if m.tokens_used)
        
        # Calculate session duration
        if session.end_time:
            duration_seconds = (session.end_time - session.start_time).total_seconds()
            duration_minutes = int(duration_seconds / 60)
        else:
            duration_seconds = (datetime.utcnow() - session.start_time).total_seconds()
            duration_minutes = int(duration_seconds / 60)
        
        return {
            "session": {
                "id": session.id,
                "topic": session.topic,
                "session_type": session.session_type,
                "start_time": session.start_time,
                "end_time": session.end_time,
                "is_active": session.is_active,
                "duration_minutes": duration_minutes
            },
            "statistics": {
                "total_messages": len(messages),
                "student_messages": len(student_messages),
                "tutor_messages": len(tutor_messages),
                "total_tokens": total_tokens
            },
            "messages": [
                {
                    "id": m.id,
                    "role": m.role,
                    "content": m.content,
                    "timestamp": m.timestamp,
                    "tokens_used": m.tokens_used
                }
                for m in messages
            ]
        }
    
    def search_sessions(self, student_id: int, topic: str = None,
                       session_type: str = None) -> List[Session]:
        """
        Search sessions by criteria
        
        Args:
            student_id: Student ID
            topic: Optional topic filter
            session_type: Optional session type filter
        
        Returns:
            List of matching sessions
        """
        all_sessions = self.db.get_student_sessions(student_id, limit=100)
        
        # Filter by criteria
        filtered = []
        for session in all_sessions:
            if topic and topic.lower() not in (session.topic or "").lower():
                continue
            if session_type and session.session_type != session_type:
                continue
            filtered.append(session)
        
        return filtered

