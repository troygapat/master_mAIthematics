"""Database models using SQLAlchemy ORM"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Student(Base):
    """Student model - stores student profile information"""
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    grade_level = Column(Integer, nullable=False)  # 9-12 for high school
    email = Column(String(255), unique=True, nullable=True)
    password_hash = Column(String(255), nullable=True)  # For authentication
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    sessions = relationship("Session", back_populates="student", cascade="all, delete-orphan")
    progress = relationship("Progress", back_populates="student", cascade="all, delete-orphan")
    study_materials = relationship("StudyMaterial", back_populates="student", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Student(id={self.id}, name='{self.name}', grade={self.grade_level})>"


class Session(Base):
    """Session model - represents a tutoring session"""
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    topic = Column(String(255), nullable=True)
    session_type = Column(String(50), default="general")  # general, homework_help, study_session, test_prep, practice
    is_active = Column(Boolean, default=True)
    
    # Session metadata (JSON field for flexible data)
    session_metadata = Column(JSON, nullable=True)
    
    # Relationships
    student = relationship("Student", back_populates="sessions")
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Session(id={self.id}, student_id={self.student_id}, topic='{self.topic}')>"


class Message(Base):
    """Message model - stores conversation messages"""
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    role = Column(String(20), nullable=False)  # 'student' or 'tutor'
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Message metadata (JSON field)
    # Can store: problem_type, difficulty, latex_content, images, etc.
    message_metadata = Column(JSON, nullable=True)
    
    # Token usage tracking
    tokens_used = Column(Integer, nullable=True)
    
    # Relationships
    session = relationship("Session", back_populates="messages")
    
    def __repr__(self):
        return f"<Message(id={self.id}, role='{self.role}', session_id={self.session_id})>"


class Progress(Base):
    """Progress model - tracks student progress on topics"""
    __tablename__ = "progress"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    topic = Column(String(255), nullable=False)
    subtopic = Column(String(255), nullable=True)
    skill_level = Column(String(50), default="beginner")  # beginner, developing, proficient, advanced
    
    # Performance metrics
    attempts = Column(Integer, default=0)
    successes = Column(Integer, default=0)
    accuracy = Column(Float, default=0.0)  # Success rate (0.0 to 1.0)
    
    # Timestamps
    first_attempted = Column(DateTime, default=datetime.utcnow)
    last_practiced = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Notes and observations
    notes = Column(Text, nullable=True)
    
    # Relationships
    student = relationship("Student", back_populates="progress")
    
    def __repr__(self):
        return f"<Progress(id={self.id}, student_id={self.student_id}, topic='{self.topic}', level='{self.skill_level}')>"


class StudyMaterial(Base):
    """Study material model - stores generated study materials"""
    __tablename__ = "study_materials"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    title = Column(String(255), nullable=False)
    topic = Column(String(255), nullable=False)
    material_type = Column(String(50), nullable=False)  # study_guide, practice_set, test, worksheet, summary
    
    # Content stored as JSON for flexibility
    # Structure: {"introduction": "...", "examples": [...], "problems": [...], "solutions": [...]}
    content = Column(JSON, nullable=False)
    
    # Metadata
    difficulty_level = Column(String(50), nullable=True)
    estimated_time_minutes = Column(Integer, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    last_accessed = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    used_count = Column(Integer, default=0)
    
    # Relationships
    student = relationship("Student", back_populates="study_materials")
    
    def __repr__(self):
        return f"<StudyMaterial(id={self.id}, title='{self.title}', type='{self.material_type}')>"


class PracticeProblem(Base):
    """Practice problem model - stores individual practice problems and student attempts"""
    __tablename__ = "practice_problems"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    topic = Column(String(255), nullable=False)
    difficulty = Column(String(50), nullable=False)  # easy, medium, hard, challenge
    
    # Problem content
    problem_text = Column(Text, nullable=False)
    problem_type = Column(String(50), nullable=False)  # multiple_choice, short_answer, word_problem, proof
    correct_answer = Column(Text, nullable=False)
    
    # For multiple choice
    options = Column(JSON, nullable=True)  # List of answer choices
    
    # Student's attempt
    student_answer = Column(Text, nullable=True)
    is_correct = Column(Boolean, nullable=True)
    attempt_count = Column(Integer, default=0)
    hints_used = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    attempted_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Feedback and explanation
    feedback = Column(Text, nullable=True)
    solution_explanation = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<PracticeProblem(id={self.id}, topic='{self.topic}', difficulty='{self.difficulty}')>"

