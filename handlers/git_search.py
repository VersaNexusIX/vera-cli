import requests

def handle(args):
    if not args:
        return "⚠️ try: git_search <keyword>"

    keyword = " ".join(args)
    url = f"https://api.github.com/search/repositories?q={keyword}&sort=stars&order=desc&per_page=5"

    try:
        r = requests.get(url, headers={"Accept": "application/vnd.github.v3+json"})
        if r.status_code != 200:
            return f"❌ GitHub API error ({r.status_code})"

        data = r.json().get("items", [])
        if not data:
            return f"🤔 There is no repository for '{keyword}'"

        out = [f"🔍 Search results '{keyword}':\n"]
        for repo in data:
            out.append(
                f"📦 {repo['full_name']}\n"
                f"⭐ {repo['stargazers_count']} | 🍴 {repo['forks_count']}\n"
                f"📖 {repo['description'] or '-'}\n"
                f"🔗 {repo['html_url']}\n"
            )
        return "\n".join(out)

    except Exception as e:
        return f"❌ Error git search: {e}"