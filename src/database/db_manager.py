"""Database manager - handles database connections and operations"""

import os
from typing import Optional, List, Dict, Any
from contextlib import contextmanager
from sqlalchemy import create_engine, and_, or_, desc
from sqlalchemy.orm import sessionmaker, Session as DBSession
from sqlalchemy.pool import StaticPool
from datetime import datetime, timedelta

from .models import Base, Student, Session, Message, Progress, StudyMaterial, PracticeProblem


class DatabaseManager:
    """Manages database connections and provides data access methods"""
    
    def __init__(self, database_url: str = None):
        """
        Initialize database manager
        
        Args:
            database_url: Database connection string (defaults to SQLite in data/ folder)
        """
        if database_url is None:
            # Default to SQLite
            db_path = os.path.join(os.path.dirname(__file__), "../../data/tutoring.db")
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            database_url = f"sqlite:///{db_path}"
        
        self.database_url = database_url
        
        # Special handling for SQLite
        if database_url.startswith("sqlite"):
            self.engine = create_engine(
                database_url,
                connect_args={"check_same_thread": False},
                poolclass=StaticPool,
                echo=False
            )
        else:
            # PostgreSQL or other databases
            self.engine = create_engine(database_url, echo=False)
        
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def create_tables(self):
        """Create all tables in the database"""
        Base.metadata.create_all(bind=self.engine)
    
    def drop_tables(self):
        """Drop all tables (use with caution!)"""
        Base.metadata.drop_all(bind=self.engine)
    
    @contextmanager
    def get_session(self):
        """Context manager for database sessions"""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    # ==================== Student Operations ====================
    
    def create_student(self, name: str, grade_level: int, email: str = None) -> Student:
        """Create a new student"""
        with self.get_session() as db_session:
            student = Student(name=name, grade_level=grade_level, email=email)
            db_session.add(student)
            db_session.flush()
            db_session.refresh(student)
            # Expunge to detach from session so it can be used outside
            db_session.expunge(student)
            return student
    
    def get_student(self, student_id: int) -> Optional[Student]:
        """Get student by ID"""
        with self.get_session() as db_session:
            student = db_session.query(Student).filter(Student.id == student_id).first()
            if student:
                db_session.expunge(student)
            return student
    
    def get_student_by_email(self, email: str) -> Optional[Student]:
        """Get student by email"""
        with self.get_session() as db_session:
            student = db_session.query(Student).filter(Student.email == email).first()
            if student:
                db_session.expunge(student)
            return student
    
    def get_all_students(self, active_only: bool = True) -> List[Student]:
        """Get all students"""
        with self.get_session() as db_session:
            query = db_session.query(Student)
            if active_only:
                query = query.filter(Student.is_active == True)
            students = query.order_by(Student.name).all()
            # Expunge all students so they can be used outside the session
            for student in students:
                db_session.expunge(student)
            return students
    
    def update_student_last_active(self, student_id: int):
        """Update student's last active timestamp"""
        with self.get_session() as db_session:
            student = db_session.query(Student).filter(Student.id == student_id).first()
            if student:
                student.last_active = datetime.utcnow()
    
    # ==================== Session Operations ====================
    
    def create_session(self, student_id: int, topic: str = None, session_type: str = "general") -> Session:
        """Create a new tutoring session"""
        with self.get_session() as db_session:
            new_session = Session(
                student_id=student_id,
                topic=topic,
                session_type=session_type,
                is_active=True
            )
            db_session.add(new_session)
            db_session.flush()
            db_session.refresh(new_session)
            db_session.expunge(new_session)
            return new_session
    
    def get_tutoring_session(self, session_id: int) -> Optional[Session]:
        """Get tutoring session by ID"""
        with self.get_session() as db_session:
            sess = db_session.query(Session).filter(Session.id == session_id).first()
            if sess:
                db_session.expunge(sess)
            return sess
    
    def get_active_session(self, student_id: int) -> Optional[Session]:
        """Get student's active session if any"""
        with self.get_session() as db_session:
            sess = db_session.query(Session).filter(
                and_(Session.student_id == student_id, Session.is_active == True)
            ).first()
            if sess:
                db_session.expunge(sess)
            return sess
    
    def get_student_sessions(self, student_id: int, limit: int = 10) -> List[Session]:
        """Get student's recent sessions"""
        with self.get_session() as db_session:
            sessions = db_session.query(Session).filter(
                Session.student_id == student_id
            ).order_by(desc(Session.start_time)).limit(limit).all()
            for sess in sessions:
                db_session.expunge(sess)
            return sessions
    
    def end_session(self, session_id: int):
        """End a session"""
        with self.get_session() as db_session:
            sess = db_session.query(Session).filter(Session.id == session_id).first()
            if sess:
                sess.is_active = False
                sess.end_time = datetime.utcnow()
    
    # ==================== Message Operations ====================
    
    def add_message(self, session_id: int, role: str, content: str, 
                    message_metadata: Dict = None, tokens_used: int = None) -> Message:
        """Add a message to a session"""
        with self.get_session() as db_session:
            message = Message(
                session_id=session_id,
                role=role,
                content=content,
                message_metadata=message_metadata,
                tokens_used=tokens_used
            )
            db_session.add(message)
            db_session.flush()
            db_session.refresh(message)
            db_session.expunge(message)
            return message
    
    def get_session_messages(self, session_id: int, limit: int = None) -> List[Message]:
        """Get messages for a session"""
        with self.get_session() as db_session:
            query = db_session.query(Message).filter(
                Message.session_id == session_id
            ).order_by(Message.timestamp)
            
            if limit:
                query = query.limit(limit)
            
            messages = query.all()
            for msg in messages:
                db_session.expunge(msg)
            return messages
    
    def get_recent_messages(self, session_id: int, limit: int = 10) -> List[Message]:
        """Get recent messages from a session"""
        with self.get_session() as db_session:
            messages = db_session.query(Message).filter(
                Message.session_id == session_id
            ).order_by(desc(Message.timestamp)).limit(limit).all()
            for msg in messages:
                db_session.expunge(msg)
            return messages
    
    # ==================== Progress Operations ====================
    
    def update_progress(self, student_id: int, topic: str, subtopic: str = None,
                       success: bool = True, skill_level: str = None) -> Progress:
        """Update or create progress record"""
        with self.get_session() as db_session:
            # Find existing progress record
            progress = db_session.query(Progress).filter(
                and_(
                    Progress.student_id == student_id,
                    Progress.topic == topic,
                    Progress.subtopic == subtopic
                )
            ).first()
            
            if progress:
                # Update existing
                progress.attempts += 1
                if success:
                    progress.successes += 1
                progress.accuracy = progress.successes / progress.attempts if progress.attempts > 0 else 0.0
                progress.last_practiced = datetime.utcnow()
                if skill_level:
                    progress.skill_level = skill_level
            else:
                # Create new
                progress = Progress(
                    student_id=student_id,
                    topic=topic,
                    subtopic=subtopic,
                    attempts=1,
                    successes=1 if success else 0,
                    accuracy=1.0 if success else 0.0,
                    skill_level=skill_level or "beginner"
                )
                db_session.add(progress)
            
            db_session.flush()
            db_session.refresh(progress)
            db_session.expunge(progress)
            return progress
    
    def get_student_progress(self, student_id: int, topic: str = None) -> List[Progress]:
        """Get student's progress records"""
        with self.get_session() as db_session:
            query = db_session.query(Progress).filter(Progress.student_id == student_id)
            if topic:
                query = query.filter(Progress.topic == topic)
            progress_list = query.order_by(desc(Progress.last_practiced)).all()
            for prog in progress_list:
                db_session.expunge(prog)
            return progress_list
    
    # ==================== Study Material Operations ====================
    
    def create_study_material(self, student_id: int, title: str, topic: str,
                            material_type: str, content: Dict) -> StudyMaterial:
        """Create a study material"""
        with self.get_session() as db_session:
            material = StudyMaterial(
                student_id=student_id,
                title=title,
                topic=topic,
                material_type=material_type,
                content=content
            )
            db_session.add(material)
            db_session.flush()
            db_session.refresh(material)
            db_session.expunge(material)
            return material
    
    def get_study_materials(self, student_id: int, topic: str = None,
                           material_type: str = None) -> List[StudyMaterial]:
        """Get study materials for a student"""
        with self.get_session() as db_session:
            query = db_session.query(StudyMaterial).filter(StudyMaterial.student_id == student_id)
            if topic:
                query = query.filter(StudyMaterial.topic == topic)
            if material_type:
                query = query.filter(StudyMaterial.material_type == material_type)
            materials = query.order_by(desc(StudyMaterial.created_at)).all()
            for mat in materials:
                db_session.expunge(mat)
            return materials
    
    def increment_material_usage(self, material_id: int):
        """Increment usage count for a study material"""
        with self.get_session() as db_session:
            material = db_session.query(StudyMaterial).filter(StudyMaterial.id == material_id).first()
            if material:
                material.used_count += 1
                material.last_accessed = datetime.utcnow()
    
    # ==================== Practice Problem Operations ====================
    
    def create_practice_problem(self, student_id: int, topic: str, difficulty: str,
                               problem_text: str, problem_type: str, correct_answer: str,
                               options: List = None) -> PracticeProblem:
        """Create a practice problem"""
        with self.get_session() as db_session:
            problem = PracticeProblem(
                student_id=student_id,
                topic=topic,
                difficulty=difficulty,
                problem_text=problem_text,
                problem_type=problem_type,
                correct_answer=correct_answer,
                options=options
            )
            db_session.add(problem)
            db_session.flush()
            db_session.refresh(problem)
            db_session.expunge(problem)
            return problem
    
    def update_problem_attempt(self, problem_id: int, student_answer: str,
                              is_correct: bool, feedback: str = None):
        """Update a problem attempt"""
        with self.get_session() as db_session:
            problem = db_session.query(PracticeProblem).filter(PracticeProblem.id == problem_id).first()
            if problem:
                problem.student_answer = student_answer
                problem.is_correct = is_correct
                problem.attempt_count += 1
                problem.attempted_at = datetime.utcnow()
                if is_correct:
                    problem.completed_at = datetime.utcnow()
                if feedback:
                    problem.feedback = feedback
    
    def get_practice_problems(self, student_id: int, topic: str = None,
                             completed: bool = None) -> List[PracticeProblem]:
        """Get practice problems for a student"""
        with self.get_session() as db_session:
            query = db_session.query(PracticeProblem).filter(PracticeProblem.student_id == student_id)
            if topic:
                query = query.filter(PracticeProblem.topic == topic)
            if completed is not None:
                if completed:
                    query = query.filter(PracticeProblem.is_correct == True)
                else:
                    query = query.filter(or_(
                        PracticeProblem.is_correct == False,
                        PracticeProblem.is_correct == None
                    ))
            problems = query.order_by(desc(PracticeProblem.created_at)).all()
            for prob in problems:
                db_session.expunge(prob)
            return problems

