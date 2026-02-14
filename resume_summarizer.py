import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")


def summarize_resume_with_ai(resume_text):
    """
    Use AI to create intelligent summary of resume
    
    Args:
        resume_text: Raw text extracted from resume PDF
    
    Returns:
        Professional summary of resume
    """
    
    # Limit text to avoid token limits (first 4000 chars)
    truncated_text = resume_text[:4000]
    
    prompt = f"""
    Analyze this resume and create a concise professional summary (3-4 sentences max).
    
    Focus on:
    - Educational background and major
    - Key technical skills and expertise areas
    - Notable work experience or internships
    - Standout projects or achievements
    
    Resume text:
    {truncated_text}
    
    Create a compelling summary that a recruiter would find valuable.
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert technical recruiter who writes compelling, concise candidate summaries. Focus on technical skills, experience, and achievements."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=200,
            temperature=0.7
        )
        
        summary = response.choices[0].message.content.strip()
        return summary
        
    except Exception as e:
        print(f"AI resume summary failed: {e}")
        # Fallback to first 200 characters
        return resume_text[:200] + "..."


def summarize_linkedin_with_ai(linkedin_text):
    """
    Use AI to create intelligent summary of LinkedIn profile
    
    Args:
        linkedin_text: Raw text extracted from LinkedIn PDF
    
    Returns:
        Professional summary of LinkedIn profile
    """
    
    truncated_text = linkedin_text[:4000]
    
    prompt = f"""
    Analyze this LinkedIn profile and create a concise professional summary (2-3 sentences max).
    
    Focus on:
    - Current role and company
    - Professional experience highlights
    - Key accomplishments or skills mentioned
    
    LinkedIn profile text:
    {truncated_text}
    
    Create a summary that highlights career trajectory and expertise.
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert technical recruiter analyzing LinkedIn profiles. Be concise and focus on career highlights."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        summary = response.choices[0].message.content.strip()
        return summary
        
    except Exception as e:
        print(f"AI LinkedIn summary failed: {e}")
        return linkedin_text[:200] + "..."


def create_comprehensive_profile_summary(resume_text, linkedin_text, github_summary, leetcode_summary, skills):
    """
    Create ONE comprehensive summary combining ALL sources
    
    This is the MASTER summary that recruiters will see first
    """
    
    prompt = f"""
    Create a comprehensive professional summary (4-5 sentences) for this candidate.
    Synthesize information from multiple sources into a compelling narrative.
    
    RESUME HIGHLIGHTS:
    {resume_text[:1500]}
    
    LINKEDIN PROFILE:
    {linkedin_text[:1000]}
    
    GITHUB ACTIVITY:
    {github_summary}
    
    LEETCODE PERFORMANCE:
    {leetcode_summary}
    
    SKILLS:
    {', '.join(skills)}
    
    Create a summary that:
    1. Starts with their strongest qualification
    2. Mentions specific technical skills and expertise
    3. Highlights notable projects or achievements
    4. Describes their problem-solving ability (from LeetCode)
    5. Sounds professional and compelling
    
    Make them sound impressive while being truthful to the data.
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert technical recruiter writing compelling candidate profiles. Synthesize multiple data sources into a cohesive narrative that highlights the candidate's strengths."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=250,
            temperature=0.7
        )
        
        summary = response.choices[0].message.content.strip()
        return summary
        
    except Exception as e:
        print(f"AI comprehensive summary failed: {e}")
        return f"Candidate with skills in {', '.join(skills[:5])}. {github_summary} {leetcode_summary}"


def extract_key_skills_from_resume(resume_text):
    """
    Use AI to extract and categorize skills from resume
    
    This helps when students don't manually list all their skills
    """
    
    prompt = f"""
    Extract all technical skills from this resume.
    Return ONLY a JSON object with categorized skills.
    
    Resume:
    {resume_text[:3000]}
    
    Format:
    {{
        "programming_languages": ["Python", "Java", ...],
        "frameworks": ["React", "TensorFlow", ...],
        "tools": ["Docker", "Git", ...],
        "domains": ["Machine Learning", "Web Development", ...]
    }}
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a technical skills extractor. Return ONLY valid JSON, no other text."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=300,
            temperature=0.3
        )
        
        import json
        skills = json.loads(response.choices[0].message.content.strip())
        return skills
        
    except Exception as e:
        print(f"AI skill extraction failed: {e}")
        return {
            "programming_languages": [],
            "frameworks": [],
            "tools": [],
            "domains": []
        }
