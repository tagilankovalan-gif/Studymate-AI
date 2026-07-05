# 🎓 StudyMate AI

**StudyMate AI** is an intelligent, modern, and student-friendly web application designed to act as a 24/7 personal learning coach. Powered by the Google Gemini API and built using Python and Streamlit, StudyMate AI transforms study sessions into structured, engaging, and high-impact educational experiences.

---

## 🚀 Core Features

1. **🏠 Interactive Home**: An elegant welcome portal outlining key learning tip insights and features designed for student success.
2. **💬 Personal AI Tutor Chat**: A conversational assistant configured with academic system instructions to explain formulas, answer curriculum questions, and provide step-by-step guidance.
3. **📅 Dynamic Study Planner**: Converts exam dates, subject names, and daily study capacities into customized daily study calendars.
4. **📝 Smart Quiz Generator**: Instantly builds a challenging 5-question multiple-choice practice exam on any user-specified topic, complete with detailed educational explanations for answers.
5. **📈 Milestone Progress Tracker**: A personal task logger and accountability checklist that updates progress metrics and bars to maintain study momentum.
6. **⚖️ AI Ethics in Education**: Explains key ethics pillars (Fairness, Transparency, Privacy, Accountability, and Human Oversight) to encourage ethical AI use.

---

## 🛠️ Local Installation & Run Guide

To run StudyMate AI on your computer:

### 1. Prerequisites
Make sure you have Python 3.9+ installed.

### 2. Clone and Install Dependencies
Install all required libraries using pip:
```bash
pip install -r requirements.txt
```

### 3. Setup Gemini API Key
Obtain a free Gemini API key from [Google AI Studio](https://aistudio.google.com/). You can make this available locally by setting it in your terminal environment:
```bash
# On Linux/macOS
export GEMINI_API_KEY="your_api_key_here"

# On Windows (Command Prompt)
set GEMINI_API_KEY="your_api_key_here"

# On Windows (PowerShell)
$env:GEMINI_API_KEY="your_api_key_here"
```
*Note: If no environment variable is detected, you can also paste your API key directly into the secure input field in the application sidebar.*

### 4. Run the Application
Boot the Streamlit server:
```bash
streamlit run app.py
```
This will open the application in your default browser at `http://localhost:8501`.

---

## ☁️ Deployment on Streamlit Community Cloud

You can deploy StudyMate AI for free to Streamlit Community Cloud:

1. **Upload your code** to a public GitHub repository containing:
   - `app.py`
   - `requirements.txt`
2. **Log in** to [Streamlit Community Cloud](https://share.streamlit.io/) and click **"New app"**.
3. Select your repository, branch, and specify `app.py` as the main file path.
4. Expand the **Advanced settings** menu.
5. In the **Secrets** text box, paste your Gemini API key in TOML format:
   ```toml
   GEMINI_API_KEY = "your_actual_gemini_api_key_here"
   ```
6. Click **Deploy!** Your application is now live and securely authenticated.
