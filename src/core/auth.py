"""Authentication module for cloud deployment"""

from typing import Optional, Dict
import jwt
from datetime import datetime, timedelta
import os
import bcrypt

from ..database.db_manager import DatabaseManager
from ..database.models import Student


class AuthManager:
    """Manages authentication and authorization"""
    
    def __init__(self, db_manager: DatabaseManager, secret_key: str = None):
        """
        Initialize auth manager
        
        Args:
            db_manager: Database manager instance
            secret_key: Secret key for JWT tokens
        """
        self.db = db_manager
        self.secret_key = secret_key or os.getenv("SECRET_KEY", "change-this-secret-key-in-production")
        self.token_expiry_hours = 24
    
    def register_student(self, name: str, email: str, password: str, 
                        grade_level: int) -> Optional[Student]:
        """
        Register a new student with authentication
        
        Args:
            name: Student name
            email: Email address
            password: Password
            grade_level: Grade level (9-12)
        
        Returns:
            Created student object or None if email exists
        """
        # Check if email already exists
        existing = self.db.get_student_by_email(email)
        if existing:
            return None
        
        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Create student with password
        with self.db.get_session() as db_session:
            student = Student(
                name=name,
                email=email,
                password_hash=password_hash,
                grade_level=grade_level
            )
            db_session.add(student)
            db_session.flush()
            db_session.refresh(student)
            db_session.expunge(student)
            return student
    
    def authenticate(self, email: str, password: str) -> Optional[Student]:
        """
        Authenticate a student
        
        Args:
            email: Email address
            password: Password
        
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
    
    def create_token(self, student_id: int) -> str:
        """
        Create JWT token for student
        
        Args:
            student_id: Student ID
        
        Returns:
            JWT token string
        """
        payload = {
            "student_id": student_id,
            "exp": datetime.utcnow() + timedelta(hours=self.token_expiry_hours),
            "iat": datetime.utcnow()
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        return token
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """
        Verify JWT token
        
        Args:
            token: JWT token string
        
        Returns:
            Decoded payload if valid, None otherwise
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def get_student_from_token(self, token: str) -> Optional[Student]:
        """
        Get student from JWT token
        
        Args:
            token: JWT token string
        
        Returns:
            Student object if valid token, None otherwise
        """
        payload = self.verify_token(token)
        if not payload:
            return None
        
        student_id = payload.get("student_id")
        if not student_id:
            return None
        
        return self.db.get_student(student_id)
    
    def change_password(self, student_id: int, old_password: str, 
                       new_password: str) -> bool:
        """
        Change student password
        
        Args:
            student_id: Student ID
            old_password: Current password
            new_password: New password
        
        Returns:
            True if successful, False otherwise
        """
        student = self.db.get_student(student_id)
        if not student or not student.password_hash:
            return False
        
        # Verify old password
        if not bcrypt.checkpw(old_password.encode('utf-8'), student.password_hash.encode('utf-8')):
            return False
        
        # Hash new password
        new_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Update in database
        with self.db.get_session() as session:
            student = session.query(Student).filter(Student.id == student_id).first()
            if student:
                student.password_hash = new_hash
                return True
        
        return False
    
    def reset_password_request(self, email: str) -> Optional[str]:
        """
        Create password reset token
        
        Args:
            email: Student email
        
        Returns:
            Reset token if student exists, None otherwise
        """
        student = self.db.get_student_by_email(email)
        if not student:
            return None
        
        # Create short-lived reset token (1 hour)
        payload = {
            "student_id": student.id,
            "type": "password_reset",
            "exp": datetime.utcnow() + timedelta(hours=1),
            "iat": datetime.utcnow()
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        return token
    
    def reset_password(self, reset_token: str, new_password: str) -> bool:
        """
        Reset password using reset token
        
        Args:
            reset_token: Password reset token
            new_password: New password
        
        Returns:
            True if successful, False otherwise
        """
        payload = self.verify_token(reset_token)
        if not payload or payload.get("type") != "password_reset":
            return False
        
        student_id = payload.get("student_id")
        if not student_id:
            return False
        
        # Hash new password
        new_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Update in database
        with self.db.get_session() as session:
            student = session.query(Student).filter(Student.id == student_id).first()
            if student:
                student.password_hash = new_hash
                return True
        
        return False


# Streamlit-specific authentication helpers

def init_auth_state():
    """Initialize authentication state in Streamlit"""
    import streamlit as st
    
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'auth_token' not in st.session_state:
        st.session_state.auth_token = None


def render_login_page(auth_manager: AuthManager):
    """Render login page for Streamlit"""
    import streamlit as st
    
    st.markdown("# 🔐 Login")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                student = auth_manager.authenticate(email, password)
                if student:
                    token = auth_manager.create_token(student.id)
                    st.session_state.authenticated = True
                    st.session_state.auth_token = token
                    st.session_state.current_student = student
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid email or password")
    
    with tab2:
        with st.form("register_form"):
            name = st.text_input("Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            password_confirm = st.text_input("Confirm Password", type="password")
            grade = st.selectbox("Grade Level", options=[9, 10, 11, 12])
            submit = st.form_submit_button("Register")
            
            if submit:
                if not all([name, email, password]):
                    st.error("Please fill in all fields")
                elif password != password_confirm:
                    st.error("Passwords do not match")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters")
                else:
                    student = auth_manager.register_student(name, email, password, grade)
                    if student:
                        st.success("Registration successful! Please login.")
                    else:
                        st.error("Email already exists")


def require_auth(auth_manager: AuthManager):
    """Decorator/function to require authentication"""
    import streamlit as st
    
    init_auth_state()
    
    # Check if authentication is enabled
    enable_auth = os.getenv("ENABLE_AUTHENTICATION", "False").lower() == "true"
    
    if not enable_auth:
        return True
    
    if not st.session_state.authenticated:
        render_login_page(auth_manager)
        st.stop()
        return False
    
    # Verify token is still valid
    student = auth_manager.get_student_from_token(st.session_state.auth_token)
    if not student:
        st.session_state.authenticated = False
        st.session_state.auth_token = None
        st.session_state.current_student = None
        st.warning("Session expired. Please login again.")
        render_login_page(auth_manager)
        st.stop()
        return False
    
    return True

