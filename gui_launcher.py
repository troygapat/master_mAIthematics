"""
AI Math Tutor - GUI Launcher
Simple graphical launcher for the application
"""

import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os
from pathlib import Path
import webbrowser


class TutorLauncher:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("AI Math Tutor Launcher")
        self.window.geometry("500x400")
        self.window.resizable(False, False)
        
        # Set icon if available
        try:
            self.window.iconbitmap(default='icon.ico')
        except:
            pass
        
        self.setup_ui()
        self.process = None
    
    def setup_ui(self):
        """Setup the user interface"""
        # Header
        header = tk.Label(
            self.window,
            text="🎓 AI Math Tutor",
            font=("Arial", 24, "bold"),
            fg="#1f77b4"
        )
        header.pack(pady=20)
        
        # Description
        desc = tk.Label(
            self.window,
            text="High School Mathematics Tutoring System\nDesigned by Troy A. Brumfield",
            font=("Arial", 10),
            justify=tk.CENTER
        )
        desc.pack(pady=10)
        
        # Status frame
        self.status_frame = tk.Frame(self.window)
        self.status_frame.pack(pady=20)
        
        self.status_label = tk.Label(
            self.status_frame,
            text="Ready to start",
            font=("Arial", 10),
            fg="green"
        )
        self.status_label.pack()
        
        # Buttons
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=20)
        
        self.start_button = tk.Button(
            button_frame,
            text="▶️  Start Tutor",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            width=20,
            height=2,
            command=self.start_app,
            cursor="hand2"
        )
        self.start_button.pack(pady=10)
        
        self.stop_button = tk.Button(
            button_frame,
            text="⏹️  Stop Tutor",
            font=("Arial", 12),
            bg="#f44336",
            fg="white",
            width=20,
            height=2,
            command=self.stop_app,
            state=tk.DISABLED,
            cursor="hand2"
        )
        self.stop_button.pack(pady=10)
        
        # Config button
        config_button = tk.Button(
            button_frame,
            text="⚙️  Configure API Key",
            font=("Arial", 10),
            bg="#2196F3",
            fg="white",
            width=20,
            command=self.open_config,
            cursor="hand2"
        )
        config_button.pack(pady=10)
        
        # Help button
        help_button = tk.Button(
            button_frame,
            text="❓ Help & Documentation",
            font=("Arial", 10),
            bg="#9E9E9E",
            fg="white",
            width=20,
            command=self.open_help,
            cursor="hand2"
        )
        help_button.pack(pady=5)
        
        # Footer
        footer = tk.Label(
            self.window,
            text="The application will open in your web browser",
            font=("Arial", 8),
            fg="gray"
        )
        footer.pack(side=tk.BOTTOM, pady=10)
    
    def check_setup(self):
        """Check if setup is complete"""
        # Check .env file
        if not os.path.exists(".env"):
            response = messagebox.askyesno(
                "Setup Required",
                ".env file not found!\n\n"
                "Would you like to create it now?\n"
                "You'll need to add your Anthropic API key."
            )
            if response:
                # Copy template
                if os.path.exists("env_template.txt"):
                    with open("env_template.txt", "r") as src:
                        content = src.read()
                    with open(".env", "w") as dst:
                        dst.write(content)
                    self.open_config()
                return False
            else:
                return False
        
        # Check if streamlit is installed
        try:
            import streamlit
        except ImportError:
            response = messagebox.askyesno(
                "First Time Setup",
                "Dependencies not installed.\n\n"
                "Would you like to install them now?\n"
                "This may take a few minutes."
            )
            if response:
                self.install_dependencies()
                return False
            else:
                return False
        
        return True
    
    def install_dependencies(self):
        """Install required dependencies"""
        self.update_status("Installing dependencies...", "orange")
        self.window.update()
        
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                check=True,
                capture_output=True
            )
            messagebox.showinfo("Success", "Dependencies installed successfully!")
            self.update_status("Ready to start", "green")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to install dependencies:\n{str(e)}")
            self.update_status("Setup failed", "red")
    
    def start_app(self):
        """Start the Streamlit application"""
        if not self.check_setup():
            return
        
        try:
            self.update_status("Starting application...", "orange")
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.window.update()
            
            # Start streamlit in background
            self.process = subprocess.Popen(
                [sys.executable, "-m", "streamlit", "run", "app.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )
            
            # Wait a bit then check if it's running
            self.window.after(3000, self.check_if_started)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start application:\n{str(e)}")
            self.update_status("Failed to start", "red")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
    
    def check_if_started(self):
        """Check if the application started successfully"""
        if self.process and self.process.poll() is None:
            self.update_status("✓ Application running", "green")
            messagebox.showinfo(
                "Success",
                "AI Math Tutor is now running!\n\n"
                "The application should open in your browser.\n"
                "If not, go to: http://localhost:8501"
            )
        else:
            messagebox.showerror(
                "Error",
                "Application failed to start.\n"
                "Check that your API key is configured correctly."
            )
            self.update_status("Failed to start", "red")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
    
    def stop_app(self):
        """Stop the application"""
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except:
                self.process.kill()
            
            self.process = None
            self.update_status("Stopped", "orange")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            messagebox.showinfo("Stopped", "Application has been stopped.")
    
    def open_config(self):
        """Open .env file for editing"""
        if not os.path.exists(".env"):
            # Create from template
            if os.path.exists("env_template.txt"):
                with open("env_template.txt", "r") as src:
                    content = src.read()
                with open(".env", "w") as dst:
                    dst.write(content)
        
        try:
            if sys.platform == 'win32':
                os.startfile(".env")
            else:
                subprocess.run(["open", ".env"])
        except:
            messagebox.showwarning(
                "Manual Edit Required",
                "Please open the .env file manually and add your API key:\n\n"
                f"{os.path.abspath('.env')}"
            )
    
    def open_help(self):
        """Open help documentation"""
        help_file = "QUICKSTART.md"
        if os.path.exists(help_file):
            try:
                if sys.platform == 'win32':
                    os.startfile(help_file)
                else:
                    subprocess.run(["open", help_file])
            except:
                messagebox.showinfo(
                    "Help",
                    f"Please open {help_file} for documentation"
                )
        else:
            messagebox.showinfo(
                "Help",
                "Quick Start:\n\n"
                "1. Click 'Configure API Key'\n"
                "2. Add your Anthropic API key\n"
                "3. Click 'Start Tutor'\n"
                "4. Create a student profile\n"
                "5. Start chatting!\n\n"
                "Get your API key from:\n"
                "https://console.anthropic.com/"
            )
    
    def update_status(self, message, color):
        """Update status message"""
        self.status_label.config(text=message, fg=color)
    
    def on_closing(self):
        """Handle window closing"""
        if self.process:
            response = messagebox.askyesno(
                "Confirm Exit",
                "The application is still running.\n"
                "Do you want to stop it and exit?"
            )
            if response:
                self.stop_app()
                self.window.destroy()
        else:
            self.window.destroy()
    
    def run(self):
        """Run the launcher"""
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()


if __name__ == "__main__":
    # Change to script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    launcher = TutorLauncher()
    launcher.run()

