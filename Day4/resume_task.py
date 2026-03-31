from google import genai
from dotenv import load_dotenv
import os
import json

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

load_dotenv()
client = genai.Client(api_key=os.getenv("gemini_api_key"))

# PROMPT
PROMPT = """
You are a resume evaluation system.

RULES:
1. ONLY use information explicitly present in the resume.
2. DO NOT assume or infer missing skills.
3. OUTPUT must be STRICT JSON only.

ANTI-PROMPTS:
- Do NOT assume Python knowledge
- Do NOT add extra text

OUTPUT FORMAT:
{
  "name": "",
  "skills": [],
  "python_present": false,
  "fit_for_python_role": "yes/no",
  "reason": ""
}

FEW-SHOT EXAMPLES:

Input:
Name: Amit
Skills: Python, SQL
Output:
{
  "name": "Amit",
  "skills": ["Python", "SQL"],
  "python_present": true,
  "fit_for_python_role": "yes",
  "reason": "Python is mentioned"
}

Input:
Name: Kajal
Skills: Java, C++
Output:
{
  "name": "Kajal",
  "skills": ["Java", "C++"],
  "python_present": false,
  "fit_for_python_role": "no",
  "reason": "Python not mentioned"
}
"""

print("Enter 1 for text input or 2 for file input:", end=" ")
mode = input().strip()

if mode == "1":
    resume = input("Enter your resume text: ").strip()

elif mode == "2":
    if PyPDF2 is None:
        raise RuntimeError("PyPDF2 missing. Install with: pip install PyPDF2")

    pdf_path = input("Enter PDF file path: ").strip()
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        resume_pages = []
        for page in reader.pages:
            resume_pages.append(page.extract_text() or "")
        resume = "\n".join(resume_pages)

else:
    raise ValueError("Invalid mode. Choose 1 or 2.")

response = client.models.generate_content(
    model="gemini-flash-latest",
    contents=PROMPT + "\n\nResume:\n" + resume
)

output = response.text

try:
    parsed = json.loads(output)
    if "eligibility" not in parsed:
        qualified = "Eligible" if parsed.get("python_present") else "Not Eligible"
        parsed["eligibility"] = qualified

    print(json.dumps(parsed, indent=2))
except json.JSONDecodeError:
    print("Invalid JSON:\n", output)