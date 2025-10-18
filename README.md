# SkillMatch — Complete Project

## Setup (Windows / macOS / Linux)

1. Create virtualenv:
   python -m venv venv
   # Windows PowerShell:
   .\venv\Scripts\Activate.ps1
   # macOS / Linux:
   source venv/bin/activate

2. Install requirements:
   pip install -r requirements.txt

3. Download SentenceTransformer model will occur automatically on first run.
   (Requires internet)

4. Run the app:
   python run.py

5. Open http://127.0.0.1:5000

Notes:
- Use Register → Login → Upload Resume.
- Uploaded PDFs are stored in instance/uploads/.
- To change secret key, set environment variable SKILLMATCH_SECRET.
