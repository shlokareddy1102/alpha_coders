from openai import OpenAI
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

# Initialize OpenAI client (reads OPENAI_API_KEY automatically)
client = OpenAI()


# ==========================================================
# Helper: Safe JSON Extraction
# ==========================================================

def safe_json_parse(content: str):
    """
    Safely parses JSON even if wrapped in markdown code blocks.
    """
    content = content.strip()

    if content.startswith("```"):
        content = content.split("```")[1]

    return json.loads(content)


# ==========================================================
# 1️⃣ Comprehensive Summary (Single AI Call)
# ==========================================================

def generate_comprehensive_summary(student_data):

    github = student_data.get("github", {})
    leetcode = student_data.get("leetcode", {})

    projects_text = "\n".join([
        f"- {p.get('name', '')}: {p.get('description', '')} "
        f"({p.get('stars', 0)} stars, {p.get('language', '')})"
        for p in github.get("notable_projects", [])[:5]
    ])

    topics_text = ", ".join([
        f"{t.get('topic', '')} ({t.get('count', 0)} problems)"
        for t in leetcode.get("top_topics", [])[:5]
    ])

    prompt = f"""
Analyze this computer science student's profile and generate a comprehensive summary.

BASIC INFO:
- Name: {student_data.get('name', 'Unknown')}
- Branch: {student_data.get('branch', 'Unknown')}
- Year: {student_data.get('year', 'Unknown')}
- Skills: {', '.join(student_data.get('skills', []))}

GITHUB PROFILE:
- Total repos: {github.get('statistics', {}).get('total_repos', 0)}
- Total stars: {github.get('statistics', {}).get('total_stars', 0)}
- Languages: {', '.join(list(github.get('languages', {}).keys())[:5])}
- Notable projects:
{projects_text if projects_text else "No notable projects yet"}

LEETCODE PROFILE:
- Problems solved: {leetcode.get('problems_solved', {}).get('total', 0)}
  (Easy: {leetcode.get('problems_solved', {}).get('easy', 0)},
   Medium: {leetcode.get('problems_solved', {}).get('medium', 0)},
   Hard: {leetcode.get('problems_solved', {}).get('hard', 0)})
- Contest rating: {leetcode.get('contest_rating', 0)}
- Strong topics: {topics_text if topics_text else "Building foundations"}

Generate 3 summaries (each under 300 words):

1. github_summary
2. leetcode_summary
3. overall_summary (3–4 professional sentences)

Return ONLY valid JSON:
{{
  "github_summary": "...",
  "leetcode_summary": "...",
  "overall_summary": "..."
}}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert technical recruiter. Be concise and professional. Return only valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.6,
            max_tokens=500
        )

        content = response.choices[0].message.content
        return safe_json_parse(content)

    except Exception as e:
        print(f"AI summary failed: {e}")

        return {
            "github_summary": "GitHub profile indicates active development work.",
            "leetcode_summary": "LeetCode profile demonstrates problem-solving capability.",
            "overall_summary": f"{student_data.get('name', 'Candidate')} shows technical potential."
        }


# ==========================================================
# 2️⃣ Match Explanation
# ==========================================================

def generate_match_explanation(name, jd, scores, github_summary, leetcode_summary):

    prompt = f"""
You are an expert technical recruiter.

Job Description:
{jd}

Candidate: {name}

GitHub Summary:
{github_summary}

LeetCode Summary:
{leetcode_summary}

Scores:
Semantic Similarity: {scores.get('semantic_similarity', 0)}
GitHub Score: {scores.get('github_score', 0)}
LeetCode Score: {scores.get('leetcode_score', 0)}

Explain:
1. Key strengths aligned with role
2. Possible gaps
3. Overall recommendation (2–3 sentences)
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a technical recruiter explaining candidate matches concisely."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.5,
            max_tokens=200
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Match explanation failed: {e}")
        return "Moderate alignment with role based on technical indicators."


# ==========================================================
# 3️⃣ Structured Dynamic Match Explanation
# ==========================================================

def generate_dynamic_match_explanation(
    job_description,
    student,
    semantic_similarity,
    github_score,
    leetcode_score,
    final_score
):

    skills = ", ".join(student.get("skills", []))

    prompt = f"""
You are a senior technical recruiter.

JOB DESCRIPTION:
{job_description}

CANDIDATE:
Name: {student.get('name')}
Branch: {student.get('branch')}
Year: {student.get('year')}
Skills: {skills}

Scores:
Semantic Similarity: {semantic_similarity:.2f}
GitHub Score: {github_score:.2f}
LeetCode Score: {leetcode_score:.2f}
Final Score: {final_score:.2f}

Return ONLY valid JSON:

{{
  "fit_summary": "...",
  "technical_alignment": "...",
  "dsa_strength": "...",
  "gaps": "...",
  "verdict": "Strong Fit / Moderate Fit / Weak Fit"
}}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Be analytical and concise. Return only valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.4,
            max_tokens=500
        )

        content = response.choices[0].message.content
        return safe_json_parse(content)

    except Exception as e:
        print(f"Dynamic explanation failed: {e}")

        return {
            "fit_summary": "Moderate alignment with role.",
            "technical_alignment": "Partially aligned based on similarity score.",
            "dsa_strength": "Adequate DSA capability.",
            "gaps": "Further evaluation required.",
            "verdict": "Moderate Fit"
        }

