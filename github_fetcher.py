import requests
from collections import Counter

def fetch_github_data_for_ai(username):
    """
    Fetch GitHub data and prepare for AI summarization
    Returns: Structured data + raw info for AI
    """
    
    base_url = "https://api.github.com"
    
    try:
        # Fetch user profile
        user_response = requests.get(f"{base_url}/users/{username}", timeout=10)
        if user_response.status_code != 200:
            return None
        
        user_data = user_response.json()
        
        # Fetch repositories
        repos_response = requests.get(
            f"{base_url}/users/{username}/repos?per_page=100&sort=updated",
            timeout=10
        )
        if repos_response.status_code != 200:
            return None
        
        repos = repos_response.json()
        
        # Basic stats (for scoring)
        total_repos = len(repos)
        total_stars = sum(repo.get("stargazers_count", 0) for repo in repos)
        total_forks = sum(repo.get("forks_count", 0) for repo in repos)
        
        # Languages
        languages = Counter()
        for repo in repos:
            if repo.get("language"):
                languages[repo["language"]] += 1
        
        # Notable projects (for AI to analyze)
        notable_projects = []
        for repo in repos:
            if repo.get("fork") and repo.get("stargazers_count", 0) < 5:
                continue
            
            if repo.get("stargazers_count", 0) >= 3 or repo.get("description"):
                notable_projects.append({
                    "name": repo["name"],
                    "description": repo.get("description", "No description"),
                    "language": repo.get("language", "Unknown"),
                    "stars": repo.get("stargazers_count", 0),
                    "topics": repo.get("topics", [])
                })
        
        # Sort by popularity
        notable_projects.sort(key=lambda x: x["stars"], reverse=True)
        
        # Simple score (for hybrid formula later)
        github_score = min((total_repos * 0.5 + total_stars * 2 + total_forks * 3) / 10, 100)
        
        return {
            "username": username,
            "statistics": {
                "total_repos": total_repos,
                "total_stars": total_stars,
                "total_forks": total_forks
            },
            "languages": dict(languages.most_common(10)),
            "notable_projects": notable_projects[:10],  # Top 10 for AI
            "github_score": round(github_score, 2),
            "profile_url": f"https://github.com/{username}"
        }
        
    except Exception as e:
        print(f"Error fetching GitHub: {e}")
        return None
