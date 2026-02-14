# 🚀 Alpha Coders  
## AI-Powered Intelligent Candidate Ranking System  
**Built for SUDHEE 2026 – CBIT Hackathon**

---

## 📌 Overview  

**Alpha Coders** is an AI-driven candidate evaluation platform that ranks students based on real technical signals extracted from:

- Coding platforms (LeetCode)  
- Development platforms (GitHub)  
- Professional presence (LinkedIn)  
- Resume content  

Instead of relying solely on static resumes, the system uses **Natural Language Processing (NLP), semantic embeddings, and weighted scoring algorithms** to evaluate real-world technical competency and match candidates to a given job description.

---

## ❗ Problem Statement  

Modern hiring pipelines face several challenges:

- Resume keyword stuffing  
- Poor validation of practical skills  
- Manual shortlisting bias  
- No structured evaluation of GitHub or LeetCode activity  
- Over-reliance on resume formatting  

As a result, strong candidates are often overlooked due to weak keyword alignment or presentation issues.

---

## 💡 Our Solution  

Alpha Coders introduces an intelligent ranking engine that:

- Extracts required skills from job descriptions using NLP  
- Converts candidate profiles into semantic embeddings  
- Computes similarity between job vectors and candidate vectors  
- Applies platform-wise weighted scoring  
- Generates an objective ranked shortlist  
- Provides explainable breakdown of scores  

---

## 🧠 How It Works  

### Step 1 – Data Input  
- Candidate database (LeetCode, GitHub, LinkedIn, Resume)  
- Recruiter-provided job description  

### Step 2 – Skill Extraction  
- NLP-based keyword extraction  
- Technical skill normalization  
- Domain classification  

### Step 3 – Embedding Generation  
- Convert job description into vector embeddings  
- Convert candidate profiles into vector embeddings  
- Store embeddings inside MongoDB  

### Step 4 – Matching Algorithm  
- Cosine similarity computation  
- Platform-weighted scoring  
- Skill gap identification  

### Step 5 – Intelligent Ranking  
- Composite final score calculation  
- Ranked output (Most suitable → Least suitable)  
- Explainable score breakdown  

---

## 🏗️ System Architecture  

```text
Frontend (HTML, CSS, JavaScript)
        ↓
Backend API (Python)
        ↓
Skill Extraction & Embedding Engine
        ↓
MongoDB (Candidate Data + Stored Embeddings)
        ↓
Ranking & Scoring Module
```

---

## ⚙️ Tech Stack  

### Backend  
- Python  
- FastAPI
- Vector Embeddings
- REST APIs  

### Frontend  
- HTML  
- CSS  
- JavaScript  

### Database  
- MongoDB  
- Pre-computed candidate embeddings  

---

## 🎯 Core Features  

- Multi-platform skill aggregation  
- Embedding-based semantic matching  
- Customizable weighted scoring system  
- Explainable AI ranking  
- Bias-reduced candidate screening  
- Skill gap analysis for students  
- Recruiter-friendly ranking dashboard  

---

## 📊 Scoring Logic  

```
Final Score =
  (LeetCode Performance × Weight₁)
+ (GitHub Activity × Weight₂)
+ (LinkedIn Skill Match × Weight₃)
+ (Resume Keyword Match × Weight₄)
+ (Embedding Similarity Score × Weight₅)
```

Each platform contributes differently based on recruiter-defined importance.

---

## 🔍 Example Use Case  

**Recruiter Input:**

"Looking for a MERN stack developer with strong DSA and backend skills."

**System Process:**

- Extract MERN, DSA, Backend as skill vectors  
- Convert job description into semantic embedding  
- Match against all candidate embeddings  
- Compute similarity + weighted scores  
- Rank candidates by relevance  
- Highlight strong and missing skills  

---

## 👥 Team Alpha Coders  

- Siddhi Sritha Shetkar – Team Lead | Frontend & UI  
- Ailapuram SaiShloka Reddy – Backend & Database Systems  
- Sanjana Donthireddy – AI & Matching Engine  

---

## 🔮 Future Improvements  

- Live API integration with GitHub & LeetCode  
- LLM-powered skill inference  
- Advanced recruiter analytics dashboard  
- Candidate performance trend visualization  
- Bias detection & fairness auditing module  
- Real-time recruiter feedback learning loop  

