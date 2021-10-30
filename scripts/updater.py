import os, json, re, requests

def commentGetter(url: str) -> str:
    """Get the url response as json and returns a string if the body of a comment starts with the string \"CONTRIBUIDORES:\" """
    response = requests.get(url).json()
    for e in response[::-1]:
        b = e.get("body")
        if b.startswith("CONTRIBUIDORES:"):
            return b

def buildContributor(comment: str) -> list:
    """Returns a list of contributors formatted accordingly to markup language with their github pages."""
    contribs = []
    users = re.findall(r'(?<=@)(\w+)', comment)
    for u in users:
        s = f"[@{u}](https://github.com/{u})"
        contribs.append(s)
    return contribs

def main():
    repo = os.getenv("repo")
    reporl = repo.replace(" ", "%20")
    assignees = json.loads(os.getenv("assignees"))

    _readme = open("README.md", "a")

    contributorsList = []
    if assignees:
        for assignee in assignees:
            login = assignee.get("login")
            url = assignee.get("html_url")
            s = f"[@{login}]({url})"
            contributorsList.append(s)
    else:
        body = os.getenv("body")
        comments_url = os.getenv("comments_url")
        comments = commentGetter(comments_url)
        review_comments_url = os.getenv("review_comments_url")
        review_comments = commentGetter(review_comments_url)

        if body.startswith("CONTRIBUIDORES:"):
            contributorsList = buildContributor(body)
        elif comments:
            contributorsList = buildContributor(comments)
        elif review_comments:
            contributorsList = buildContributor(review_comments)
    
    contributorsString = ", ".join(contributorsList)

    string = f"\n### [{repo}](https://github.com/ifpeopensource/workshops/tree/main/{reporl}), com {contributorsString}"
    _readme.write(string)
    _readme.close()

if __name__ == "__main__":
    main()    