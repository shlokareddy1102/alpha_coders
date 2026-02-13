from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import requests
import pdfplumber

# -----------------------------------
# Initialize FastAPI
# -----------------------------------
app = FastAPI()

# -----------------------------------
# MongoDB Connection
# -----------------------------------
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["alpha_coders"]
students_collection = db["students"]

print("Connected to DB:", db.name)
print("Collections:", db.list_collection_names())

# -----------------------------------
# Load Embedding Model (Load once)
# -----------------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------------
# Request Model for Ranking
# -----------------------------------
class JobRequest(BaseModel):
    job_description: str

# -----------------------------------
# LeetCode Fetch Function
# -----------------------------------
def fetch_leetcode_stats(username):
    url = "https://leetcode.com/graphql"

    query = """
    query getUserProfile($username: String!) {
      matchedUser(username: $username) {
        submitStats {
          acSubmissionNum {
            difficulty
            count
          }
        }
        profile {
          ranking
        }
      }
    }
    """

    variables = {"username": username}

    try:
        response = requests.post(url, json={"query": query, "variables": variables})
    except:
        return None

    if response.status_code != 200:
        return None

    data = response.json()
    user = data.get("data", {}).get("matchedUser")

    if not user:
        return None

    stats = user["submitStats"]["acSubmissionNum"]

    easy = medium = hard = 0

    for item in stats:
        if item["difficulty"] == "Easy":
            easy = item["count"]
        elif item["difficulty"] == "Medium":
            medium = item["count"]
        elif item["difficulty"] == "Hard":
            hard = item["count"]

    ranking = user["profile"]["ranking"]

    return {
        "easy": easy,
        "medium": medium,
        "hard": hard,
        "rating": ranking
    }

# -----------------------------------
# Placement Coordinator Endpoint
# -----------------------------------
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

    # -------- GitHub Fetch --------
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

    # -------- LeetCode Fetch --------
    leetcode_stats = fetch_leetcode_stats(leetcode_username)

    if leetcode_stats:
        leetcode_data = leetcode_stats
    else:
        leetcode_data = {"easy": 0, "medium": 0, "hard": 0, "rating": 0}

    # -------- LinkedIn Parsing --------
    linkedin_text = ""
    try:
        with pdfplumber.open(linkedin_pdf.file) as pdf:
            for page in pdf.pages:
                linkedin_text += page.extract_text() or ""
    except:
        linkedin_text = ""

    # -------- Resume Parsing --------
    resume_text = ""
    try:
        with pdfplumber.open(resume_pdf.file) as pdf:
            for page in pdf.pages:
                resume_text += page.extract_text() or ""
    except:
        resume_text = ""

    # -------- Skill Extraction --------
    tech_keywords = [
        "python", "java", "react", "machine learning",
        "docker", "aws", "sql", "node", "fastapi",
        "tensorflow", "mongodb", "kubernetes",
        "c++", "c", "html", "css", "javascript"
    ]

    combined_text = (linkedin_text + " " + resume_text).lower()

    extracted_skills = [
        keyword for keyword in tech_keywords
        if keyword in combined_text
    ]

    manual_skills = [s.strip() for s in skills.split(",")]
    combined_skills = list(set(manual_skills + extracted_skills))

    # -------- Embedding Generation --------
    profile_text = " ".join(combined_skills) + " " + " ".join(github_data["primary_languages"])
    student_embedding = model.encode([profile_text])[0].tolist()

    student_document = {
        "name": name,
        "branch": branch,
        "year": year,
        "skills": combined_skills,
        "github": github_data,
        "leetcode": leetcode_data,
        "professional": {"internships": 0, "certifications": 0},
        "embedding": student_embedding
    }

    result = students_collection.insert_one(student_document)
    print("Inserted ID:", result.inserted_id)

    return {"message": "Student added successfully with resume + LinkedIn analysis"}

# -----------------------------------
# Recruiter Ranking Endpoint
# -----------------------------------
@app.post("/rank")
def rank_students(request: JobRequest):

    job_description = request.job_description
    job_embedding = model.encode([job_description])
    job_text_lower = job_description.lower()

    students = list(students_collection.find())
    ranked_students = []

    for student in students:

        if "embedding" not in student:
            continue

        student_embedding = np.array(student["embedding"]).reshape(1, -1)
        similarity = cosine_similarity(job_embedding, student_embedding)[0][0]

        github_score = student["github"]["repos"] * 0.5 + student["github"]["stars"] * 0.2

        leetcode_score = (
            student["leetcode"]["easy"] * 0.1 +
            student["leetcode"]["medium"] * 0.3 +
            student["leetcode"]["hard"] * 0.6
        )

        final_score = (
            similarity * 50 +
            github_score * 0.05 +
            leetcode_score * 0.02
        )

        # -------- Smart Reasoning --------
        reasoning = []

        matched_skills = [
            skill for skill in student["skills"]
            if skill.lower() in job_text_lower
        ]

        if matched_skills:
            reasoning.append(f"Matched required skills: {', '.join(matched_skills)}")

        matched_languages = [
            lang for lang in student["github"]["primary_languages"]
            if lang and lang.lower() in job_text_lower
        ]

        if matched_languages:
            reasoning.append(f"GitHub projects use: {', '.join(matched_languages)}")

        if similarity > 0.7:
            reasoning.append("Strong semantic alignment with job description")

        if student["leetcode"]["hard"] > 30:
            reasoning.append("Strong DSA performance (many hard problems solved)")

        ranked_students.append({
            "name": student["name"],
            "final_score": round(float(final_score), 2),
            "similarity": round(float(similarity), 3),
            "reasoning": reasoning
        })

    ranked_students.sort(key=lambda x: x["final_score"], reverse=True)

    return ranked_students
