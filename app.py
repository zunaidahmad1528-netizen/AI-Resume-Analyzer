import os
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import anthropic
from PyPDF2 import PdfReader

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "txt"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text(filepath):
    if filepath.lower().endswith(".pdf"):
        reader = PdfReader(filepath)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def analyze_resume(resume_text, job_role=""):
    role_context = f" for a {job_role} role" if job_role else ""
    prompt = f"""You are an expert resume reviewer and career coach.
Analyze the following resume{role_context} and return your response in this exact structure:

1. OVERALL SCORE: (a number out of 100)
2. STRENGTHS: (3-5 bullet points)
3. WEAKNESSES: (3-5 bullet points)
4. MISSING KEYWORDS: (list relevant keywords the resume lacks, if a job role was provided)
5. IMPROVEMENT SUGGESTIONS: (3-5 concrete, actionable suggestions)
6. ATS COMPATIBILITY: (short note on formatting/parsing issues, if any)

Resume:
{resume_text}
"""

    message = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    if "resume" not in request.files:
        flash("No file uploaded")
        return redirect(url_for("index"))

    file = request.files["resume"]
    job_role = request.form.get("job_role", "").strip()

    if file.filename == "":
        flash("No file selected")
        return redirect(url_for("index"))

    if not allowed_file(file.filename):
        flash("Only PDF or TXT files are allowed")
        return redirect(url_for("index"))

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    try:
        resume_text = extract_text(filepath)
        if not resume_text.strip():
            flash("Could not extract any text from the uploaded file")
            return redirect(url_for("index"))

        analysis = analyze_resume(resume_text, job_role)
        return render_template("result.html", analysis=analysis, job_role=job_role)
    except Exception as e:
        flash(f"Something went wrong while analyzing: {e}")
        return redirect(url_for("index"))
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)


if __name__ == "__main__":
    app.run(debug=True)
