from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import numpy as np
from datetime import datetime
import uuid
import os
from fastapi.middleware.cors import CORSMiddleware

# Import all modules
from vector_engine import load_or_rebuild, match, add_or_update_vector, remove_vector
from github_fetcher import fetch_github_data_for_ai
from leetcode_fetcher import fetch_leetcode_data_for_ai
from ai_summarizer import generate_comprehensive_summary, generate_match_explanation,generate_dynamic_match_explanation
from file_handler import save_uploaded_file, get_file_path, UPLOAD_DIR, delete_student_files
from resume_summarizer import (
    summarize_resume_with_ai,
    summarize_linkedin_with_ai,
    create_comprehensive_profile_summary,
    extract_key_skills_from_resume
)

# Database imports - JUST USE THESE, DON'T REDEFINE!
from db import (
    save_student,
    get_student_by_uuid,
    get_students_by_numeric_ids,
    update_student,
    delete_student,
    get_all_students,
    get_next_numeric_id,
    students_collection,
)

app = FastAPI()

# Serve uploaded files
app.mount("/files", StaticFiles(directory=UPLOAD_DIR), name="files")

# Model
model = SentenceTransformer("all-MiniLM-L6-v2")


# =====================================================
# REQUEST MODELS
# =====================================================

class JobRequest(BaseModel):
    job_description: str



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for development
    allow_methods=["*"],
    allow_headers=["*"],
)
# =====================================================
# HELPER FUNCTIONS (ONLY ONES NOT IN db.py)
# =====================================================

def extract_pdf_text_from_disk(file_path):
    """Extract text from PDF stored on disk"""
    try:
        import pdfplumber
        with pdfplumber.open(file_path) as pdf:
            text = " ".join([page.extract_text() or "" for page in pdf.pages])
        return text
    except Exception as e:
        print(f"PDF extraction error: {e}")
        return ""


# =====================================================
# STARTUP EVENT
# =====================================================

@app.on_event("startup")
def startup_event():
    """Initialize FAISS index from MongoDB on server start"""
    print("🚀 Initializing FAISS...")
    students = get_all_students()  # ✅ Using db.py function

    student_records = [
        {"id": s["numeric_id"], "embedding": s["embedding"]}
        for s in students
        if "embedding" in s and "numeric_id" in s
    ]

    load_or_rebuild(student_records)
    print(f"✅ FAISS ready with {len(student_records)} students")


# =====================================================
# STUDENT REGISTRATION
# =====================================================

