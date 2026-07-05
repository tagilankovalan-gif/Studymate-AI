import streamlit as st
import os
import json
import datetime
import google.generativeai as genai

# ----------------------------------------------------
# 1. PAGE CONFIGURATION & THEME STYLING
# ----------------------------------------------------
st.set_page_config(
    page_title="StudyMate AI - Your Smart Learning Companion",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern Blue and White Student-Friendly Interface
st.markdown("""
<style>
    /* Main container background */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* Header and Title Styles */
    h1, h2, h3 {
        color: #1E3A8A !important; /* Deep Blue */
        font-family: 'Inter', sans-serif;
    }
    
    /* Custom Card Style */
    .study-card {
        background-color: #FFFFFF;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    
    /* Sidebar styling */
    .css-110u7m1, .css-1d391kg {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0;
    }
    
    /* Custom button primary styling */
    div.stButton > button:first-child {
        background-color: #2563EB !important; /* Royal Blue */
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease-in-out;
    }
    
    div.stButton > button:first-child:hover {
        background-color: #1D4ED8 !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
    }
    
    /* Custom status / info banners */
    .stAlert {
        border-radius: 8px !important;
    }
    
    /* Sidebar branding header */
    .sidebar-brand {
        font-size: 24px;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 20px;
        text-align: center;
        border-bottom: 2px solid #EFF6FF;
        padding-bottom: 12px;
    }
    
    /* Ethics Item Highlight */
    .ethics-card {
        background-color: #FFFFFF;
        border-left: 5px solid #2563EB;
        padding: 16px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 16px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 2. API KEY VALIDATION & GEMINI CONFIGURATION
# ----------------------------------------------------
# Prioritize Streamlit secrets, then OS environment variables, then sidebar input
api_key = None
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
elif os.environ.get("GEMINI_API_KEY"):
    api_key = os.environ.get("GEMINI_API_KEY")

# Sidebar navigation header & API input
with st.sidebar:
    st.markdown('<div class="sidebar-brand">🎓 StudyMate AI</div>', unsafe_allow_html=True)
    
    # If key wasn't found automatically, ask the user
    if not api_key:
        api_key = st.text_input(
            "Enter Gemini API Key:", 
            type="password", 
            placeholder="AI Studio API Key",
            help="Get an API key from Google AI Studio. It is kept secure."
        )
        if api_key:
            st.success("API Key successfully registered!")
    else:
        st.markdown("🟢 **Gemini API Connected**")

# Configure GenAI SDK if API key is present
if api_key:
    genai.configure(api_key=api_key)

# ----------------------------------------------------
# 3. SIDEBAR NAVIGATION
# ----------------------------------------------------
pages = ["🏠 Home", "💬 AI Chat", "📅 Study Planner", "📝 Quiz Generator", "📈 Progress Tracker", "⚖️ About AI Ethics"]
selected_page = st.sidebar.radio("Navigate", pages)

# ----------------------------------------------------
# 4. PAGE IMPLEMENTATION
# ----------------------------------------------------

# PAGE 1: HOME
if selected_page == "🏠 Home":
    st.title("Welcome to StudyMate AI! 📚")
    st.subheader("Your Intelligent, Modern Student Companion")
    
    st.markdown("""
    StudyMate AI leverages cutting-edge artificial intelligence to transform the way you learn, organize, and excel in your studies. 
    Designed specifically for students, it provides high-quality guidance, personalized test prep, and customized organizational planners.
    """)
    
    # Decorative visual banner
    st.info("💡 **Fun study tip:** Short, regular study sessions (the Pomodoro technique) are far more effective than marathon cramming sessions!")
    
    # Interactive features grid using columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="study-card">
            <h3>💬 Personal AI Tutor Chat</h3>
            <p>Get instant answers to complex questions, step-by-step explanations for mathematical equations, or language translation and grammar checks. Available 24/7.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="study-card">
            <h3>📝 Multiple Choice Quiz Generator</h3>
            <p>Generate automated, challenging multiple-choice questions on any subject area using Gemini. Test yourself and read detailed feedback on why each answer is correct.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="study-card">
            <h3>📅 Dynamic Study Planner</h3>
            <p>Convert any subject outline or exam date into an organized day-by-day study calendar, distributed based on your daily available study hours.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="study-card">
            <h3>📈 Milestone Progress Tracker</h3>
            <p>Stay motivated! Log your tasks, mark off study milestones, and watch your progress bar climb. Track your journey to academic success.</p>
        </div>
        """, unsafe_allow_html=True)

    # Call to action footer
    st.markdown("<br><p style='text-align: center; color: #64748B;'>Select a tool in the left sidebar navigation to begin your journey!</p>", unsafe_allow_html=True)


# PAGE 2: AI CHAT
elif selected_page == "💬 AI Chat":
    st.title("💬 AI Tutor Chat")
    st.subheader("Ask academic questions and receive guided, step-by-step learning support")
    
    if not api_key:
        st.warning("⚠️ Please provide a Gemini API Key in the left sidebar to start chatting.")
    else:
        # Initialize message history
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
            
        # Clear chat history button
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()
            
        # Display existing messages
        for message in st.session_state.chat_history:
            role = message["role"]
            with st.chat_message(role):
                st.markdown(message["content"])
                
        # Handle new user input
        user_prompt = st.chat_input("Ask StudyMate AI anything (e.g., 'Explain Photosynthesis simply' or 'Solve x^2 - 5x + 6 = 0')")
        
        if user_prompt:
            # Display user message
            with st.chat_message("user"):
                st.markdown(user_prompt)
            st.session_state.chat_history.append({"role": "user", "content": user_prompt})
            
            # Request response from Gemini
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                with st.spinner("Analyzing and preparing explanation..."):
                    try:
                        # Construct a conversational wrapper
                        model = genai.GenerativeModel(
                            model_name="gemini-1.5-flash", # Robust fallback for streamlit
                            system_instruction="You are StudyMate AI, a friendly, modern, and encouraging academic tutor. Help the student understand complex concepts, solve homework problems step-by-step, explain equations, or practice language skills. Keep your answers clear, concise, and structured with clean markdown. Always maintain an encouraging and positive educational tone."
                        )
                        
                        # Prepare context
                        contents = []
                        for m in st.session_state.chat_history[-10:]: # Pass recent history
                            contents.append({"role": m["role"] if m["role"] == "user" else "model", "parts": [m["content"]]})
                        
                        response = model.generate_content(contents)
                        response_text = response.text
                        
                        message_placeholder.markdown(response_text)
                        st.session_state.chat_history.append({"role": "assistant", "content": response_text})
                    except Exception as e:
                        st.error(f"Failed to communicate with Gemini: {str(e)}")


# PAGE 3: STUDY PLANNER
elif selected_page == "📅 Study Planner":
    st.title("📅 Dynamic Study Planner")
    st.subheader("Turn any test or subject into a structural, stress-free day-by-day plan")
    
    if not api_key:
        st.warning("⚠️ Please provide a Gemini API Key in the left sidebar to generate study schedules.")
    else:
        with st.form("planner_form"):
            col1, col2, col3 = st.columns(3)
            with col1:
                subject = st.text_input("What subject/exam are you studying for?", placeholder="e.g., AP Chemistry Midterm")
            with col2:
                exam_date = st.date_input("When is the Exam Date?", min_value=datetime.date.today())
            with col3:
                hours_per_day = st.number_input("Study commitment (Hours per day)", min_value=0.5, max_value=12.0, value=2.0, step=0.5)
                
            submit_plan = st.form_submit_button("📅 Generate Study Plan")
            
        if submit_plan:
            if not subject:
                st.error("Please enter a valid subject or exam name.")
            else:
                days_left = (exam_date - datetime.date.today()).days
                if days_left < 0:
                    st.error("The selected exam date cannot be in the past.")
                else:
                    with st.spinner("Crafting your optimized study schedule with StudyMate AI..."):
                        try:
                            model = genai.GenerativeModel("gemini-1.5-flash")
                            prompt = f"""
                            Generate a highly detailed day-by-day study plan for the subject: "{subject}".
                            The exam is in exactly {days_left} days (Date: {exam_date}).
                            I can study for {hours_per_day} hours each day.
                            Provide:
                            1. An overview of the main strategy.
                            2. Key Milestones to cross.
                            3. A structured chronological breakdown of topics and actionable items.
                            Organize it beautifully using headers, bullet points, and markdown tables. Make sure it is realistic and manageable.
                            """
                            response = model.generate_content(prompt)
                            
                            st.success("✨ Your customized Study Plan has been successfully generated!")
                            
                            # Display response
                            st.markdown(response.text)
                            
                            # Option to add to Progress tracker automatically (stored in session state)
                            if "schedule_tasks" not in st.session_state:
                                st.session_state.schedule_tasks = []
                            
                            # Simple extraction for milestone adding
                            st.info("💡 You can manually log milestones or daily tasks from this plan in the **Progress Tracker** tab to stay accountable!")
                        except Exception as e:
                            st.error(f"Error generating study plan: {str(e)}")


# PAGE 4: QUIZ GENERATOR
elif selected_page == "📝 Quiz Generator":
    st.title("📝 Quiz Generator")
    st.subheader("Test your understanding and master the material through instant AI-generated quizzes")
    
    if not api_key:
        st.warning("⚠️ Please provide a Gemini API Key in the left sidebar to generate quizzes.")
    else:
        topic = st.text_input("Enter the topic or subject you want to practice:", placeholder="e.g., Mitosis vs Meiosis, Calculus Limits, World War II Causes")
        
        # Initialize quiz session variables
        if "active_quiz" not in st.session_state:
            st.session_state.active_quiz = None
            st.session_state.quiz_score = None
            
        generate_quiz = st.button("🚀 Generate 5 MCQs")
        
        if generate_quiz:
            if not topic:
                st.error("Please enter a topic first.")
            else:
                with st.spinner("Constructing 5 custom educational questions with solutions..."):
                    try:
                        # Use Gemini to generate a JSON array of 5 questions
                        model = genai.GenerativeModel("gemini-1.5-flash")
                        prompt = f"""
                        Generate exactly 5 multiple-choice questions (MCQs) for the topic: "{topic}".
                        Each question must have exactly 4 options, a correct answer index (0, 1, 2, or 3), and a clear constructive explanation of why it is correct.
                        You must return strictly valid JSON matching this schema:
                        [
                          {{
                            "question": "question text",
                            "options": ["option A", "option B", "option C", "option D"],
                            "correctAnswerIndex": 0,
                            "explanation": "why correct explanation text"
                          }}
                        ]
                        Make sure your response contains ONLY the raw JSON string, no markdown headers or ```json wrappers.
                        """
                        response = model.generate_content(prompt)
                        
                        # Strip markdown wrappers if returned
                        clean_text = response.text.replace("```json", "").replace("```", "").strip()
                        questions_data = json.loads(clean_text)
                        
                        if len(questions_data) > 0:
                            st.session_state.active_quiz = questions_data
                            st.session_state.quiz_score = None
                            st.session_state.submitted_answers = {}
                        else:
                            st.error("Could not parse valid quiz questions. Please try again.")
                    except Exception as e:
                        st.error(f"Error generating quiz questions: {str(e)}")
                        st.info("Tip: Double check your API key status and network connection.")
                        
        # Render active quiz
        if st.session_state.active_quiz:
            st.write("---")
            st.success(f"📖 Quiz Loaded successfully! Choose your answers below:")
            
            answers = {}
            for idx, item in enumerate(st.session_state.active_quiz):
                st.markdown(f"**Q{idx+1}: {item['question']}**")
                selected_opt = st.radio(
                    f"Select option for Q{idx+1}:", 
                    options=item['options'], 
                    key=f"q_{idx}",
                    index=None
                )
                answers[idx] = selected_opt
                st.write("")
                
            submit_quiz = st.button("✅ Submit Answers")
            
            if submit_quiz:
                correct_count = 0
                unanswered = False
                
                # Double-check all answered
                for idx in range(len(st.session_state.active_quiz)):
                    if answers[idx] is None:
                        unanswered = True
                        
                if unanswered:
                    st.warning("⚠️ Please answer all questions before submitting.")
                else:
                    st.markdown("### 📊 Quiz Results & Review")
                    for idx, item in enumerate(st.session_state.active_quiz):
                        user_ans = answers[idx]
                        correct_opt = item['options'][item['correctAnswerIndex']]
                        is_correct = (user_ans == correct_opt)
                        
                        if is_correct:
                            correct_count += 1
                            st.markdown(f"✅ **Q{idx+1}: Correct!**")
                        else:
                            st.markdown(f"❌ **Q{idx+1}: Incorrect**")
                            st.write(f"*Your answer:* {user_ans}")
                        
                        st.write(f"**Correct answer:** {correct_opt}")
                        st.info(f"📚 **Explanation:** {item['explanation']}")
                        st.write("---")
                        
                    score_percentage = (correct_count / len(st.session_state.active_quiz)) * 100
                    st.metric(label="Your Score", value=f"{correct_count} / {len(st.session_state.active_quiz)}", delta=f"{score_percentage}%")
                    
                    if correct_count == 5:
                        st.balloons()
                        st.success("🎉 Outstanding job! Absolute perfection!")
                    elif correct_count >= 3:
                        st.success("👍 Good effort! Review the explanations to achieve a perfect score.")
                    else:
                        st.warning("💪 Keep learning! Review the topic or ask StudyMate AI Chat to explain these concepts further.")


# PAGE 5: PROGRESS TRACKER
elif selected_page == "📈 Progress Tracker":
    st.title("📈 Milestone Progress Tracker")
    st.subheader("Stay accountable, log study completed hours, and hit your milestones")
    
    # Initialize tasks in session state
    if "tracker_tasks" not in st.session_state:
        st.session_state.tracker_tasks = [
            {"id": 1, "task": "Read chapter 1 of textbook", "done": True, "hours": 1.5},
            {"id": 2, "task": "Attempt quiz on cell division", "done": False, "hours": 1.0},
            {"id": 3, "task": "Review math practice problems", "done": False, "hours": 2.0}
        ]
        
    # Form to add new task
    st.markdown("### ➕ Add New Study Session / Milestone")
    with st.form("new_task_form"):
        col1, col2 = st.columns([3, 1])
        with col1:
            new_task_text = st.text_input("What task did you accomplish or schedule?", placeholder="e.g., Reviewed physics notes for 2 hours")
        with col2:
            task_hours = st.number_input("Duration (Hours)", min_value=0.1, max_value=12.0, value=1.0, step=0.5)
            
        submit_task = st.form_submit_button("⚡ Add Task")
        
    if submit_task and new_task_text:
        new_id = len(st.session_state.tracker_tasks) + 1
        st.session_state.tracker_tasks.append({
            "id": new_id,
            "task": new_text_input := new_task_text,
            "done": False,
            "hours": task_hours
        })
        st.success(f"Added task: '{new_task_text}'")
        st.rerun()

    # Task List Section
    st.markdown("### 📝 Active Tasks & Milestones")
    
    if len(st.session_state.tracker_tasks) == 0:
        st.info("You don't have any study tasks logged. Add one above to start tracking your progress!")
    else:
        completed_hours = 0.0
        total_hours = 0.0
        completed_count = 0
        updated_tasks = []
        
        # Display each checkbox and record changes
        for item in st.session_state.tracker_tasks:
            total_hours += item["hours"]
            if item["done"]:
                completed_hours += item["hours"]
                completed_count += 1
                
            # Render Checkbox
            checked = st.checkbox(f"{item['task']} ({item['hours']} hrs)", value=item["done"], key=f"task_check_{item['id']}")
            updated_tasks.append({
                "id": item["id"],
                "task": item["task"],
                "done": checked,
                "hours": item["hours"]
            })
            
        # Update session state on changes
        st.session_state.tracker_tasks = updated_tasks
        
        # Progress Calculation
        total_tasks = len(st.session_state.tracker_tasks)
        progress_percentage = (completed_count / total_tasks) if total_tasks > 0 else 0.0
        
        st.write("---")
        st.markdown("### 📊 Overall Statistics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Milestones Completed", f"{completed_count} / {total_tasks}")
        with col2:
            st.metric("Total Study Investment", f"{completed_hours:.1f} / {total_hours:.1f} hours")
        with col3:
            st.metric("Progress Rate", f"{progress_percentage * 100:.1f}%")
            
        # Progress Bar Display
        st.progress(progress_percentage)
        
        # Educational/Motivational Quotes
        if progress_percentage == 1.0:
            st.balloons()
            st.success("⭐ Perfect complete! You have conquered all your goals for today!")
        elif progress_percentage >= 0.5:
            st.info("🚀 Over halfway there! Keep pushing, study master!")
        elif progress_percentage > 0:
            st.info("🏃 Keep moving! Every small milestone builds massive knowledge!")


# PAGE 6: ABOUT (AI ETHICS)
elif selected_page == "⚖️ About AI Ethics":
    st.title("⚖️ AI Ethics in Education")
    st.subheader("Responsible learning in the age of artificial intelligence")
    
    st.markdown("""
    At **StudyMate AI**, we believe that Artificial Intelligence is a powerful tool to augment and enhance education — not replace the hard work, critical thinking, and integrity that defines true scholarship.
    Below is a breakdown of our adherence to core AI Ethics guidelines to ensure a safe, fair, and transparent environment for students:
    """)
    
    # 5 Pillars of AI Ethics
    st.markdown("""
    <div class="ethics-card">
        <h4>🤝 1. Fairness</h4>
        <p>Our educational models are designed to present balanced explanations without favoring specific socioeconomic or educational backgrounds. We continuously refine prompts to eliminate bias and keep our feedback objective, scientific, and encouraging for everyone.</p>
    </div>
    
    <div class="ethics-card">
        <h4>👁️ 2. Transparency</h4>
        <p>Transparency means you should always know when you are interacting with an AI. StudyMate AI clearly indicates generated answers, quizzes, and planners. We provide explicit educational explanations with our quiz questions so you can understand the reasoning and scientific facts behind every response.</p>
    </div>
    
    <div class="ethics-card">
        <h4>🛡️ 3. Privacy & Security</h4>
        <p>Your academic queries, planner criteria, and tracker information belong entirely to you. We do not store or sell student search data. Your API keys are handled server-side using standard encryption, meaning they are never exposed publicly or shared with third parties.</p>
    </div>
    
    <div class="ethics-card">
        <h4>🧠 4. Accountability</h4>
        <p>While generative AI is extremely advanced, it can occasionally experience 'hallucinations' or mathematical errors. We hold ourselves accountable for explaining these limitations, encouraging students to cross-reference primary sources, and providing options to report inaccurate responses to improve model training.</p>
    </div>
    
    <div class="ethics-card">
        <h4>👤 5. Human Oversight</h4>
        <p>AI is a study mate — a supportive coach, not a surrogate author. We strongly discourage using this platform to write whole essays or complete assignments for submission. StudyMate AI is engineered to explain the process, helping you build internal competence rather than outsourcing your homework.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("🎓 **Ethical Student Pledge:** *'I pledge to use StudyMate AI to understand principles, learn active study methods, and expand my mind. I will not use AI to commit plagiarism or bypass my own academic responsibilities.'*")
