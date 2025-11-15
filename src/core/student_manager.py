"""Student management module"""

from typing import Optional, List, Dict
from datetime import datetime
import bcrypt

from ..database.db_manager import DatabaseManager
from ..database.models import Student


class StudentManager:
    """Manages student operations"""
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize student manager
        
        Args:
            db_manager: Database manager instance
        """
        self.db = db_manager
    
    def create_student(self, name: str, grade_level: int, email: str = None,
                      password: str = None) -> Student:
        """
        Create a new student
        
        Args:
            name: Student's name
            grade_level: Grade level (9-12)
            email: Optional email for authentication
            password: Optional password for authentication
        
        Returns:
            Created student object
        """
        if grade_level < 9 or grade_level > 12:
            raise ValueError("Grade level must be between 9 and 12 for high school")
        
        # Hash password if provided
        password_hash = None
        if password:
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        student = self.db.create_student(
            name=name,
            grade_level=grade_level,
            email=email
        )
        
        return student
    
    def get_student(self, student_id: int) -> Optional[Student]:
        """Get student by ID"""
        return self.db.get_student(student_id)
    
    def get_all_students(self, active_only: bool = True) -> List[Student]:
        """Get all students"""
        return self.db.get_all_students(active_only=active_only)
    
    def authenticate_student(self, email: str, password: str) -> Optional[Student]:
        """
        Authenticate a student by email and password
        
        Args:
            email: Student email
            password: Student password
        
        Returns:
            Student object if authenticated, None otherwise
        """
        student = self.db.get_student_by_email(email)
        
        if not student or not student.password_hash:
            return None
        
        # Check password
        if bcrypt.checkpw(password.encode('utf-8'), student.password_hash.encode('utf-8')):
            # Update last active
            self.db.update_student_last_active(student.id)
            return student
        
        return None
    
    def update_last_active(self, student_id: int):
        """Update student's last active timestamp"""
        self.db.update_student_last_active(student_id)
    
    def get_student_summary(self, student_id: int) -> Dict:
        """
        Get comprehensive summary of student's activity
        
        Args:
            student_id: Student ID
        
        Returns:
            Dict with student info and statistics
        """
        student = self.get_student(student_id)
        if not student:
            return None
        
        # Get ALL sessions to count total (not just limited)
        all_sessions = self.db.get_student_sessions(student_id, limit=1000)
        
        # Get recent sessions for display
        recent_sessions = all_sessions[:5] if all_sessions else []
        
        # Get progress records
        progress_records = self.db.get_student_progress(student_id)
        
        # Calculate statistics - query messages count directly
        total_sessions = len(all_sessions)
        
        # Count total messages across all sessions
        total_messages = 0
        message_counts = {}
        for session in all_sessions:
            messages = self.db.get_session_messages(session.id)
            count = len(messages)
            message_counts[session.id] = count
            total_messages += count
        
        # Topics worked on
        topics_worked = set()
        for progress in progress_records:
            topics_worked.add(progress.topic)
        
        return {
            "student": {
                "id": student.id,
                "name": student.name,
                "grade_level": student.grade_level,
                "created_at": student.created_at,
                "last_active": student.last_active
            },
            "statistics": {
                "total_sessions": total_sessions,
                "total_messages": total_messages,
                "topics_worked": len(topics_worked),
                "topics_list": list(topics_worked)
            },
            "recent_sessions": [
                {
                    "id": s.id,
                    "topic": s.topic,
                    "session_type": s.session_type,
                    "start_time": s.start_time,
                    "message_count": message_counts.get(s.id, 0)
                }
                for s in recent_sessions
            ],
            "progress": [
                {
                    "topic": p.topic,
                    "subtopic": p.subtopic,
                    "skill_level": p.skill_level,
                    "accuracy": round(p.accuracy * 100, 1),
                    "attempts": p.attempts,
                    "last_practiced": p.last_practiced
                }
                for p in progress_records[:10]
            ]
        }