@app.post("/add-student")
async def add_student(
    name: str = Form(...),
    branch: str = Form(...),
    year: int = Form(...),
    skills: str = Form(...),
    github_username: str = Form(...),
    leetcode_username: str = Form(...),
    linkedin_pdf: UploadFile = File(...),
    resume_pdf: UploadFile = File(...)
):
    """Complete student registration with AI-powered resume analysis"""
    
    student_uuid = str(uuid.uuid4())
    student_numeric_id = get_next_numeric_id()  # ✅ Using db.py function
    
    print(f"\n{'='*70}")
    print(f"📝 REGISTERING STUDENT: {name}")
    print(f"{'='*70}")
    
    # STEP 1: SAVE PDFs TO DISK
    print("\n💾 STEP 1: Saving PDFs to disk...")
    resume_info = save_uploaded_file(resume_pdf, student_uuid, "resume")
    linkedin_info = save_uploaded_file(linkedin_pdf, student_uuid, "linkedin")
    print(f"   ✅ Resume: {resume_info['filename']}")
    print(f"   ✅ LinkedIn: {linkedin_info['filename']}")
    
    # STEP 2: PARSE PDFs FROM DISK
    print("\n📖 STEP 2: Extracting text from PDFs...")
    resume_text = extract_pdf_text_from_disk(resume_info["file_path"])
    linkedin_text = extract_pdf_text_from_disk(linkedin_info["file_path"])
    print(f"   ✅ Resume: {len(resume_text)} characters")
    print(f"   ✅ LinkedIn: {len(linkedin_text)} characters")
    
    # STEP 3: AI SUMMARIZE RESUME & LINKEDIN
    print("\n🤖 STEP 3: AI analyzing resume and LinkedIn...")
    ai_resume_summary = summarize_resume_with_ai(resume_text)
    print(f"   ✅ Resume summary: {ai_resume_summary[:80]}...")
    
    ai_linkedin_summary = summarize_linkedin_with_ai(linkedin_text)
    print(f"   ✅ LinkedIn summary: {ai_linkedin_summary[:80]}...")
    
    ai_extracted_skills = extract_key_skills_from_resume(resume_text)
    print(f"   ✅ AI found skills: {list(ai_extracted_skills.get('programming_languages', []))[:5]}")
    
    # STEP 4: FETCH GITHUB DATA
    print(f"\n🐙 STEP 4: Fetching GitHub data...")
    github_data = fetch_github_data_for_ai(github_username)
    if not github_data:
        github_data = {
            "username": github_username,
            "statistics": {"total_repos": 0, "total_stars": 0, "total_forks": 0},
            "languages": {},
            "notable_projects": [],
            "github_score": 0,
            "profile_url": f"https://github.com/{github_username}"
        }
    print(f"   ✅ Found {github_data['statistics']['total_repos']} repos")
    existing = students_collection.find_one({"github.username": github_username})
    if existing:
      raise HTTPException(
        status_code=400,
        detail=f"Student with GitHub username '{github_username}' already exists (ID: {existing['student_id']})"
    )
    # STEP 5: FETCH LEETCODE DATA
    print(f"\n💻 STEP 5: Fetching LeetCode data...")
    leetcode_data = fetch_leetcode_data_for_ai(leetcode_username)
    if not leetcode_data:
        leetcode_data = {
            "username": leetcode_username,
            "problems_solved": {"total": 0, "easy": 0, "medium": 0, "hard": 0},
            "top_topics": [],
            "coding_score": 0,
            "profile_url": f"https://leetcode.com/{leetcode_username}"
        }
    print(f"   ✅ Solved {leetcode_data['problems_solved']['total']} problems")
    
    # STEP 6: AI SUMMARIZE GITHUB & LEETCODE
    print("\n🤖 STEP 6: AI analyzing GitHub and LeetCode...")
    manual_skills = [s.strip() for s in skills.split(",") if s.strip()]
    
    student_data_for_ai = {
        "name": name,
        "branch": branch,
        "year": year,
        "skills": manual_skills,
        "github": github_data,
        "leetcode": leetcode_data
    }
    
    external_summaries = generate_comprehensive_summary(student_data_for_ai)
    print(f"   ✅ GitHub summary generated")
    print(f"   ✅ LeetCode summary generated")
    
    # STEP 7: CREATE MASTER SUMMARY
    print("\n🌟 STEP 7: Creating comprehensive profile summary...")
    master_summary = create_comprehensive_profile_summary(
        resume_text=resume_text,
        linkedin_text=linkedin_text,
        github_summary=external_summaries["github_summary"],
        leetcode_summary=external_summaries["leetcode_summary"],
        skills=manual_skills
    )
    print(f"   ✅ Master summary: {master_summary[:100]}...")
    
    # STEP 8: CREATE EMBEDDING
    print("\n🧠 STEP 8: Creating embedding for vector search...")
    profile_text = (
        f"{resume_text[:2000]} "
        f"{linkedin_text[:1000]} "
        f"AI Resume Summary: {ai_resume_summary} "
        f"AI LinkedIn Summary: {ai_linkedin_summary} "
        f"Name: {name}, Branch: {branch}, Year: {year} "
        f"Skills: {' '.join(manual_skills)} "
        f"GitHub: {external_summaries['github_summary']} "
        f"LeetCode: {external_summaries['leetcode_summary']}"
    )
    
    embedding = model.encode(profile_text)
    embedding = embedding / np.linalg.norm(embedding)
    embedding_list = embedding.tolist()
    print(f"   ✅ Embedding created: {len(embedding_list)}-D vector")
    
    # STEP 9: SAVE TO MONGODB
    print("\n💾 STEP 9: Saving to MongoDB...")
    student_document = {
        "student_id": student_uuid,
        "numeric_id": student_numeric_id,
        "name": name,
        "branch": branch,
        "year": year,
        "skills": manual_skills,
        "resume": resume_info,
        "linkedin": linkedin_info,
        "resume_text_preview": resume_text[:1000],
        "linkedin_text_preview": linkedin_text[:1000],
        "ai_resume_summary": ai_resume_summary,
        "ai_linkedin_summary": ai_linkedin_summary,
        "ai_extracted_skills": ai_extracted_skills,
        "master_summary": master_summary,
        "github": github_data,
        "leetcode": leetcode_data,
        "github_summary": external_summaries["github_summary"],
        "leetcode_summary": external_summaries["leetcode_summary"],
        "embedding": embedding_list,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    save_student(student_document)  # ✅ Using db.py function
    print("   ✅ Saved to MongoDB")
    
    # STEP 10: ADD TO FAISS
    print("\n🔍 STEP 10: Adding to FAISS index...")
    if not add_or_update_vector(student_numeric_id, embedding_list):
        print("   ❌ FAISS failed, rolling back...")
        delete_student(student_uuid)  # ✅ Using db.py function
        delete_student_files([resume_info["file_path"], linkedin_info["file_path"]])
        raise HTTPException(status_code=500, detail="FAISS indexing failed")
    
    print("   ✅ Added to FAISS")
    
    print(f"\n{'='*70}")
    print(f"✅ {name} REGISTERED SUCCESSFULLY!")
    print(f"{'='*70}\n")
    
    return {
        "success": True,
        "student_id": student_uuid,
        "numeric_id": student_numeric_id,
        "name": name,
        "master_summary": master_summary,
        "resume_summary": ai_resume_summary,
        "linkedin_summary": ai_linkedin_summary,
        "github_summary": external_summaries["github_summary"],
        "leetcode_summary": external_summaries["leetcode_summary"],
        "resume_url": resume_info["file_url"],
        "linkedin_url": linkedin_info["file_url"],
        "github_url": github_data["profile_url"],
        "leetcode_url": leetcode_data["profile_url"]
    }


# =====================================================
# GET STUDENT DETAILS
# =====================================================

@app.get("/student/{student_id}")
def get_student_endpoint(student_id: str):
    """Get complete student profile by ID"""
    student = get_student_by_uuid(student_id)  # ✅ Using db.py function
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student.pop("_id", None)
    student.pop("embedding", None)
    
    return student


# =====================================================
# RANK STUDENTS (JOB MATCHING)
# =====================================================

@app.post("/rank")
def rank_students(request: JobRequest, top_k: int = 100):
    """Rank students for a job description"""
    
    print(f"\n{'='*60}")
    print(f"🎯 Ranking students for job")
    print(f"{'='*60}")
    print(f"JD: {request.job_description[:100]}...")
    
    jd_embedding = model.encode(request.job_description)
    jd_lower = request.job_description.lower()

    is_dsa_role = any(word in jd_lower for word in [
       "dsa", "data structures", "algorithms",
       "competitive programming", "coding rounds"
    ])

    is_backend_role = any(word in jd_lower for word in [
       "backend", "api", "microservices", "scalable systems"
    ])

    is_ml_role = any(word in jd_lower for word in [
      "machine learning", "deep learning", "nlp",
      "computer vision", "model training"
    ])

    jd_embedding = jd_embedding / np.linalg.norm(jd_embedding)
    
    print("🔍 Searching FAISS index...")
    faiss_results = match(jd_embedding.tolist(), top_k=top_k)
    
    if not faiss_results:
        return {"message": "No students found", "ranked_students": []}
    
    print(f"   ✅ Found {len(faiss_results)} candidates")
    
    numeric_ids = [r["student_id"] for r in faiss_results]
    students = get_students_by_numeric_ids(numeric_ids)  # ✅ Using db.py function
    faiss_scores = {r["student_id"]: r["score"] for r in faiss_results}
    
    print("📊 Calculating scores...")
    ranked = []
    semantic_weight = 0.4
    github_weight = 0.3
    leetcode_weight = 0.3

    if is_dsa_role:
      semantic_weight = 0.3
      github_weight = 0.2
      leetcode_weight = 0.5

    elif is_backend_role:
      semantic_weight = 0.4
      github_weight = 0.4
      leetcode_weight = 0.2

    elif is_ml_role:
       semantic_weight = 0.6
       github_weight = 0.3
       leetcode_weight = 0.1

    for student in students:
        semantic_sim = faiss_scores.get(student["numeric_id"], 0.0)
        github_score = student["github"].get("github_score", 0) / 100
        leetcode_score = student["leetcode"].get("coding_score", 0) / 100
        
        final_score = (
          semantic_sim * semantic_weight +
          github_score * github_weight +
         leetcode_score * leetcode_weight
        )

        
        match_exp = generate_dynamic_match_explanation(
          job_description=request.job_description,
         student=student,
          semantic_similarity=semantic_sim,
           github_score=github_score,
           leetcode_score=leetcode_score,
          final_score=final_score
        )
        
        ranked.append({
            "student_id": student["student_id"],
            "numeric_id": student["numeric_id"],
            "name": student["name"],
            "branch": student["branch"],
            "year": student["year"],
            "skills": student["skills"],
            "final_score": round(final_score, 3),
            "semantic_similarity": round(semantic_sim, 3),
            "github_score": round(github_score, 3),
            "leetcode_score": round(leetcode_score, 3),
            "overall_summary": student.get("master_summary", ""),
            "github_summary": student.get("github_summary", ""),
            "leetcode_summary": student.get("leetcode_summary", ""),
            "match_explanation": match_exp,
            "github_profile": student.get("github", {}).get("profile_url", ""),
            "leetcode_profile": student.get("leetcode", {}).get("profile_url", ""),
            "resume_url": student.get("resume", {}).get("file_url", ""),
            "linkedin_url": student.get("linkedin", {}).get("file_url", ""),
            "github_stats": {
                "repos": student["github"].get("statistics", {}).get("total_repos", 0),
                "stars": student["github"].get("statistics", {}).get("total_stars", 0),
                "languages": list(student["github"].get("languages", {}).keys())[:5]
            },
            "leetcode_stats": {
                "total": student["leetcode"].get("problems_solved", {}).get("total", 0),
                "easy": student["leetcode"].get("problems_solved", {}).get("easy", 0),
                "medium": student["leetcode"].get("problems_solved", {}).get("medium", 0),
                "hard": student["leetcode"].get("problems_solved", {}).get("hard", 0),
                "contest_rating": student["leetcode"].get("contest_rating", 0)
            }
        })
    
    ranked.sort(key=lambda x: x["final_score"], reverse=True)
    
    print(f"✅ Returning {len(ranked)} ranked students\n")
    
    return {
        "job_description": request.job_description,
        "total_candidates": len(ranked),
        "ranked_students": ranked
    }


# =====================================================
# UPDATE STUDENT
# =====================================================

@app.put("/student/{student_id}")
async def update_student_endpoint(student_id: str, skills: str = Form(None)):
    """Update student skills and regenerate embedding"""
    student = get_student_by_uuid(student_id)  # ✅ Using db.py function
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    manual_skills = [s.strip() for s in skills.split(",")] if skills else student["skills"]
    
    profile_text = (
        f"{student.get('ai_resume_summary', '')} "
        f"{student.get('ai_linkedin_summary', '')} "
        f"{student.get('github_summary', '')} "
        f"{student.get('leetcode_summary', '')} "
        f"Skills: {' '.join(manual_skills)}"
    )
    
    embedding = model.encode(profile_text)
    embedding = embedding / np.linalg.norm(embedding)
    
    # Update using db.py function
    update_data = {
        "skills": manual_skills,
        "embedding": embedding.tolist(),
        "updated_at": datetime.utcnow()
    }
    
    update_student(student_id, update_data)  # ✅ Using db.py function
    add_or_update_vector(student["numeric_id"], embedding.tolist())
    
    return {"success": True, "message": "Student updated"}

import pandas as pd
import io
import json

@app.post("/bulk-upload")
async def bulk_upload(file: UploadFile = File(...)):

    if file.filename.endswith(".xlsx"):
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
        data = df.to_dict(orient="records")

    elif file.filename.endswith(".json"):
        contents = await file.read()
        data = json.loads(contents)

    else:
        return {"error": "Only .xlsx or .json files are supported"}

    inserted_count = 0

    for student in data:

        name = student.get("name")
        branch = student.get("branch")
        year = int(student.get("year"))
        skills = student.get("skills", "")
        github_username = student.get("github_username")
        leetcode_username = student.get("leetcode_username")

        manual_skills = [s.strip() for s in skills.split(",")] if skills else []

        # GitHub Fetch
        github_api_url = f"https://api.github.com/users/{github_username}/repos"
        response = requests.get(github_api_url)

        if response.status_code != 200:
            github_data = {"repos": 0, "stars": 0, "primary_languages": []}
        else:
            repos_data = response.json()
            total_repos = len(repos_data)
            total_stars = 0
            languages = set()

            for repo in repos_data:
                total_stars += repo.get("stargazers_count", 0)
                if repo.get("language"):
                    languages.add(repo["language"])

            github_data = {
                "repos": total_repos,
                "stars": total_stars,
                "primary_languages": list(languages)
            }

        # LeetCode Fetch
        leetcode_stats = fetch_leetcode_stats(leetcode_username)

        if leetcode_stats:
            leetcode_data = leetcode_stats
        else:
            leetcode_data = {"easy": 0, "medium": 0, "hard": 0, "rating": 0}

        # Embedding
        profile_text = " ".join(manual_skills) + " " + " ".join(github_data["primary_languages"])
        embedding = model.encode([profile_text])[0].tolist()

        student_document = {
            "name": name,
            "branch": branch,
            "year": year,
            "skills": manual_skills,
            "github": github_data,
            "leetcode": leetcode_data,
            "professional": {"internships": 0, "certifications": 0},
            "embedding": embedding,
            "source": "bulk"
        }

        students_collection.insert_one(student_document)
        inserted_count += 1

    return {"message": f"{inserted_count} students uploaded successfully"}
@app.post("/upload-documents/{student_name}")
async def upload_documents(
    student_name: str,
    linkedin_pdf: UploadFile = File(...),
    resume_pdf: UploadFile = File(...)
):

    student = students_collection.find_one({"name": student_name})

    if not student:
        return {"error": "Student not found"}

    # -------- Extract LinkedIn Text --------
    linkedin_text = ""
    try:
        with pdfplumber.open(linkedin_pdf.file) as pdf:
            for page in pdf.pages:
                linkedin_text += page.extract_text() or ""
    except:
        linkedin_text = ""

    # -------- Extract Resume Text --------
    resume_text = ""
    try:
        with pdfplumber.open(resume_pdf.file) as pdf:
            for page in pdf.pages:
                resume_text += page.extract_text() or ""
    except:
        resume_text = ""

    tech_keywords = [
        "python", "java", "react", "machine learning",
        "docker", "aws", "sql", "node", "fastapi",
        "tensorflow", "mongodb", "kubernetes",
        "c++", "javascript", "html", "css"
    ]

    combined_text = (linkedin_text + " " + resume_text).lower()

    extracted_skills = [
        keyword for keyword in tech_keywords
        if keyword in combined_text
    ]

    updated_skills = list(set(student["skills"] + extracted_skills))

    # Regenerate embedding
    profile_text = " ".join(updated_skills) + " " + " ".join(student["github"]["primary_languages"])
    new_embedding = model.encode([profile_text])[0].tolist()

    students_collection.update_one(
        {"name": student_name},
        {
            "$set": {
                "skills": updated_skills,
                "embedding": new_embedding,
                "has_documents": True
            }
        }
    )

    return {"message": "Documents uploaded and profile enriched successfully"}

# =====================================================
# DELETE STUDENT
# =====================================================

@app.delete("/student/{student_id}")
def delete_student_endpoint(student_id: str):
    """Delete student and their files"""
    student = get_student_by_uuid(student_id)  # ✅ Using db.py function
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Remove from FAISS
    remove_vector(student["numeric_id"])
    
    # Delete files
    file_paths = [
        student.get("resume", {}).get("file_path"),
        student.get("linkedin", {}).get("file_path")
    ]
    delete_student_files([fp for fp in file_paths if fp])
    
    # Delete from MongoDB
    delete_student(student_id)  # ✅ Using db.py function
    
    return {"success": True, "message": "Student deleted"}


# =====================================================
# DOWNLOAD FILE
# =====================================================

@app.get("/download/{filename}")
def download_file(filename: str):
    """Download uploaded file"""
    file_path = get_file_path(filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/pdf"
    )


# =====================================================
# HEALTH CHECK & STATS
# =====================================================

@app.get("/")
def health_check():
    """Health check endpoint"""
    return {
        "status": "running",
        "service": "AI Campus Placement System",
        "version": "3.0"
    }


@app.get("/stats")
def system_stats():
    """System statistics"""
    from vector_engine import get_stats
    
    return {
        "mongodb": {
            "total_students": students_collection.count_documents({}),
            "database": "alpha_coders",
            "collection": "students"
        },
        "faiss": get_stats(),
        "storage": {
            "upload_dir": UPLOAD_DIR,
            "total_files": len([f for f in os.listdir(UPLOAD_DIR) if f.endswith('.pdf')]) if os.path.exists(UPLOAD_DIR) else 0
        }
    }
@app.get("/students")
def list_students(skip: int = 0, limit: int = 100):
    """
    Get all students (without embeddings) for coordinator dashboard.
    """
    students = list(students_collection.find().skip(skip).limit(limit))
    for s in students:
        s.pop("_id", None)
        s.pop("embedding", None)  # remove heavy field
    return students
