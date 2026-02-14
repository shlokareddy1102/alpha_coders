🚀 Alpha Coders
AI-Powered Intelligent Candidate Ranking System
Built for SUDHEE 2026 – CBIT Hackathon
📌 Overview
Alpha Coders is an AI-driven candidate evaluation platform that ranks students based on real technical signals from:
Coding platforms (LeetCode)
Development platforms (GitHub)
Professional presence (LinkedIn)
Resume content
Instead of relying only on static resumes, the system uses NLP + embeddings + weighted scoring algorithms to evaluate real-world technical competency and match candidates to a specific job description.
❗ Problem Statement
Traditional hiring pipelines suffer from:
Resume keyword stuffing
Lack of practical skill validation
Manual shortlisting bias
No structured evaluation of GitHub/LeetCode activity
Recruiters miss out on strong candidates due to poor resume formatting or incomplete keyword alignment.
💡 Our Solution
Alpha Coders introduces an AI-powered ranking engine that:
Extracts required skills from a Job Description using NLP
Converts candidate profiles into semantic embeddings
Computes similarity scores between candidate skill vectors and job vectors
Applies a weighted scoring system across platforms
Ranks candidates objectively
Provides explainable insights
🧠 How It Works
Step 1 – Data Input
Candidate database (LeetCode, GitHub, LinkedIn, Resume)
Job description text
Step 2 – Skill Extraction
NLP-based keyword extraction
Technical skill normalization
Domain categorization
Step 3 – Embedding Generation
Convert job description into vector embedding
Convert candidate profiles into vector embeddings
Store embeddings in database
Step 4 – Matching Algorithm
Cosine similarity computation
Platform-weighted scoring
Skill gap calculation
Step 5 – Intelligent Ranking
Final composite score
Ranked list (most suitable → least suitable)
Explainable breakdown of score
🏗️ System Architecture
'''bash
Frontend (HTML, CSS, JS)
        ↓
Backend API (Python)
        ↓
Skill Extraction + Embedding Engine
        ↓
MongoDB (Candidate Data + Embeddings)
        ↓
Ranking & Scoring Module
'''
⚙️ Tech Stack
🖥️ Backend
Python
Scikit-learn
NLP (TF-IDF / Embeddings)
REST APIs
🌐 Frontend
HTML
CSS
JavaScript
🗄️ Database
MongoDB
Stored candidate embeddings
🎯 Core Features
✔ Multi-platform skill aggregation
✔ Embedding-based semantic matching
✔ Weighted scoring system
✔ Explainable AI ranking
✔ Bias-reduced candidate screening
✔ Skill gap analysis for students
✔ Recruiter-friendly ranking dashboard
📊 Scoring Logic
Final Score =
LeetCode Performance Weight
GitHub Activity Weight
LinkedIn Skill Match
Resume Keyword Match
Embedding Similarity Score
Each platform contributes differently based on recruiter-defined importance.
🔍 Example Use Case
Recruiter inputs:
"Looking for a MERN stack developer with strong DSA and backend skills."
System will:
Extract MERN + DSA + Backend as key vectors
Compare against all candidate embeddings
Rank candidates based on semantic closeness
Highlight missing or strong skills
🚀 Why This Project Stands Out
Uses real-world data signals
Embedding-based semantic understanding (not just keyword matching)
Recruiter-focused explainability
Scalable architecture
Hackathon-ready but production-expandable
👥 Team Alpha Coders
Siddhi Sritha Shetkar – Team Lead - Frontend & UI
Ailapuram Sai Shloka Reddy – Backend & Database
Sanjana Donthireddy – AI Systems
🔮 Future Improvements
Live API integration with GitHub & LeetCode
LLM-powered skill inference
Dashboard analytics for recruiters
Candidate performance trend graphs
Bias detection auditing module
