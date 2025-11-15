# master mAIthematics - AI Math Tutor

An interactive AI-powered mathematics tutoring application for high school students, designed by Troy A. Brumfield.

## Features

### 🤖 Interactive AI Tutoring
- Real-time chat with an AI math tutor powered by Claude Sonnet 4.5
- Natural, conversational explanations at 5th grade reading level
- Personalized guidance based on student grade level and learning style

### ✍️ Interactive Practice Problems
- Generate custom practice problems by topic and difficulty
- Submit answers and receive instant AI feedback
- Get guided hints without revealing the full solution
- Track completion progress in real-time

### 📊 Progress Tracking
- Monitor performance across different topics
- View session history and activity timeline
- Identify weak areas and get personalized recommendations

### 📁 File Upload Support
- Upload homework images or PDFs
- Multi-file support with drag-and-drop
- Mobile-friendly camera integration

## Installation

### Prerequisites
- Python 3.9 or higher
- Anthropic API key ([Get one here](https://www.anthropic.com))

### Quick Start

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd math_tutor
```

2. **Run setup**
```bash
python setup.py
```

This will:
- Install all required dependencies
- Create the database
- Set up configuration files

3. **Configure API Key**
- Copy `env_template.txt` to `.env`
- Add your Anthropic API key:
```
ANTHROPIC_API_KEY=your_key_here
```

4. **Launch the application**
```bash
python launch.py
```

Or use the GUI launcher:
```bash
python gui_launcher.py
```

## Project Structure

```
math_tutor/
├── app.py                 # Main Streamlit application
├── pages/                 # Multi-page app sections
│   ├── 1_Chat.py         # Interactive chat interface
│   ├── 2_Practice.py     # Practice problems with AI feedback
│   └── 3_Progress.py     # Progress tracking and analytics
├── src/                   # Core application logic
│   ├── ai/               # AI client and prompts
│   ├── core/             # Business logic
│   ├── database/         # Database models and management
│   └── utils/            # Utility functions
├── data/                  # Data files
│   └── system_instructions.txt  # AI tutor personality
└── requirements.txt       # Python dependencies
```

## Usage

### Creating a Student Profile
1. Launch the app
2. Enter student name and grade level
3. Select learning preferences
4. Start learning!

### Getting Help with Homework
1. Navigate to Chat page
2. Click "Help with Homework"
3. Upload a photo or type the problem
4. Receive step-by-step guidance

### Practicing Math Problems
1. Go to Practice page
2. Select a topic and difficulty level
3. Click "Generate Problems"
4. Enter your answers and click "Check"
5. Receive personalized feedback from the AI tutor

### Tracking Progress
1. Visit Progress page
2. View topic mastery charts
3. Review recent activity
4. Get recommendations for improvement

## Technology Stack

- **Frontend**: Streamlit
- **AI**: Anthropic Claude (Sonnet 4.5)
- **Database**: SQLite with SQLAlchemy ORM
- **Python Version**: 3.9+

## Features Highlights

### Clean, Professional Design
- No emojis, professional symbols only
- Purple gradient color scheme
- Responsive layout for mobile and desktop
- Bluxstudio-inspired modern UI

### Smart AI Tutoring
- Checks answers and provides feedback
- Guides students without giving direct answers
- Adapts to student's level
- Natural conversation flow

### Privacy & Data
- All data stored locally
- No third-party analytics
- Student information stays on your machine

## Configuration

### AI Model Selection
Edit `.env` to change the AI model:
```
AI_MODEL=claude-sonnet-4-5-20250929
```

### Custom Topics
Edit `src/utils/config.py` to add or modify math topics.

## Troubleshooting

### API Key Issues
- Verify your API key is active at anthropic.com
- Check that it's correctly entered in `.env`
- Ensure no extra spaces or quotes

### Database Errors
- Delete `data/tutoring.db` and run `python setup.py` again
- This will create a fresh database

### Installation Problems
- Make sure Python 3.9+ is installed
- Try: `pip install --upgrade pip`
- On Windows, you may need Visual C++ Build Tools for some packages

## Credits

**Designed by Troy A. Brumfield**

Powered by:
- Anthropic Claude AI
- Streamlit
- SQLAlchemy

## License

This project is for educational purposes.

## Support

For issues or questions, please open an issue on GitHub.

---

**Happy Learning! 📚**
