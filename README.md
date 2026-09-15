# 📄 AI Resume Analyzer

A Flask web app that uses the Claude API to analyze resumes and give instant, structured feedback — score, strengths, weaknesses, missing keywords, and improvement suggestions.

---

## 🧠 How It Works

1. User uploads a resume (PDF or TXT) through the web page.
2. Flask extracts the text from the file (`PyPDF2` for PDFs).
3. The extracted text — plus an optional target job role — is sent to the Claude API with a structured prompt.
4. Claude analyzes the resume and returns a score, strengths, weaknesses, missing keywords, and suggestions.
5. The result is displayed back on a results page.

---

## ✨ Features
- Upload a resume as PDF or TXT
- Optional target job role for tailored feedback
- AI-generated score out of 100
- Strengths, weaknesses, missing keywords, and ATS compatibility notes
- Clean, dark-themed UI

## 🛠️ Tech Stack
- **Backend:** Flask (Python)
- **AI:** Anthropic Claude API
- **PDF Parsing:** PyPDF2

---

## 🚀 Setup — Step by Step

### Step 1: Clone the repository
Download the project to your computer.
```bash
git clone https://github.com/<your-username>/ai-resume-analyzer.git
cd ai-resume-analyzer
```

### Step 2: Create a virtual environment
This keeps the project's Python packages separate from your system.
```bash
python -m venv venv
```
Activate it:
```bash
# On Mac/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```
You'll know it's active when you see `(venv)` at the start of your terminal line.

### Step 3: Install dependencies
This installs Flask, the Claude API library, and PDF-reading tools.
```bash
pip install -r requirements.txt
```

### Step 4: Get your Claude API key
1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up / log in
3. Create an API key from the dashboard
4. Copy the key — you'll need it in the next step

### Step 5: Set your API key as an environment variable
This keeps your key secret and out of your code.
```bash
# On Mac/Linux
export ANTHROPIC_API_KEY="your-api-key-here"

# On Windows (Command Prompt)
set ANTHROPIC_API_KEY=your-api-key-here
```

### Step 6: Run the app
```bash
python app.py
```

### Step 7: Open it in your browser
Go to:
