import requests

def fetch_leetcode_data_for_ai(username):
    """
    Fetch LeetCode data and prepare for AI summarization
    Returns: Structured data + raw info for AI
    """
    
    url = "https://leetcode.com/graphql"
    
    query = """
    query getUserProfile($username: String!) {
      matchedUser(username: $username) {
        username
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
      userContestRanking(username: $username) {
        rating
        globalRanking
        attendedContestsCount
      }
    }
    """
    
    skills_query = """
    query skillStats($username: String!) {
      matchedUser(username: $username) {
        tagProblemCounts {
          advanced {
            tagName
            problemsSolved
          }
          intermediate {
            tagName
            problemsSolved
          }
          fundamental {
            tagName
            problemsSolved
          }
        }
      }
    }
    """
    
    try:
        # Fetch basic stats
        response = requests.post(
            url,
            json={"query": query, "variables": {"username": username}},
            timeout=10
        )
        
        if response.status_code != 200:
            return None
        
        basic_data = response.json().get("data", {})
        matched_user = basic_data.get("matchedUser")
        
        if not matched_user:
            return None
        
        # Parse problems solved
        ac_submissions = matched_user.get("submitStats", {}).get("acSubmissionNum", [])
        problems_solved = {"easy": 0, "medium": 0, "hard": 0, "total": 0}
        
        for item in ac_submissions:
            difficulty = item["difficulty"].lower()
            count = item["count"]
            if difficulty in problems_solved:
                problems_solved[difficulty] = count
                problems_solved["total"] += count
        
        # Contest stats
        contest_data = basic_data.get("userContestRanking", {})
        contest_rating = contest_data.get("rating", 0) if contest_data else 0
        
        # Fetch skills
        skills_response = requests.post(
            url,
            json={"query": skills_query, "variables": {"username": username}},
            timeout=10
        )
        
        # Parse top skills
        top_topics = []
        if skills_response.status_code == 200:
            skills_data = skills_response.json().get("data", {})
            if skills_data.get("matchedUser"):
                tag_counts = skills_data["matchedUser"].get("tagProblemCounts", {})
                
                all_tags = []
                for level in ["advanced", "intermediate", "fundamental"]:
                    all_tags.extend(tag_counts.get(level, []))
                
                # Sort by problems solved
                all_tags.sort(key=lambda x: x["problemsSolved"], reverse=True)
                top_topics = [
                    {"topic": tag["tagName"], "count": tag["problemsSolved"]}
                    for tag in all_tags[:10] if tag["problemsSolved"] > 0
                ]
        
        # Simple score
        coding_score = min(
            problems_solved["easy"] * 0.1 +
            problems_solved["medium"] * 0.3 +
            problems_solved["hard"] * 0.6 +
            (contest_rating - 1000) / 20 if contest_rating > 1000 else 0,
            100
        )
        
        return {
            "username": username,
            "problems_solved": problems_solved,
            "contest_rating": round(contest_rating, 2),
            "ranking": matched_user.get("profile", {}).get("ranking", 0),
            "top_topics": top_topics,
            "coding_score": round(coding_score, 2),
            "profile_url": f"https://leetcode.com/{username}"
        }
        
    except Exception as e:
        print(f"Error fetching LeetCode: {e}")
        return None
