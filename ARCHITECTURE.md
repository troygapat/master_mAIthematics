# AI Math Tutor - System Architecture

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                          PRESENTATION LAYER                         │
│                         (Streamlit Frontend)                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │   app.py     │  │  1_Chat.py   │  │ 2_Practice.py│           │
│  │   (Home)     │  │   (Chat)     │  │  (Problems)  │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
│                                                                     │
│  ┌──────────────┐  ┌──────────────────────────────────┐           │
│  │3_Progress.py │  │      UI Components               │           │
│  │  (Analytics) │  │  • Chat widgets                  │           │
│  └──────────────┘  │  • Math renderer                 │           │
│                    │  • Progress charts               │           │
│                    └──────────────────────────────────┘           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                                 ↕
┌─────────────────────────────────────────────────────────────────────┐
│                        APPLICATION LAYER                            │
│                        (Business Logic)                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────────────┐  ┌──────────────────────┐              │
│  │ ConversationHandler  │  │   SessionManager     │              │
│  │ • handle_message()   │  │ • start_session()    │              │
│  │ • start_homework()   │  │ • get_messages()     │              │
│  │ • request_practice() │  │ • end_session()      │              │
│  └──────────────────────┘  └──────────────────────┘              │
│                                                                     │
│  ┌──────────────────────┐  ┌──────────────────────┐              │
│  │   StudentManager     │  │     AuthManager      │              │
│  │ • create_student()   │  │ • authenticate()     │              │
│  │ • get_summary()      │  │ • create_token()     │              │
│  │ • update_progress()  │  │ • verify_token()     │              │
│  └──────────────────────┘  └──────────────────────┘              │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                                 ↕
┌─────────────────────────────────────────────────────────────────────┐
│                      AI INTEGRATION LAYER                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────────────┐  ┌──────────────────────┐              │
│  │      AIClient        │  │   PromptBuilder      │              │
│  │ • chat()             │  │ • build_prompt()     │              │
│  │ • generate()         │  │ • format_homework()  │              │
│  │ • truncate_history() │  │ • format_practice()  │              │
│  └──────────────────────┘  └──────────────────────┘              │
│                                                                     │
│  ┌─────────────────────────────────────────┐                      │
│  │      System Instructions                │                      │
│  │  • Teaching methodology                 │                      │
│  │  • Communication standards              │                      │
│  │  • 5th grade reading level              │                      │
│  └─────────────────────────────────────────┘                      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                                 ↕
┌─────────────────────────────────────────────────────────────────────┐
│                      EXTERNAL SERVICES                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────────────────────────────────────┐                 │
│  │         Anthropic Claude API                 │                 │
│  │  • claude-3-5-sonnet-20241022               │                 │
│  │  • Natural language understanding           │                 │
│  │  • Educational conversation                 │                 │
│  └──────────────────────────────────────────────┘                 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                                 ↕
┌─────────────────────────────────────────────────────────────────────┐
│                         DATA LAYER                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────────────┐  ┌──────────────────────┐              │
│  │    DatabaseManager   │  │   SQLAlchemy ORM     │              │
│  │ • CRUD operations    │  │ • Models             │              │
│  │ • Session management │  │ • Relationships      │              │
│  │ • Query building     │  │ • Migrations         │              │
│  └──────────────────────┘  └──────────────────────┘              │
│                                                                     │
│  ┌─────────────────────────────────────────────┐                  │
│  │         Database (SQLite / PostgreSQL)      │                  │
│  │                                             │                  │
│  │  ┌─────────┐ ┌─────────┐ ┌──────────┐     │                  │
│  │  │Students │ │Sessions │ │ Messages │     │                  │
│  │  └─────────┘ └─────────┘ └──────────┘     │                  │
│  │                                             │                  │
│  │  ┌─────────┐ ┌──────────┐ ┌──────────┐    │                  │
│  │  │Progress │ │Materials │ │ Problems │    │                  │
│  │  └─────────┘ └──────────┘ └──────────┘    │                  │
│  └─────────────────────────────────────────────┘                  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## 🔄 Data Flow

### Chat Conversation Flow

```
1. Student enters message in Chat UI (1_Chat.py)
                ↓
2. ConversationHandler.handle_message()
                ↓
3. SessionManager creates/retrieves session
                ↓
4. Save student message to database
                ↓
5. PromptBuilder builds context:
   • System instructions
   • Student profile (name, grade)
   • Conversation history
                ↓
6. AIClient sends to Anthropic Claude
                ↓
7. Claude generates response
                ↓
8. Save tutor response to database
                ↓
9. Update student last_active
                ↓
10. Display response in UI with LaTeX rendering
```

