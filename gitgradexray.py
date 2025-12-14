from github import Github

GITHUB_TOKEN = "YOUR_GITHUB_TOKEN"
g = Github(GITHUB_TOKEN)

# -------------------------------
# Fetch Repository
# -------------------------------
def fetch_repo_info(repo_url):
    parts = repo_url.rstrip('/').split('/')
    owner, repo_name = parts[-2], parts[-1]
    return g.get_repo(f"{owner}/{repo_name}")

# -------------------------------
# README Analysis
# -------------------------------
def analyze_readme(repo):
    score = 0
    feedback = []
    try:
        content = repo.get_readme().decoded_content.decode().lower()
        if len(content) > 200: score += 2
        else: feedback.append("README description too short")

        if "install" in content or "setup" in content: score += 2
        else: feedback.append("Missing installation instructions")

        if "usage" in content or "example" in content: score += 2
        else: feedback.append("Missing usage examples")

        if "contribute" in content: score += 2
        else: feedback.append("Missing contribution guidelines")

        if "license" in content: score += 2
        else: feedback.append("Missing license information")
    except:
        feedback.append("README not found")

    return score, feedback

# -------------------------------
# Commit Analysis (SAFE)
# -------------------------------
def analyze_commits(repo):
    score = 0
    feedback = []

    commits = repo.get_commits()
    count = commits.totalCount

    if count < 10:
        score = 2
        feedback.append("Very few commits")
    elif count < 50:
        score = 4
    elif count < 200:
        score = 6
    else:
        score = 8

    return score, feedback

# -------------------------------
# Test Analysis (LIMITED)
# -------------------------------
def analyze_tests(repo):
    score = 0
    feedback = []

    try:
        contents = repo.get_contents("")
        test_found = False

        for item in contents[:15]:   # 🔴 LIMIT SCAN
            if "test" in item.name.lower():
                test_found = True
                break

        if test_found:
            score = 6
        else:
            feedback.append("No test folder found")

    except:
        feedback.append("Test analysis skipped")

    return score, feedback

# -------------------------------
# Final Evaluation
# -------------------------------
def generate_health_score(r, c, t):
    total = r*2 + c*3 + t*2
    score = int((total / 50) * 100)

    if score >= 80: level = "Advanced"
    elif score >= 50: level = "Intermediate"
    else: level = "Beginner"

    return score, level

def recruiter_verdict(score):
    return "Shortlist-ready" if score >= 60 else "Rejected"
