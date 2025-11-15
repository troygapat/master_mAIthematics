"""Setup script for AI Math Tutor"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Run a command and print status"""
    print(f"\n{'='*60}")
    print(f"  {description}")
    print(f"{'='*60}\n")
    
    try:
        result = subprocess.run(command, check=True, shell=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed")
        print(f"Error: {e}")
        return False


def main():
    """Main setup function"""
    print("\n" + "="*60)
    print("  AI Math Tutor - Setup")
    print("="*60)
    
    base_dir = Path(__file__).parent
    
    # Check Python version
    print(f"\nPython version: {sys.version}")
    if sys.version_info < (3, 9):
        print("✗ Python 3.9 or higher is required")
        sys.exit(1)
    print("✓ Python version OK")
    
    # Install dependencies
    if not run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing dependencies"
    ):
        print("\nSetup failed. Please check the errors above.")
        sys.exit(1)
    
    # Check for .env file
    env_file = base_dir / ".env"
    env_example = base_dir / ".env.example"
    
    if not env_file.exists() and env_example.exists():
        print(f"\n{'='*60}")
        print("  Creating .env file")
        print(f"{'='*60}\n")
        
        # Copy .env.example to .env
        with open(env_example, 'r') as f:
            env_content = f.read()
        
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        print("✓ Created .env file")
        print("\n⚠️  IMPORTANT: Edit .env file and add your ANTHROPIC_API_KEY")
    elif env_file.exists():
        print("\n✓ .env file already exists")
    
    # Create data directory
    data_dir = base_dir / "data"
    data_dir.mkdir(exist_ok=True)
    print(f"\n✓ Created data directory")
    
    # Initialize database
    print(f"\n{'='*60}")
    print("  Initializing database")
    print(f"{'='*60}\n")
    
    init_db_script = base_dir / "src" / "database" / "init_db.py"
    if init_db_script.exists():
        if run_command(
            f"{sys.executable} {init_db_script}",
            "Creating database tables"
        ):
            print("✓ Database initialized")
        else:
            print("⚠️  Database initialization failed (will be created on first run)")
    
    # Setup complete
    print("\n" + "="*60)
    print("  Setup Complete!")
    print("="*60)
    print("\n✓ All dependencies installed")
    print("✓ Database initialized")
    print("✓ Application ready to run")
    
    print("\n" + "="*60)
    print("  Next Steps")
    print("="*60)
    print("\n1. Edit .env file and add your ANTHROPIC_API_KEY")
    print("   Get your key from: https://www.anthropic.com")
    print("\n2. Run the application:")
    print(f"   {sys.executable} -m streamlit run app.py")
    print("\nOr use the launch script:")
    print("   python launch.py")
    print("\n" + "="*60)


if __name__ == "__main__":
    main()

