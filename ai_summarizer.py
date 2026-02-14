import openai
import os
import json

openai.api_key = os.getenv("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")

def generate_comprehensive_summary(student_data):
    """
    ONE AI CALL - Generate everything at once
    Much more efficient!
    """
    
    # Prepare all data for AI
    github = student_data.get('github', {})
    leetcode = student_data.get('leetcode', {})
    
    # Format notable projects
    projects_text = "\n".join([
        f"- {p['name']}: {p['description']} ({p['stars']} stars, {p['language']})"
        for p in github.get('notable_projects', [])[:5]
    ])
    
    # Format top LeetCode topics
    topics_text = ", ".join([
        f"{t['topic']} ({t['count']} problems)"
        for t in leetcode.get('top_topics', [])[:5]
    ])
    
    prompt = f"""
    Analyze this computer science student's profile and generate a comprehensive summary.
    
    BASIC INFO:
    - Name: {student_data['name']}
    - Branch: {student_data['branch']}
    - Year: {student_data['year']}
    - Skills: {', '.join(student_data['skills'])}
    
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
    
    Generate 3 summaries (keep each under 300 words):
    
    1. GITHUB_SUMMARY: Focus on project work, languages, and notable achievements
    2. LEETCODE_SUMMARY: Focus on problem-solving ability and algorithmic strength
    3. OVERALL_SUMMARY: Professional 3-4 sentence summary suitable for recruiters and which shows the skills of the student properly
    
    Format as JSON:
    {{
      "github_summary": "...",
      "leetcode_summary": "...",
      "overall_summary": "..."
    }}
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert technical recruiter. Create concise, professional summaries that highlight key strengths. Return ONLY valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=400,
            temperature=0.7
        )
        
        import json
        summaries = json.loads(response.choices[0].message.content.strip())
        return summaries
        
    except Exception as e:
        print(f"AI summary failed: {e}")
        # Fallback to simple summaries
        return {
            "github_summary": f"Developer with {github.get('statistics', {}).get('total_repos', 0)} repositories using {', '.join(list(github.get('languages', {}).keys())[:3])}.",
            "leetcode_summary": f"Solved {leetcode.get('problems_solved', {}).get('total', 0)} LeetCode problems with focus on {', '.join([t['topic'] for t in leetcode.get('top_topics', [])[:3]])}.",
            "overall_summary": f"{student_data['name']} is a {student_data['branch']} student with skills in {', '.join(student_data['skills'][:3])}."
        }


def generate_match_explanation(name, jd, scores, github_summary, leetcode_summary):

    prompt = f"""
    You are an expert technical recruiter.

Given:
- Job Description
- Candidate profile summary
- GitHub activity
- LeetCode performance

Explain:
1. Why this candidate is suitable for this role.
2. Where they are strongest.
3. Any potential gaps.
4. What makes them rank highly.

Be specific. Avoid generic praise.


    Job Description:
    {jd}

    Candidate: {name}

    GitHub Summary:
    {github_summary}

    LeetCode Summary:
    {leetcode_summary}

    Scores:
    Semantic Similarity: {scores['semantic_similarity']}
    GitHub Score: {scores['github_score']}
    LeetCode Score: {scores['leetcode_score']}

    Provide:
    1. Key strengths aligned with the role
    2. Possible gaps
    3. Overall recommendation in 2–3 sentences
    """

    # call your LLM here

    
    try:
        response = openai.ChatCompletion.create(
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
            max_tokens=150,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"Match explanation failed: {e}")
        return f"Strong alignment with {scores['semantic_similarity']*100:.0f}% skills match."

def generate_dynamic_match_explanation(
    job_description,
    student,
    semantic_similarity,
    github_score,
    leetcode_score,
    final_score
):
    """
    Generates structured, job-aware reasoning for candidate ranking.
    """

    skills = ", ".join(student.get("skills", []))
    github_summary = student.get("github_summary", "")
    leetcode_summary = student.get("leetcode_summary", "")

    prompt = f"""
You are a senior technical recruiter.

Analyze the candidate against the job description.

JOB DESCRIPTION:
{job_description}

CANDIDATE:
Name: {student['name']}
Branch: {student['branch']}
Year: {student['year']}
Skills: {skills}

GitHub:
{github_summary}

LeetCode:
{leetcode_summary}

Scores:
Semantic Similarity: {semantic_similarity:.2f}
GitHub Score: {github_score:.2f}
LeetCode Score: {leetcode_score:.2f}
Final Score: {final_score:.2f}

Return ONLY valid JSON in this format:

{{
  "fit_summary": "...",
  "technical_alignment": "...",
  "dsa_strength": "...",
  "gaps": "...",
  "verdict": "Strong Fit / Moderate Fit / Weak Fit"
}}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert technical recruiter. Be analytical and concise. Return only valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.4,
            max_tokens=500
        )

        content = response.choices[0].message.content.strip()

        return json.loads(content)

    except Exception as e:
        print(f"Dynamic explanation failed: {e}")

        # Safe fallback
        return {
            "fit_summary": f"{student['name']} shows moderate alignment with the role.",
            "technical_alignment": "Profile aligns partially based on semantic similarity.",
            "dsa_strength": "DSA performance contributes moderately.",
            "gaps": "Further evaluation required.",
            "verdict": "Moderate Fit"
        }