### Practice Problem Generation Flow

```
1. Student selects topic and difficulty (2_Practice.py)
                ↓
2. ConversationHandler.request_practice_problems()
                ↓
3. PromptBuilder.format_practice_request_prompt()
                ↓
4. AIClient generates problems
                ↓
5. Parse response (problems, answers, explanations)
                ↓
6. Save to StudyMaterial table
                ↓
7. Display in Practice UI
                ↓
8. Student works on problems
                ↓
9. Update Progress table when completed
```

### Progress Tracking Flow

```
1. Student completes practice/session
                ↓
2. DatabaseManager.update_progress()
                ↓
3. Calculate metrics:
   • Accuracy = successes / attempts
   • Skill level assessment
   • Last practiced timestamp
                ↓
4. Store in Progress table
                ↓
5. Progress page queries and displays:
   • Charts (Plotly)
   • Metrics
   • Recommendations
```

## 🗄️ Database Schema

### Entity Relationship Diagram

```
┌─────────────┐
│  Students   │
│─────────────│
│ id (PK)     │──┐
│ name        │  │
│ grade_level │  │
│ email       │  │
│ password_h. │  │
│ created_at  │  │
│ last_active │  │
└─────────────┘  │
                 │ 1:N
                 │
    ┌────────────┴──────────┬───────────────┬─────────────┐
    │                       │               │             │
    ↓                       ↓               ↓             ↓
┌──────────┐        ┌──────────┐    ┌──────────┐  ┌──────────┐
│ Sessions │        │ Progress │    │Materials │  │ Problems │
│──────────│        │──────────│    │──────────│  │──────────│
│ id (PK)  │──┐     │ id (PK)  │    │ id (PK)  │  │ id (PK)  │
│ stud_id  │  │     │ stud_id  │    │ stud_id  │  │ stud_id  │
│ topic    │  │     │ topic    │    │ title    │  │ topic    │
│ type     │  │     │ subtopic │    │ type     │  │ problem  │
│ start    │  │     │ accuracy │    │ content  │  │ answer   │
│ end      │  │     │ attempts │    │ created  │  │ correct  │
└──────────┘  │     │ level    │    └──────────┘  └──────────┘
              │     └──────────┘
              │ 1:N
              │
              ↓
        ┌──────────┐
        │ Messages │
        │──────────│
        │ id (PK)  │
        │ sess_id  │
        │ role     │
        │ content  │
        │ tokens   │
        │ metadata │
        └──────────┘
```

## 🔐 Security Architecture

### Authentication Flow (Optional)

```
┌─────────────┐
│   Browser   │
└─────┬───────┘
      │ 1. Email + Password
      ↓
┌─────────────┐
│ AuthManager │
└─────┬───────┘
      │ 2. Verify credentials
      │    (bcrypt password check)
      ↓
┌─────────────┐
│  Database   │
└─────┬───────┘
      │ 3. If valid, return Student
      ↓
┌─────────────┐
│ AuthManager │
│ create_token│
└─────┬───────┘
      │ 4. Generate JWT token
      ↓
┌─────────────┐
│   Browser   │
│ Store token │
└─────┬───────┘
      │ 5. Include token in requests
      ↓
┌─────────────┐
│ AuthManager │
│verify_token │
└─────┬───────┘
      │ 6. Validate token
      ↓
    Allow Access
```

### API Key Security

```
Environment Variables (.env)
        ↓
┌──────────────────┐
│   Config.py      │
│ Loads from env   │
└────────┬─────────┘
         │
         ↓
┌──────────────────┐
│   AIClient       │
│ Uses API key     │
└────────┬─────────┘
         │
         ↓
┌──────────────────┐
│ Anthropic API    │
│ Secure HTTPS     │
└──────────────────┘
```

## 📊 State Management

### Streamlit Session State

```python
st.session_state = {
    # Core managers (cached)
    'db_manager': DatabaseManager(),
    'ai_client': AIClient(),
    'student_manager': StudentManager(),
    'conversation_handler': ConversationHandler(),
    
    # Current state
    'current_student': Student | None,
    'current_session': int | None,
    
    # Chat state
    'chat_messages': List[Dict],
    'chat_session_id': int | None,
    
    # Practice state
    'practice_problems': List[Dict],
    'practice_content': str,
    'practice_topic': str,
    
    # Auth state (optional)
    'authenticated': bool,
    'auth_token': str | None
}
```

## 🔄 Component Interactions

### ConversationHandler Interactions

