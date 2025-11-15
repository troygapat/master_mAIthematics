# AI Math Tutor - Quick Start Guide

Get up and running in 5 minutes!

## Prerequisites

- Python 3.9 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com/))

## Installation

### 1. Clone or Download

```bash
cd math_tutor
```

### 2. Run Setup

**Windows:**
```bash
python setup.py
```

**Mac/Linux:**
```bash
python3 setup.py
```

This will:
- Install all required dependencies
- Create a `.env` file
- Initialize the database
- Set up the data directory

### 3. Configure API Key

1. Open the `.env` file in a text editor
2. Replace `your_api_key_here` with your actual Anthropic API key:
   ```
   ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
   ```
3. Save the file

### 4. Launch the Application

**Windows:**
```bash
python launch.py
```

**Mac/Linux:**
```bash
python3 launch.py
```

The application will open in your web browser automatically!

## First Steps

### 1. Create a Student Profile

- Click "Create New Student" in the sidebar
- Enter name and grade level (9-12)
- Click "Create Student"

### 2. Start Tutoring

Choose from three main features:

#### 💬 Chat
- Ask homework questions
- Get step-by-step explanations
- Study specific topics
- Prepare for tests

**Example questions to try:**
- "I need help with quadratic equations"
- "Can you explain the unit circle?"
- "How do I factor polynomials?"

#### 📝 Practice
- Select a topic from the sidebar
- Choose difficulty level
- Generate practice problems
- Work through problems at your own pace

**Topics available:**
- Algebra 1 & 2
- Geometry
- Trigonometry
- Precalculus
- Calculus

#### 📊 Progress
- View accuracy by topic
- Track skill levels
- See recent sessions
- Get personalized recommendations

## Tips for Best Results

### Getting Help Effectively

✅ **DO:**
- Explain what you don't understand
- Show your work so far
- Ask specific questions
- Be patient with yourself

❌ **DON'T:**
- Just ask for the answer
- Rush through explanations
- Skip practice problems
- Give up after one attempt

### Using Math Notation

The tutor understands math in plain text:
- `x^2` for x squared
- `3/4` for three fourths
- `sqrt(x)` for square root of x
- Responses will show proper math notation

### Making Progress

1. **Start with chat** to understand concepts
2. **Practice regularly** with generated problems
3. **Check progress** to identify weak areas
4. **Focus practice** on topics that need work
5. **Review sessions** to reinforce learning

## Common Issues

### "API key not configured"
- Make sure you edited the `.env` file
- Check that your API key is correct
- Restart the application after changing `.env`

### "Module not found"
- Run `python setup.py` again
- Make sure you're in the `math_tutor` directory
- Try: `pip install -r requirements.txt`

### Application won't start
- Check Python version: `python --version` (needs 3.9+)
- Make sure port 8501 isn't already in use
- Try closing and restarting

## Advanced Features

### Multiple Students

Create multiple student profiles:
- Each student has separate progress tracking
- Switch between students in the sidebar
- All data is saved separately

### Session History

Access previous tutoring sessions:
- View past conversations
- Continue where you left off
- Review what you learned

### Study Materials

The AI can generate:
- Custom study guides
- Practice problem sets
- Test preparation materials
- Concept explanations

## Getting More Help

### In the App
- Check the "Tips" expandable sections in each page
- Use the quick start buttons in Chat
- View recommendations in Progress page

### Documentation
- See `README.md` for full documentation
- Check `DEPLOYMENT.md` for cloud deployment
- Review `config.yaml` for customization options

## What's Next?

### For Students
1. Work through problems regularly
2. Ask questions when stuck
3. Track your progress
4. Celebrate improvements!

### For Deployment
Ready to deploy to the cloud?
- See `DEPLOYMENT.md` for instructions
- Enable authentication in `.env`
- Use PostgreSQL for production database

## Support

Having issues? Here's how to get help:

1. Check this guide first
2. Review error messages carefully
3. Make sure all prerequisites are installed
4. Try running setup again

## Pro Tips

🎯 **Daily Practice**: 15-20 minutes per day is better than long sessions

📊 **Track Progress**: Check your progress page weekly to see improvement

💡 **Ask Why**: Don't just solve problems - understand WHY solutions work

🎓 **Be Consistent**: Regular practice leads to mastery

🔄 **Review**: Revisit challenging topics periodically

---

**Ready to master math? Start chatting with your AI tutor now!** 🚀

