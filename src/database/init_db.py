"""Initialize database - Create tables and optionally seed data"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.database.db_manager import DatabaseManager
from src.database.models import Base


def init_database(database_url: str = None, drop_existing: bool = False):
    """
    Initialize the database
    
    Args:
        database_url: Database connection string
        drop_existing: If True, drop existing tables first (WARNING: deletes all data)
    """
    print("Initializing database...")
    
    db_manager = DatabaseManager(database_url)
    
    if drop_existing:
        print("WARNING: Dropping existing tables...")
        db_manager.drop_tables()
    
    print("Creating tables...")
    db_manager.create_tables()
    
    print("Database initialization complete!")
    print(f"Database location: {db_manager.database_url}")


def seed_demo_data(database_url: str = None):
    """Add demo data for testing"""
    print("\nSeeding demo data...")
    
    db_manager = DatabaseManager(database_url)
    
    # Create demo student
    student = db_manager.create_student(
        name="Demo Student",
        grade_level=10,
        email="demo@example.com"
    )
    print(f"Created demo student: {student.name} (Grade {student.grade_level})")
    
    # Create a demo session
    session = db_manager.create_session(
        student_id=student.id,
        topic="Quadratic Equations",
        session_type="homework_help"
    )
    print(f"Created demo session: {session.topic}")
    
    # Add some demo messages
    db_manager.add_message(
        session_id=session.id,
        role="student",
        content="I need help solving x^2 + 5x + 6 = 0"
    )
    
    db_manager.add_message(
        session_id=session.id,
        role="tutor",
        content="Great question! Let's solve this quadratic equation together. What method do you think we should use?"
    )
    print("Added demo messages")
    
    # Add demo progress
    db_manager.update_progress(
        student_id=student.id,
        topic="Algebra",
        subtopic="Quadratic Equations",
        success=True,
        skill_level="developing"
    )
    print("Added demo progress record")
    
    print("\nDemo data seeding complete!")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Initialize the database")
    parser.add_argument("--drop", action="store_true", help="Drop existing tables first")
    parser.add_argument("--demo", action="store_true", help="Add demo data")
    parser.add_argument("--url", type=str, help="Database URL", default=None)
    
    args = parser.parse_args()
    
    # Initialize database
    init_database(database_url=args.url, drop_existing=args.drop)
    
    # Add demo data if requested
    if args.demo:
        seed_demo_data(database_url=args.url)

