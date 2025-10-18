🧠 SkillMatch — AI-Powered Job Matching Platform

> A smart web application that analyzes resumes and instantly finds the best matching jobs based on skills and experience.



🚀 Overview
SkillMatch is an intelligent job recommendation platform built with Python and Flask, designed to help users discover the most relevant career opportunities by analyzing their resumes.

By leveraging Natural Language Processing (NLP), it automatically extracts skills and key keywords from uploaded CVs and compares them with a structured job dataset to calculate match scores— making the job search process faster, smarter, and more transparent.

🎯 Key Features

✅ Resume Upload & Parsing
Upload your CV (PDF), and SkillMatch will extract keywords and technical skills automatically.

✅ AI-Powered Job Matching
Compares extracted skills with a predefined job dataset using cosine similarity and keyword scoring.

✅ Instant Results
Displays top matching jobs ranked by percentage match.

✅ Simple & Clean Interface
Modern UI built with HTML, CSS, and Bootstrap for a smooth user experience.

✅ Local Privacy
All processing happens locally — no external data sharing.

⚙️ Tech Stack

| Category | Technologies |
|-----------|---------------|
| Frontend | HTML, CSS, Bootstrap |
| Backend | Python (Flask) |
| Data Analysis | Pandas, scikit-learn |
| NLP | spaCy / TF-IDF Vectorizer |
| Storage | CSV / Local Database |
| Deployment (Future) | Render / Railway / AWS |

🧩 System Workflow

1. User Uploads CV (PDF)
2. Text Extracted from Resume
3. NLP-based Keyword Extraction
4. Job Dataset Comparison (using TF-IDF / cosine similarity)
5. Top Job Matches Displayed with Scores



