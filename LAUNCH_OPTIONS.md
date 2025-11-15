# 🚀 Easy Launch Options for AI Math Tutor

No command line needed! Choose your preferred way to launch the app:

---

## ⭐ Option 1: Simple Double-Click (Recommended)

**Just double-click this file:**
```
START_TUTOR.bat
```

✅ **What it does:**
- Automatically checks for dependencies
- Sets up the database if needed
- Launches the app in your browser
- Shows a console window with status

---

## 🎨 Option 2: GUI Launcher (Pretty Interface)

**Double-click this file:**
```
START_TUTOR_GUI.bat
```

✅ **Features:**
- Nice graphical window with buttons
- Easy configuration of API key
- Start/Stop controls
- Status indicators
- Help button

**Or run directly:**
```
python gui_launcher.py
```

---

## 🖥️ Option 3: Create Desktop Shortcut

### Windows Instructions:

1. **Right-click on `START_TUTOR.bat`** (or `START_TUTOR_GUI.bat`)
2. Click **"Create shortcut"**
3. **Drag the shortcut** to your Desktop
4. *(Optional)* **Right-click the shortcut** → Properties → Change Icon

Now you can launch from your desktop with one click!

### Custom Icon (Optional):

If you want a custom icon:
1. Right-click the desktop shortcut
2. Click **Properties**
3. Click **Change Icon**
4. Browse to an `.ico` file or use system icons

---

## 📌 Option 4: Pin to Taskbar

### Windows 10/11:

1. Create a desktop shortcut (see Option 3)
2. **Right-click the shortcut**
3. Select **"Pin to taskbar"**

Now it's always one click away!

---

## 🔧 Option 5: Create Windows Start Menu Entry

1. Press **Win+R** to open Run
2. Type: `shell:programs`
3. Press Enter
4. Copy `START_TUTOR.bat` to this folder
5. Rename it to `AI Math Tutor.bat`

Now you can launch from Start Menu:
- Press **Windows key**
- Type **"AI Math Tutor"**
- Press Enter

---

## ⚡ Quick Comparison

| Method | Ease | Features | Best For |
|--------|------|----------|----------|
| **START_TUTOR.bat** | ⭐⭐⭐⭐⭐ | Basic | Quick daily use |
| **GUI Launcher** | ⭐⭐⭐⭐ | Advanced | First-time users |
| **Desktop Shortcut** | ⭐⭐⭐⭐⭐ | Basic | Convenience |
| **Taskbar Pin** | ⭐⭐⭐⭐⭐ | Basic | Power users |
| **Start Menu** | ⭐⭐⭐⭐ | Basic | Organization |

---

## 🎯 First Time Setup

**All methods will automatically:**
1. ✅ Check if Python is installed
2. ✅ Install dependencies (first run only)
3. ✅ Create `.env` file from template
4. ✅ Initialize the database
5. ✅ Open your web browser

**You only need to:**
- Add your Anthropic API key to `.env` file
- The launcher will help you do this!

---

## 🔑 Configuring Your API Key

### Using GUI Launcher:
1. Click **"Configure API Key"** button
2. The `.env` file will open in Notepad
3. Replace `your_anthropic_api_key_here` with your actual key
4. Save and close
5. Click **"Start Tutor"**

### Manual Method:
1. Open `.env` file (in the math_tutor folder)
2. Find the line: `ANTHROPIC_API_KEY=your_anthropic_api_key_here`
3. Replace with: `ANTHROPIC_API_KEY=sk-ant-your-actual-key`
4. Save the file

**Get your API key:** https://console.anthropic.com/

---

## ⏹️ Stopping the Application

### Simple Method:
- Close the browser tab
- Press **Ctrl+C** in the console window
- Or just close the console window

### GUI Launcher:
- Click the **"Stop Tutor"** button

---

## 🐛 Troubleshooting

### "Python not found"
- Install Python 3.9+ from [python.org](https://python.org)
- Make sure to check "Add Python to PATH" during installation

### "API key not configured"
- Open `.env` file
- Add your Anthropic API key
- Restart the application

### "Port already in use"
- Another instance is running
- Close it first, then restart
- Or change the port in the launch command

### GUI won't open
- Use `START_TUTOR.bat` instead
- Or run from command line: `python -m streamlit run app.py`

---

## 💡 Pro Tips

### Tip 1: Auto-start on Login (Optional)
1. Press **Win+R**
2. Type: `shell:startup`
3. Copy your shortcut to this folder

### Tip 2: Custom Name
Rename `START_TUTOR.bat` to anything you want:
- `Math Tutor.bat`
- `My Tutor.bat`
- `Homework Helper.bat`

### Tip 3: Multiple Students
Each time you launch, you can:
- Switch between student profiles
- Or create a new student
- All data is saved between sessions

---

## 📊 Comparison with Command Line

| Feature | Easy Launch | Command Line |
|---------|-------------|--------------|
| **Setup** | Automatic | Manual |
| **User-friendly** | ✅ Yes | ❌ No |
| **Error handling** | ✅ Yes | ⚠️ Basic |
| **Status messages** | ✅ Clear | ⚠️ Technical |
| **Configuration help** | ✅ Yes | ❌ No |
| **Best for** | Everyone | Developers |

---

## 🎓 Ready to Start?

**Recommended for most users:**
1. Double-click `START_TUTOR.bat`
2. Let it do the setup (first time only)
3. Add your API key when prompted
4. Create a student profile
5. Start learning! 🚀

**For a prettier experience:**
- Use `START_TUTOR_GUI.bat` for the graphical launcher

**Questions?**
- See `QUICKSTART.md` for detailed setup guide
- See `README.md` for feature documentation

---

**Happy tutoring! 📚✨**

