from bs4 import BeautifulSoup

def audit_ui(html: str):
    soup = BeautifulSoup(html, "html.parser")
    score = 100
    issues = []

    if not soup.title or not soup.title.string.strip():
        issues.append("Missing or empty <title> tag")
        score -= 10

    if not soup.find_all("h1"):
        issues.append("No H1 headings found")
        score -= 10

    if not soup.find_all("a", string=lambda s: s and "contact" in s.lower()):
        issues.append("No clear contact or CTA link")
        score -= 15

    if not soup.find_all("img"):
        issues.append("No images found")
        score -= 5

    if len(soup.get_text()) < 300:
        issues.append("Very little on-page content")
        score -= 10

    score = max(score, 0)
    return score, issues