```
ConversationHandler
    │
    ├──→ SessionManager
    │       └──→ DatabaseManager
    │               └──→ Database
    │
    ├──→ StudentManager
    │       └──→ DatabaseManager
    │               └──→ Database
    │
    ├──→ AIClient
    │       └──→ Anthropic API
    │
    └──→ PromptBuilder
            └──→ System Instructions (file)
```

### Page → Manager → Database Flow

```
Streamlit Page
    │
    ├──→ Manager (e.g., ConversationHandler)
    │       │
    │       ├──→ Business Logic
    │       │
    │       ├──→ AIClient (if needed)
    │       │       └──→ Anthropic API
    │       │
    │       └──→ DatabaseManager
    │               │
    │               ├──→ SQLAlchemy Session
    │               │
    │               └──→ Database
    │
    └──→ Render Result in UI
```

## 🎯 Design Patterns Used

### 1. **Repository Pattern**
```
DatabaseManager = Repository
    • Abstracts database operations
    • Provides clean API for data access
    • Hides SQLAlchemy details
```

### 2. **Manager Pattern**
```
StudentManager, SessionManager, ConversationHandler
    • Business logic encapsulation
    • Orchestrates multiple operations
    • Manages transactions
```

### 3. **Factory Pattern**
```
PromptBuilder
    • Creates different types of prompts
    • Formats based on context
    • Centralizes prompt logic
```

### 4. **Singleton Pattern** (via Streamlit caching)
```
@st.cache_resource
def get_database_manager():
    return DatabaseManager()
    
# Same instance reused across requests
```

## 🚀 Deployment Architecture

### Development

```
Local Machine
    │
    ├──→ SQLite (file-based)
    ├──→ Python virtual environment
    └──→ Streamlit dev server (localhost:8501)
```

### Production (Cloud)

```
┌─────────────────────────────────────┐
│      Load Balancer / CDN            │
│      (HTTPS/SSL)                    │
└────────────┬────────────────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│    Streamlit Application Server(s)  │
│    (Multiple instances for scale)   │
└────────┬───────────┬────────────────┘
         │           │
         ↓           ↓
┌────────────┐  ┌──────────────┐
│ PostgreSQL │  │Anthropic API │
│  Database  │  │  (External)  │
│  (Managed) │  └──────────────┘
└────────────┘
```

## 📈 Performance Optimizations

### Caching Strategy

```
Level 1: Streamlit Cache
    @st.cache_resource
    • Database connections
    • AI client instances
    • Configuration objects
    
Level 2: Streamlit Data Cache
    @st.cache_data
    • Student progress data
    • Study materials
    • Static content
    
Level 3: Database Queries
    • Indexed columns
    • Efficient joins
    • Pagination
```

### Context Management

```
Conversation History
    │
    ├──→ Store all messages in DB
    │
    ├──→ Load recent N messages
    │
    ├──→ Truncate to fit token limit
    │       • Keep most recent
    │       • Stay under max tokens
    │
    └──→ Send to AI
```

## 🔍 Monitoring & Logging

### Application Logs

```
app.py
    │
    ├──→ User actions
    ├──→ API calls
    ├──→ Database operations
    ├──→ Errors & exceptions
    │
    └──→ Log file / stdout
```

### Metrics to Track

```
• API usage (tokens per day)
• Response times
• Error rates
• Active users
• Session durations
• Database query performance
```

## 🧪 Testing Strategy

### Unit Tests
```
tests/
    ├── test_ai_client.py
    ├── test_database.py
    ├── test_managers.py
    └── test_auth.py
```

### Integration Tests
```
• End-to-end conversation flow
• Database operations
• API integration
• Authentication flow
```

## 📦 Dependency Management

```
requirements.txt
    │
    ├──→ Production dependencies
    ├──→ Version pinning
    └──→ Security updates
    
Virtual Environment
    │
    ├──→ Isolated dependencies
    └──→ Reproducible builds
```

---

## Key Architectural Decisions

### ✅ Why Streamlit?
- Rapid development
- Python-native
- Built-in session management
- Easy deployment

### ✅ Why SQLAlchemy?
- Database abstraction
- Easy to switch DBs
- Type safety with models
- Query building

### ✅ Why Anthropic Claude?
- Best-in-class for education
- Long context window
- Excellent instruction following
- Safe and aligned

### ✅ Why SQLite → PostgreSQL?
- Start simple (SQLite)
- Scale when needed (PostgreSQL)
- Same code works for both
- Easy migration path

---

**This architecture supports:**
- 🚀 Rapid development
- 📈 Easy scaling
- 🔒 Secure deployment
- 🧪 Testable code
- 📊 Clear data flow
- 🎯 Separation of concerns

