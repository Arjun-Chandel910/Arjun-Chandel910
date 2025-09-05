import os
import requests
import jinja2

# Your GitHub username
USERNAME = "arjun-chandel910"

# --- Function to fetch the latest merged pull requests ---
# This uses the GitHub API to find your recent merged PRs
def get_merged_prs(username):
    headers = {"Authorization": f"token {os.getenv('GITHUB_TOKEN')}"}
    query = """
    query($username: String!) {
      user(login: $username) {
        pullRequests(
          first: 5,
          states: MERGED,
          orderBy: {field: CREATED_AT, direction: DESC}
        ) {
          nodes {
            title
            url
            repository {
              nameWithOwner
              primaryLanguage {
                name
                color
              }
            }
            createdAt
          }
        }
      }
    }
    """
    variables = {"username": username}
    response = requests.post(
        "https://api.github.com/graphql",
        json={"query": query, "variables": variables},
        headers=headers
    )
    return response.json().get("data", {}).get("user", {}).get("pullRequests", {}).get("nodes", [])

# --- Function to generate the animated SVG file ---
def generate_svg(template_data):
    templateLoader = jinja2.FileSystemLoader(searchpath="./")
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template("contribution_template.svg.j2")
    
    # Render the template with the fetched data
    output = template.render(pull_requests=template_data)
    
    with open("contribution_card.svg", "w") as f:
        f.write(output)

# --- Main script execution ---
if __name__ == "__main__":
    merged_prs = get_merged_prs(USERNAME)
    generate_svg(merged_prs)

    print("Successfully updated contribution_card.svg with merged PRs")