"""Launch script for AI Math Tutor"""

import subprocess
import sys
import os
from pathlib import Path


def check_api_key():
    """Check if API key is configured"""
    env_file = Path(__file__).parent / ".env"
    
    if not env_file.exists():
        return False
    
    with open(env_file, 'r') as f:
        content = f.read()
        if 'ANTHROPIC_API_KEY=your_api_key_here' in content or 'ANTHROPIC_API_KEY=' not in content:
            return False
    
    return True


def main():
    """Main launch function"""
    print("\n" + "="*60)
    print("  AI Math Tutor - Launcher")
    print("="*60 + "\n")
    
    # Check if setup was run
    if not Path("data").exists():
        print("⚠️  Setup not completed. Running setup first...\n")
        subprocess.run([sys.executable, "setup.py"])
        print("\n")
    
    # Check API key
    if not check_api_key():
        print("⚠️  WARNING: ANTHROPIC_API_KEY not configured in .env file")
        print("   The application will not work without an API key.")
        print("   Get your key from: https://www.anthropic.com\n")
        
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Exiting...")
            sys.exit(0)
    
    # Launch Streamlit
    print("\n" + "="*60)
    print("  Launching AI Math Tutor...")
    print("="*60 + "\n")
    print("The application will open in your web browser.")
    print("Press Ctrl+C to stop the application.\n")
    print("="*60 + "\n")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n\nShutting down...")
    except Exception as e:
        print(f"\nError launching application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

